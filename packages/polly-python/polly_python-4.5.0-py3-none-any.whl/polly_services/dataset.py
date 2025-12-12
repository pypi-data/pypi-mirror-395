import os
from os.path import join as join_paths
from datetime import datetime
import logging
import warnings
import gzip
import re
from dataclasses import dataclass
from typing import Tuple, Optional, Union, TYPE_CHECKING, Any
import json
import tempfile

from requests import Response
import boto3
import botocore
from botocore.client import BaseClient
from botocore.credentials import RefreshableCredentials
from botocore.session import get_session

from polly.auth import Polly, UnauthorizedException
from polly.s3_utils import copy_file, read_bytes
from polly.errors import error_handler

if TYPE_CHECKING:
    from cmapPy.pandasGEXpress.GCToo import GCToo
    from anndata import AnnData


class UnsupportedFormat(ValueError):
    pass


def humanize_unix_timestamp(unix_timestamp_ms: int) -> str:
    """
    Converts a Unix timestamp in milliseconds to a human-readable date and time string.

    Args:
        unix_timestamp_ms: The Unix timestamp in milliseconds.

    Returns:
        A string representing the date and time in the format "YYYY-MM-DD HH:MM:SS"
    """
    unix_timestamp = unix_timestamp_ms / 1000.0
    dt = datetime.fromtimestamp(unix_timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def sanitize_user_defined_id(string):
    if len(str(string)) == 0:
        raise ValueError("Empty string cannot be sanitized")

    string = re.sub("[^0-9a-zA-Z_-]", "_", string)
    return string


def validate_user_defined_id(identifier: str, name_for_id: str):
    if identifier == "":
        raise ValueError(f"Empty string cannot be used as {name_for_id}")
    sanitized_id = sanitize_user_defined_id(identifier)
    if identifier != sanitized_id:
        raise ValueError(
            f"Cannot use '{identifier}' as {name_for_id},"
            f" consider using '{sanitized_id}'",
        )


def handle_errors_or_warnings(response: Response):
    error_handler(response)

    # this try-except block exists just in case
    # the response doesn't have any body (or has a non-json body)
    try:
        response_dict = response.json()

        if "meta" not in response_dict:
            return
        if "warnings" not in response_dict["meta"]:
            return
        msgs = response_dict["meta"]["warnings"]
        if not isinstance(msgs, list):
            return
        for msg in msgs:
            if not isinstance(msg, str):
                continue
            warnings.warn(msg)
    except Exception:
        pass


@dataclass
class S3SessionDetails:
    session: boto3.Session
    client: BaseClient
    bucket: str
    prefix: str
    access: Optional[str] = None  # 'read' or 'write'


class S3ClientManager:
    """
    Retrieving the right S3 client for the omixatlas S3 bucket

    The client returned by `get_client` is configured with temporary
    tokens for the omixatlas bucket, and auto-refreshes when they
    expire

    Clients are cached, and as per AWS docs they are thread safe
    """

    _cache = {}

    def __init__(self, omixatlas_id: str, copy_dest_omixatlas_id: Optional[str] = None):
        if Polly.default_session is None:
            raise UnauthorizedException()

        self.omixatlas_id = omixatlas_id
        self.copy_dest_omixatlas_id = copy_dest_omixatlas_id
        self.get_polly_session = lambda: Polly.default_session

    def _init_client(self) -> S3SessionDetails:
        if (self.omixatlas_id, self.copy_dest_omixatlas_id) not in self._cache:
            session_details = self._get_autorefresh_session()
            self._cache[(self.omixatlas_id, self.copy_dest_omixatlas_id)] = (
                session_details
            )

        return self._cache[(self.omixatlas_id, self.copy_dest_omixatlas_id)]

    def clear(self):
        """
        Clears cached tokens
        """
        self._cache.pop((self.omixatlas_id, self.copy_dest_omixatlas_id), None)

    def get_client(self) -> BaseClient:
        session_details = self._init_client()
        return session_details.client

    def get_upload_path(self) -> Tuple[str, str]:
        session_details = self._init_client()
        return session_details.bucket, session_details.prefix

    def get_access_level(self) -> Optional[str]:
        "'read' or 'write'"
        session_details = self._init_client()
        return session_details.access

    def _generate_temp_s3_tokens(self):
        logging.debug(
            f"Generating temporary S3 tokens for omixatlas_id='{self.omixatlas_id}'"
        )

        # post request for upload urls
        payload = {
            "data": {
                "type": "session-tokens",
                "attributes": {
                    "omixatlas_id": self.omixatlas_id,
                    "copy_dest_omixatlas_id": self.copy_dest_omixatlas_id,
                },
            }
        }

        # post request
        url = f"{self.get_polly_session().discover_url}/session-tokens"

        resp = self.get_polly_session().post(url, json=payload)
        handle_errors_or_warnings(resp)

        response_data = resp.json()
        attrs = response_data["data"]["attributes"]

        credentials = {}
        if self.copy_dest_omixatlas_id is None:
            bucket_name = attrs["bucket_name"]
            prefix = attrs["prefix"]
            access_level = attrs.get("access_level")
        else:
            bucket_name = attrs["copy_dest_details"]["bucket_name"]
            prefix = attrs["copy_dest_details"]["prefix"]
            access_level = attrs["copy_dest_details"].get("access_level")

        tokens = attrs["tokens"]
        credentials["access_key"] = tokens["AccessKeyId"]
        credentials["secret_key"] = tokens["SecretAccessKey"]
        credentials["token"] = tokens["SessionToken"]
        credentials["expiry_time"] = tokens["Expiration"]

        return credentials, bucket_name, prefix, access_level

    def _get_autorefresh_session(self) -> S3SessionDetails:
        creds, bucket, folder, access_level = self._generate_temp_s3_tokens()

        def refresh_using():
            creds, _, _, _ = self._generate_temp_s3_tokens()
            return creds

        session_credentials = RefreshableCredentials.create_from_metadata(
            metadata=creds,
            refresh_using=refresh_using,
            method="files-endpoint",
        )

        session = get_session()
        session._credentials = session_credentials
        autorefresh_session = boto3.Session(botocore_session=session)
        config = botocore.config.Config(max_pool_connections=30)
        client = autorefresh_session.client("s3", config=config)

        return S3SessionDetails(
            session=autorefresh_session,
            client=client,
            bucket=bucket,
            prefix=folder,
            access=access_level,
        )


def is_supported_format(path: str) -> bool:
    try:
        infer_file_type(path)
    except UnsupportedFormat:
        return False

    return True


def infer_file_type(path: str) -> Tuple[str, str]:
    """
    Args:
        path (str): The file path for which to infer the file type.

    Returns:
        A tuple containing the inferred file type and file extension.

    Raises:
        UnsupportedFormat: If the file extension is not recognized as a supported format
    """
    extension_to_format = {
        ".txt": "txt",
        ".gct": "gct",
        ".csv": "csv",
        ".tsv": "tsv",
        ".h5ad": "h5ad",
        ".fasta": "fasta",
        ".fa": "fasta",
        ".fastq": "fastq",
        ".sam": "sam",
        ".bam": "bam",
        ".vcf": "vcf",
        ".maf": "maf",
        ".idat": "idat",
        ".bed": "bed",
        ".dcm": "dcm",
        ".nii": "nifti",
        ".pdb": "pdb",
        ".mzml": "mzml",
        ".cel": "cel",
        ".fcs": "fcs",
        ".ped": "plink",
        ".map": "plink",
        ".ab1": "ab1",
        ".sff": "sff",
        ".tiff": "tiff",
        ".tif": "tiff",
        ".jpg": "jpeg",
        ".jpeg": "jpeg",
        ".png": "png",
        ".xml": "xml",
        ".json": "json",
        ".sbml": "sbml",
        ".gff": "gff",
        ".parquet": "parquet",
        ".pdf": "pdf",
        ".rds": "rds",
        ".RData": "rdata",
        ".rdata": "rdata",
        ".h5Seurat": "h5seurat",
        ".h5seurat": "h5seurat",
    }
    for ext, format in list(extension_to_format.items()):
        extension_to_format[ext + ".gz"] = format + "+gzip"

    extension = extract_file_extension(path)
    if extension in extension_to_format:
        return extension_to_format[extension], extension

    raise UnsupportedFormat(f"Couldn't infer file type {path}")


def extract_extension_from_s3_uri(uri: str) -> str:
    """
    Args:
        uri (str): S3 URI (e.g. s3://mybucket/file.txt)

    Returns:
        str: The file extension, including the leading period (e.g., '.txt'),
             or an empty string if no extension is found.
    """
    uri_without_version = uri.split("?")[0]

    s3_key = uri_without_version.rstrip("/").split("/")[-1]

    if s3_key.startswith("."):
        return "" if s3_key.count(".") == 1 else ".".join(s3_key.split(".")[1:])
    parts = s3_key.split(".")
    if len(parts) > 1:
        extension = "." + ".".join(parts[1:])  # Join all parts except the file name
    else:
        extension = ""  # No extension present
    return extension


class VersionBase:
    _s3_client_manager: S3ClientManager

    def __init__(self, **kwargs):
        self.omixatlas_id: str = kwargs.get("omixatlas_id")
        self.dataset_id: str = kwargs.get("dataset_id")
        self.version_id: str = kwargs.get("version_id")
        self.data_type: str = kwargs.get("data_type")
        self.metadata_location: str = kwargs.get("metadata_location")
        self.data_location: str = kwargs.get("data_location")
        self.data_format: str = kwargs.get("data_format")
        self.created_at: int = kwargs.get("created_at")

        self.attributes = kwargs

    def metadata(self) -> dict:
        """
        Retrieves the metadata for the dataset.

        Returns:
            The metadata dictionary.

        Examples:
            >>> metadata = dataset.metadata()
            >>> print(metadata)
            {'description': '...'}
        """
        if not hasattr(self, "_metadata"):
            raw_data = read_bytes(
                self._s3_client_manager.get_client(), self.metadata_location
            )
            self._metadata = json.loads(gzip.decompress(raw_data).decode("utf-8"))

        return self._metadata

    def load(self) -> Union["GCToo", "AnnData"]:
        """
        Loads the underlying data into memory, as a GCToo or AnnData object

        Returns:
            The loaded data object

        Raises:
            ValueError: If the data format is not supported or cannot be determined.

        Examples:
            >>> adata = dataset.load()
        """
        if self.data_format is None:
            raise ValueError(
                "Unable to determine file format. Use `dataset.download(...)` instead"
            )

        if self.data_format == "gct":
            from cmapPy.pandasGEXpress.parse import parse

            with tempfile.NamedTemporaryFile("w", suffix=".gct", delete=True) as f:
                # Using a context manager to handle the temporary file
                tmp_file_path = f.name
                copy_file(
                    self.data_location,
                    tmp_file_path,
                    s3_client=self._s3_client_manager.get_client(),
                )
                return parse(tmp_file_path)

        if self.data_format == "h5ad":
            import anndata

            with tempfile.NamedTemporaryFile("w", suffix=".h5ad", delete=True) as f:
                # Using a context manager to handle the temporary file
                tmp_file_path = f.name
                copy_file(
                    self.data_location,
                    tmp_file_path,
                    s3_client=self._s3_client_manager.get_client(),
                )
                return anndata.read_h5ad(tmp_file_path)

        raise ValueError(f"Unsupported format: {self.data_format}")

    def download(self, path: str) -> str:
        """
        Args:
            path: Can be a directory or a file path.

        Returns:
            The relative path where the data was downloaded

        Examples:
            >>> dataset.download('./mydataset.h5ad')
        """
        if path.endswith(os.sep):  # if it looks like a directory
            format_to_extension = {
                "csv": ".csv",
                "json+gzip": ".json.gz",
                "gct": ".gct",
                "h5ad": ".h5ad",
            }

            if self.data_format in format_to_extension:
                extension = format_to_extension[self.data_format]
            else:
                extension = extract_extension_from_s3_uri(self.data_location)

            path = join_paths(path, f"{self.dataset_id}{extension}")

        copy_file(
            self.data_location, path, s3_client=self._s3_client_manager.get_client()
        )
        return path


class SupplementaryFile:
    """
    Class that represents a supplementary file

    Attributes:
        dataset_id: Dataset Identifier
        omixatlas_id: OmixAtlas ID (e.g. `'1673411159486'`)
        file_name: Unique identifier for the file
        file_format: Format of the file (e.g. `vcf`, `csv`, `pdf`)
        tag: An optional tag for the file
        created_at: Unix timestamp (ms) for when the file was added (or modified)
    """

    dataset_id: str
    omixatlas_id: str
    file_name: str
    file_format: str
    file_location: str
    tag: Optional[str]
    derived_from: Optional[str]
    created_at: int

    def __init__(self, **kwargs):
        self.dataset_id: str = kwargs.get("dataset_id")
        self.omixatlas_id: str = kwargs.get("omixatlas_id")
        self.file_name: str = kwargs.get("file_name")
        self.file_format: str = kwargs.get("file_format")
        self.file_location: str = kwargs.get("file_location")
        self.tag: Optional[str] = kwargs.get("tag")
        self.derived_from: Optional[str] = kwargs.get("derived_from")
        self.created_at: int = kwargs.get("created_at")

        self._s3_client_manager = S3ClientManager(self.omixatlas_id)

    def __repr__(self) -> str:
        created_at = humanize_unix_timestamp(self.created_at)
        derived_from = ", derived_from=..." if self.derived_from is not None else ""
        tag = f", tag='{self.tag}'" if self.tag is not None else ""
        return (
            f"SupplementaryFile(file_name='{self.file_name}', "
            f"file_format='{self.file_format}',"
            f" created_at='{created_at}'{tag}{derived_from})"
        )

    def download(self, path: str) -> str:
        """
        Args:
            path: Can be a directory or a file path.

        Returns:
            The relative path where the data was downloaded

        Examples:
            >>> supplementary_file.download('./')
        """
        if path.endswith(os.sep):  # if it looks like a directory
            path = join_paths(path, self.file_name)

        copy_file(
            self.file_location, path, s3_client=self._s3_client_manager.get_client()
        )
        return path


class Dataset(VersionBase):
    """
    Class that represents a dataset

    Attributes:
        dataset_id: Dataset Identifier
        omixatlas_id: OmixAtlas ID (e.g. `'1673411159486'`)
        data_type: Data type (e.g. `Single Cell RNASeq`)
        data_format: Storage format for the data (e.g. `h5ad`, `gct`)
        version_id: Unique version identifier
        study_id: Identifier for the parent study
        last_modified_at: Unix timestamp (ms) for when the dataset was last modified
    """

    # Applicable to both Dataset & DatasetVersion
    dataset_id: str
    omixatlas_id: str
    data_type: str
    version_id: str
    data_format: str
    created_at: int
    # (not included in docs)
    metadata_location: str
    data_location: str

    # Only applicable to Dataset
    study_id: Optional[str]
    last_modified_at: int

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.study_id: Optional[str] = kwargs.get("study_id")
        self.last_modified_at: int = kwargs.get("last_modified_at")

        self._s3_client_manager = S3ClientManager(self.omixatlas_id)

    def __repr__(self) -> str:
        modified_at = humanize_unix_timestamp(self.last_modified_at)
        if self.study_id is None:
            return (
                f"Dataset(dataset_id='{self.dataset_id}', data_type='{self.data_type}',"
                f" last_modified_at='{modified_at}', data_format='{self.data_format}')"
            )
        return (
            f"Dataset(dataset_id='{self.dataset_id}', data_type='{self.data_type}',"
            f" last_modified_at='{modified_at}', data_format={self.data_format},"
            f" study_id='{self.study_id}')"
        )


# TODO: Check for anndata > 0.8.0

# TODO: Params for validation?


class DatasetVersion(VersionBase):
    """
    Class that represents an immutable version of a dataset

    Attributes:
        dataset_id: Dataset Identifier
        omixatlas_id: OmixAtlas ID (e.g. `'1673411159486'`)
        data_type: Data type (e.g. `Single Cell RNASeq`)
        data_format: Storage format for the data (e.g. `h5ad`, `gct`)
        version_id: Unique version identifier
        created_at: Unix timestamp (ms) for when this version was created
    """

    # Applicable to both Dataset & DatasetVersion
    dataset_id: str
    omixatlas_id: str
    data_type: str
    version_id: str
    data_format: str
    created_at: int
    # (not included in docs)
    metadata_location: str
    data_location: str

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self._s3_client_manager = S3ClientManager(self.omixatlas_id)

    def __repr__(self) -> str:
        return (
            f"DatasetVersion(version_id='{self.version_id}',"
            f" created_at='{humanize_unix_timestamp(self.created_at)}')"
        )


def is_gctoo(obj: Any) -> bool:
    """
    Checks if obj is an instance of GCToo without
    requiring cmapPy to be present as a dependency
    """
    try:
        from cmapPy.pandasGEXpress.GCToo import GCToo

        return isinstance(obj, GCToo)
    except ImportError:
        return False


def is_anndata(obj: Any) -> bool:
    try:
        from anndata import AnnData

        return isinstance(obj, AnnData)
    except ImportError:
        return False


def extract_file_extension(path: str):
    """
    Extracts the file extension from the given file path.

    Args:
        path (str): The file path from which to extract the file extension.

    Returns:
        str: The file extension including the leading period (e.g. '.txt').

    Raises:
        ValueError: If the file path is either an empty string, a directory path,
                    or does not contain a file extension.
    """
    if not path or path.endswith("/") or path.endswith("\\"):
        raise ValueError("The file path is either an empty string or a directory path.")

    base_name = os.path.basename(path)
    if "." not in base_name or base_name.startswith("."):
        raise ValueError("The file path does not contain a file extension.")

    # Handle multi-part extensions like '.tar.gz'
    parts = base_name.split(".")
    if len(parts) > 2:
        return "." + ".".join(parts[1:])
    else:
        return os.path.splitext(base_name)[1]
