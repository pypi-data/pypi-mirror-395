import os
from os.path import join as join_paths
from typing import Tuple, Optional, Union, List, TYPE_CHECKING, Callable
import json
import urllib
import tempfile

from polly.auth import Polly, UnauthorizedException
from polly.session import PollySession
from polly.s3_utils import copy_file
from polly.errors import AccessDeniedError
from polly.threading_utils import for_each_threaded
from polly_services.dataset import (
    validate_user_defined_id,
    handle_errors_or_warnings,
    S3ClientManager,
    is_supported_format,
    infer_file_type,
    extract_extension_from_s3_uri,
    extract_file_extension,
    Dataset,
    DatasetVersion,
    SupplementaryFile,
    is_gctoo,
    is_anndata,
)

if TYPE_CHECKING:
    from cmapPy.pandasGEXpress.GCToo import GCToo
    from anndata import AnnData


class Catalog:
    """
    Attributes:
        omixatlas_id: Omixatlas ID
    """

    omixatlas_id: str

    def __init__(self, omixatlas_id: str) -> None:
        """
        Initializes the internal data Catalog for a given OmixAtlas

        Args:
            omixatlas_id: The identifier for the OmixAtlas

        Examples:
            >>> catalog = Catalog(omixatlas_id='9')
        """
        if Polly.default_session is None:
            raise UnauthorizedException()

        # Instead of storing Polly.default_session directly as a private attribute
        # I'm creating a function that returns Polly.default_session
        # This ensures that any changes to default_session (e.g. token update)
        # are incorporated by an existing catalog object
        self._get_session: Callable[[], PollySession] = lambda: Polly.default_session

        self.omixatlas_id = omixatlas_id
        self._s3_client_manager = S3ClientManager(self.omixatlas_id)

    def _upload_data(
        self,
        dataset_id: str,
        data: Union[str, "GCToo", "AnnData"],
        data_format: Optional[str] = None,
    ) -> Tuple[str, str]:
        client = self._s3_client_manager.get_client()
        bucket, prefix = self._s3_client_manager.get_upload_path()

        dest_path_without_extension = "s3://" + join_paths(
            bucket, prefix, f"v2/{dataset_id}/{dataset_id}"
        )

        if isinstance(data, str) and data.startswith("s3://"):
            # user is passing s3 uri directly
            if data_format is None:
                raise ValueError(
                    "'data_format' is a required field when passing S3 uri directly"
                )
            return data, data_format

        if isinstance(data, str) and not is_supported_format(data):
            # couldn't infer format
            if data_format is None:
                raise ValueError(
                    "Couldn't infer 'data_format', please pass it directly"
                )
            s3_uri = dest_path_without_extension + extract_file_extension(data)
            s3_uri_with_version = copy_file(data, s3_uri, s3_client=client)
            return s3_uri_with_version, data_format

        if isinstance(data, str):
            # try to infer file format
            file_type, extension = infer_file_type(data)
            s3_uri = dest_path_without_extension + extension
            s3_uri_with_version = copy_file(data, s3_uri, s3_client=client)
            return s3_uri_with_version, file_type

        if is_gctoo(data):
            extension = ".gct"
            import cmapPy.pandasGEXpress.write_gct as wg

            with tempfile.NamedTemporaryFile("w", suffix=extension, delete=True) as f:
                # Using a context manager to handle the temporary file
                tmp_file_path = f.name
                wg.write(data, tmp_file_path)
                s3_uri_with_version = copy_file(
                    tmp_file_path,
                    dest_path_without_extension + extension,
                    s3_client=client,
                )
                return s3_uri_with_version, "gct"

        if is_anndata(data):
            extension = ".h5ad"
            with tempfile.NamedTemporaryFile("w", suffix=extension, delete=True) as f:
                # Using a context manager to handle the temporary file
                tmp_file_path = f.name
                data.write(tmp_file_path, compression="lzf")
                s3_uri_with_version = copy_file(
                    tmp_file_path,
                    dest_path_without_extension + extension,
                    s3_client=client,
                )
                return s3_uri_with_version, "h5ad"

        raise ValueError(f"Unsupported type ({type(data)}) for parameter 'data'")

    # TODO: support passing Path objects directly in data
    def create_dataset(
        self,
        dataset_id: str,
        data_type: str,
        data: Union[str, "GCToo", "AnnData"],
        metadata: dict,
        *,
        ingestion_params: Optional[dict] = None,
        other_params: Optional[dict] = None,
        **kwargs,
    ) -> Dataset:
        """
        Creates a new dataset in the catalog.

        Raises an error if a dataset with the same ID already exists

        Args:
            dataset_id: The unique identifier for the dataset.
            data_type: The type of data being uploaded (e.g. `Single Cell RNASeq`).
            data: The data, either as a file or as an AnnData or GCToo object
            metadata: The metadata dictionary

        Returns:
            Newly created dataset.

        Examples:
            >>> new_dataset = catalog.create_dataset(
            ...     dataset_id='GSE123',
            ...     data_type='Bulk RNAseq',
            ...     data='path/to/data/file.gct',
            ...     metadata={'description': 'New dataset description'}
            ... )
        """

        validate_user_defined_id(dataset_id, "dataset_id")

        self._check_s3_write_access()
        s3_uri_with_version, file_type = self._upload_data(
            dataset_id, data, data_format=kwargs.pop("data_format", None)
        )

        other_params = other_params or {}
        payload = {
            "data": {
                "type": "datasets",
                "id": dataset_id,
                "attributes": {
                    "data_type": data_type,
                    "metadata": metadata,
                    "data_s3_uri": s3_uri_with_version,
                    "data_format": file_type,
                    **kwargs,
                },
            },
            "meta": {"ingestion_params": ingestion_params, **other_params},
        }
        resp = self._get_session().post(
            f"{self._get_session().discover_url}/repositories/{self.omixatlas_id}/datasets",
            json=payload,
        )
        handle_errors_or_warnings(resp)
        return Dataset(**resp.json()["data"]["attributes"])

    def get_dataset(self, dataset_id: str) -> Dataset:
        """
        Retrieves the dataset with the given dataset_id if it exists

        This function doesn't download the underlying data, it only returns a reference to it

        Args:
            dataset_id: The unique identifier for the dataset to retrieve.

        Returns:
            An object representing the retrieved dataset.

        Examples:
            >>> dataset = catalog.get_dataset(dataset_id='GSE123')
            >>> dataset
            Dataset(dataset_id='GSE123', data_type='Bulk RNAseq', last_modified_at='2023-11-07 15:42:40', data_format='gct')
        """
        resp = self._get_session().get(
            f"{self._get_session().discover_url}/repositories/{self.omixatlas_id}/datasets/{dataset_id}",
        )
        handle_errors_or_warnings(resp)
        data = resp.json()["data"]
        dataset_id = data["id"]
        data["attributes"].pop("dataset_id", None)
        return Dataset(dataset_id=dataset_id, **data["attributes"])

    def list_datasets(
        self, *, limit: Optional[int] = None, prefetch_metadata: bool = False
    ) -> List[Dataset]:
        """
        Retrieves the complete list of datasets in the catalog.

        If `prefetch_metadata` is `True` the metadata json is downloaded in advance
        using multiple threads. This makes the `dataset.metadata()` function call
        return instantly. This is useful for bulk metadata download.

        Args:
            limit: Limits the number of datasets that are returned
            prefetch_metadata: Prefetches metadata for each dataset

        Returns:
            A list of Dataset instances.

        Examples:
            >>> datasets = catalog.list_datasets()
            >>> len(datasets)
            148
        """
        dataset_dicts = []

        next_link = f"/repositories/{self.omixatlas_id}/datasets"
        if limit is not None:
            # A bit hacky, `page[size]` is not the same as `limit`
            # This may not work for large values of `limit`
            next_link = f"/repositories/{self.omixatlas_id}/datasets?page[size]={limit}"

        while True:  # loop over pages
            resp = self._get_session().get(
                f"{self._get_session().discover_url}{next_link}"
            )
            handle_errors_or_warnings(resp)
            resp_dict = resp.json()
            dataset_dicts.extend(resp.json()["data"])

            if limit is not None and len(dataset_dicts) >= limit:
                dataset_dicts = dataset_dicts[:limit]
                break

            if "links" not in resp_dict or "next" not in resp_dict["links"]:
                break

            if resp_dict["links"]["next"] is None:
                break

            next_link = resp_dict["links"]["next"]

        datasets = []
        for dataset_dict in dataset_dicts:
            dataset_id = dataset_dict["id"]
            dataset_dict["attributes"].pop("dataset_id", None)
            datasets.append(
                Dataset(dataset_id=dataset_id, **dataset_dict["attributes"])
            )

        if prefetch_metadata:
            for_each_threaded(
                datasets, lambda d: d.metadata(), max_workers=20, verbose=True
            )

        return datasets

    def update_dataset(
        self,
        dataset_id: str,
        data_type: Optional[str] = None,
        metadata: Optional[dict] = None,
        data: Union[str, "GCToo", "AnnData", None] = None,
        *,
        ingestion_params: Optional[dict] = None,
        other_params: Optional[dict] = None,
        **kwargs,
    ) -> Dataset:
        """
        Updates one or more attributes of a dataset.

        Every update creates a new version of the dataset.

        Args:
            dataset_id: Identifier for the dataset.
            data_type: The type of data being uploaded (e.g. `Single Cell RNASeq`).
            data: The data, either as a file or as an AnnData or GCToo object
            metadata: The metadata dictionary

        Returns:
            The updated dataset

        Examples:
            >>> updated_dataset = catalog.update_dataset(
            ...     dataset_id='GSE123',
            ...     metadata={'new': 'metadata'}
            ... )
        """
        attrs = {**kwargs}

        if data is not None:
            self._check_s3_write_access()
            s3_uri_with_version, file_type = self._upload_data(
                dataset_id, data, data_format=kwargs.pop("data_format", None)
            )
            attrs["data_s3_uri"] = s3_uri_with_version
            attrs["data_format"] = file_type

        if data_type is not None:
            attrs["data_type"] = data_type

        if metadata is not None:
            attrs["metadata"] = metadata

        other_params = other_params or {}
        payload = {
            "data": {
                "type": "datasets",
                "id": dataset_id,
                "attributes": attrs,
            },
            "meta": {"ingestion_params": ingestion_params, **other_params},
        }

        if not attrs:
            raise ValueError("Nothing to update")

        resp = self._get_session().patch(
            f"{self._get_session().discover_url}/repositories/{self.omixatlas_id}/datasets/{dataset_id}",
            json=payload,
        )

        handle_errors_or_warnings(resp)
        data = resp.json()["data"]
        dataset_id = data["id"]
        data["attributes"].pop("dataset_id", None)
        return Dataset(dataset_id=dataset_id, **data["attributes"])

    def delete_dataset(self, dataset_id: str, **kwargs) -> None:
        """
        Performs a soft deletion of the dataset

        Args:
            dataset_id: Identifier for the dataset to be deleted.

        Examples:
            >>> catalog.delete_dataset(dataset_id='GSE123')
        """
        params = urllib.parse.quote(json.dumps(kwargs))
        resp = self._get_session().delete(
            f"{self._get_session().discover_url}/repositories/{self.omixatlas_id}/datasets/{dataset_id}?params={params}",
        )
        handle_errors_or_warnings(resp)

    def set_parent_study(
        self,
        dataset_id: str,
        study_id: Optional[str],
        *,
        ingestion_params: Optional[dict] = None,
        other_params: Optional[dict] = None,
        **kwargs,
    ) -> None:
        """
        Adds a dataset to a study. The study_id can be any arbitrary string.

        To remove the dataset from the study, set the study_id to None.

        Args:
            dataset_id: Identifier for the dataset
            study_id: User defined ID for the parent study

        Examples:
            Add dataset to a study
            >>> catalog.set_parent_study(dataset_id='GSE123', study_id='PMID123')

            Remove the dataset from the study
            >>> catalog.set_parent_study(dataset_id='GSE123', study_id=None)
        """
        if study_id is not None:
            validate_user_defined_id(study_id, "study_id")

        other_params = other_params or {}
        payload = {
            "data": {
                "type": "datasets",
                "id": dataset_id,
                "attributes": {"study_id": study_id, **kwargs},
            },
            "meta": {"ingestion_params": ingestion_params, **other_params},
        }

        resp = self._get_session().patch(
            f"{self._get_session().discover_url}/repositories/{self.omixatlas_id}/datasets/{dataset_id}",
            json=payload,
        )

        handle_errors_or_warnings(resp)

    def list_datasets_in_study(self, study_id: str) -> List[str]:
        """
        Retrieves a list of datasets associated with a specific study.

        Args:
            study_id: Identifier for the study.

        Returns:
            A list of dataset IDs that are part of the study.

        Examples:
            >>> catalog.list_datasets_in_study(study_id='PMID123')
            ['GSE123', 'GSE123_raw']

        """
        resp = self._get_session().get(
            f"{self._get_session().discover_url}/repositories/{self.omixatlas_id}/studies/{study_id}",
        )

        handle_errors_or_warnings(resp)
        items = resp.json()["relationships"]["datasets"]["data"]
        return [item["id"] for item in items]

    def list_studies(self) -> List[str]:
        """
        Retrieves a list of all studies in the catalog.

        Returns:
            A list of study IDs.

        Examples:
            >>> study_ids = catalog.list_studies()
            >>> study_ids
            ['PMID123', 'PMID125', 'SCP300']
        """
        resp = self._get_session().get(
            f"{self._get_session().discover_url}/repositories/{self.omixatlas_id}/studies"
        )
        handle_errors_or_warnings(resp)
        studies = resp.json()["data"]
        return [study["id"] for study in studies]

    def get_version(self, dataset_id: str, version_id: str) -> DatasetVersion:
        """
        Retrieves a specific version of a dataset.

        You can also use this to retrieve a version that may have been deleted.

        Args:
            dataset_id (str): Identifier for the dataset.
            version_id (str): Identifier for the dataset version.

        Returns:
            An object representing the dataset version.

        Examples:
            >>> catalog.get_version(dataset_id='GSE123', version_id='<uuid>')
            DatasetVersion(version_id='<uuid>', created_at='2023-10-29 20:41:15')
        """
        resp = self._get_session().get(
            f"{self._get_session().discover_url}/repositories/{self.omixatlas_id}/datasets/{dataset_id}/versions/{version_id}",
        )
        handle_errors_or_warnings(resp)
        data = resp.json()["data"]
        version_id = data["id"]
        data["attributes"].pop("version_id", None)
        return DatasetVersion(version_id=version_id, **data["attributes"])

    def list_versions(
        self, dataset_id: str, *, include_deleted: bool = False
    ) -> List[DatasetVersion]:
        """
        Lists dataset versions, optionally including deleted ones.

        Args:
            dataset_id: Identifier for the dataset.
            include_deleted: If set to True, includes previously deleted versions

        Returns:
            List of dataset versions.
        """
        resp = self._get_session().get(
            f"{self._get_session().discover_url}/repositories/{self.omixatlas_id}/"
            f"datasets/{dataset_id}/versions?include_deleted={include_deleted}"
        )
        handle_errors_or_warnings(resp)
        data = resp.json()["data"]
        versions = []
        for version_dict in data:
            version_id = version_dict["id"]
            version_dict["attributes"].pop("version_id", None)
            versions.append(
                DatasetVersion(version_id=version_id, **version_dict["attributes"])
            )
        return versions

    def rollback(
        self,
        dataset_id: str,
        version_id: str,
        *,
        ingestion_params: Optional[dict] = None,
        other_params: Optional[dict] = None,
        **kwargs,
    ) -> Dataset:
        """
        Reverts a dataset to a specified older version.

        This function updates the dataset's `data` and `metadata` to match the specified
        version. The version ID itself is not restored.

        Args:
            dataset_id: Identifier for the dataset.
            version_id: Identifier for the version to roll back to.

        Returns:
            The dataset instance with the rolled back data and metadata.
        """
        version = self.get_version(dataset_id, version_id)

        if dataset_id in self:
            return self.update_dataset(
                dataset_id,
                data_type=version.data_type,
                metadata=version.metadata(),
                data=version.data_location,
                data_format=version.data_format,  # important: don't try to infer format
                ingestion_params=ingestion_params,
                other_params=other_params,
                **kwargs,
            )
        else:
            return self.create_dataset(
                dataset_id,
                data_type=version.data_type,
                data=version.data_location,
                metadata=version.metadata(),
                data_format=version.data_format,  # important: don't try to infer format
                ingestion_params=ingestion_params,
                other_params=other_params,
                **kwargs,
            )

    def attach_file(
        self,
        dataset_id: str,
        path: str,
        *,
        tag: Optional[str] = None,
        source_version_id: Optional[str] = None,
        file_name: Optional[str] = None,
        **kwargs: dict,
    ) -> SupplementaryFile:
        """
        Attach a supplementary file to a dataset.

        If a file with the same name already exists it is overwritten.

        Optionally, you can link the supplementary file to a specific version of a dataset.
        This will auto-delete the file if the underlying data for the dataset changes.
        Note that changes to `metadata` or `data_type` will not auto-delete the file.

        _Added in polly-python v1.3_

        Args:
            dataset_id: Identifier for the dataset.
            path: Local path of the file.
            tag: An optional tag for the supplementary file.
            source_version_id: The version_id of the source dataset.
            file_name: The name of the file. If not provided the file name will be
              inferred from the path.

        Returns:
            A SupplementaryFile instance representing the attached file.
        """
        self._check_s3_write_access()

        # user is passing s3 uri directly
        if path.startswith("s3://"):
            err_msg = (
                "The 'file_format' and 'file_name' need to be"
                " explicitly provided if path is an s3 uri"
            )

            if "file_format" not in kwargs:
                raise ValueError(err_msg)
            if file_name is None:
                raise ValueError(err_msg)

            file_format = kwargs["file_format"]
            s3_uri_with_version = path

        else:
            file_name = file_name or os.path.basename(path)
            file_format = kwargs.get("file_format")

            if file_format is None and is_supported_format(path):
                file_format, _ = infer_file_type(path)
            elif file_format is None:
                raise ValueError(
                    "Could not infer the file format, please provide it"
                    " explicitly using the 'file_format' parameter"
                )

            client = self._s3_client_manager.get_client()
            bucket, prefix = self._s3_client_manager.get_upload_path()
            dest_path = "s3://" + join_paths(
                bucket, prefix, f"v2/{dataset_id}/.sfiles/{file_name}"
            )
            s3_uri_with_version = copy_file(path, dest_path, s3_client=client)

        payload = {
            "data": {
                "type": "supplementary_files",
                "attributes": {
                    "file_name": file_name,
                    "file_s3_uri": s3_uri_with_version,
                    "file_format": file_format,
                    "tag": tag,
                    "source_version_id": source_version_id,
                    **kwargs,
                },
            }
        }

        resp = self._get_session().post(
            f"{self._get_session().discover_url}/repositories/{self.omixatlas_id}/datasets/{dataset_id}/supplementary_files",
            json=payload,
        )

        handle_errors_or_warnings(resp)

        data = resp.json()["data"]
        return SupplementaryFile(**data["attributes"])

    def get_file(self, dataset_id: str, file_name: str) -> SupplementaryFile:
        """
        Retrieves a supplementary file.

        _Added in polly-python v1.3_

        Args:
            dataset_id: Identifier for the dataset.
            file_name: Name of the file to retrieve.

        Returns:
            A SupplementaryFile instance.
        """
        sess = self._get_session()
        resp = sess.get(
            f"{sess.discover_url}/repositories/{self.omixatlas_id}/datasets/{dataset_id}"
            f"/supplementary_files/{file_name}"
        )
        handle_errors_or_warnings(resp)
        data = resp.json()["data"]
        return SupplementaryFile(**data["attributes"])

    def list_files(self, dataset_id: str) -> List[SupplementaryFile]:
        """
        Retrieves a list of all supplementary files attached to a dataset.

        _Added in polly-python v1.3_

        Args:
            dataset_id: Identifier for the dataset.

        Returns:
            A list of SupplementaryFile instances.
        """
        sess = self._get_session()
        resp = sess.get(
            f"{sess.discover_url}/repositories/{self.omixatlas_id}/datasets/{dataset_id}"
            f"/supplementary_files"
        )
        handle_errors_or_warnings(resp)
        data = resp.json()["data"]
        return [SupplementaryFile(**item["attributes"]) for item in data]

    def delete_file(self, dataset_id: str, file_name: str) -> None:
        """
        Deletes the supplementary file.

        _Added in polly-python v1.3_

        Args:
            dataset_id: Identifier for the dataset.
            file_name: File name
        """
        sess = self._get_session()
        resp = sess.delete(
            f"{sess.discover_url}/repositories/{self.omixatlas_id}/datasets/{dataset_id}"
            f"/supplementary_files/{file_name}"
        )
        handle_errors_or_warnings(resp)

    def _check_s3_write_access(self):
        access = self._s3_client_manager.get_access_level()

        if access is None:
            return

        if access == "read":
            raise AccessDeniedError(
                detail=(
                    "You don't have permission to write to"
                    f" omixatlas_id='{self.omixatlas_id}'. "
                    "\n\nRun `catalog.clear_token_cache()` before retrying"
                ),
            )

    def clear_token_cache(self) -> None:
        """
        Clears cached S3 tokens
        """
        self._s3_client_manager.clear()

    def trigger_ingestion(
        self,
        dataset_id: str,
        *,
        ingestion_params: Optional[dict] = None,
        other_params: Optional[dict] = None,
    ):
        """
        A helper function to manually trigger ingestion for a dataset

        Args:
            dataset_id: Identifier for the dataset.
        """
        other_params = other_params or {}
        payload = {
            "data": {
                "type": "datasets",
                "id": dataset_id,
                "attributes": {},
            },
            "meta": {"ingestion_params": ingestion_params, **other_params},
        }

        resp = self._get_session().patch(
            f"{self._get_session().discover_url}/repositories/{self.omixatlas_id}/datasets/{dataset_id}",
            json=payload,
        )
        handle_errors_or_warnings(resp)
        return resp.json()

    def __contains__(self, dataset_id: str) -> bool:
        """
        Check if a dataset with the given dataset_id exists in the catalog.

        Args:
            dataset_id: Identifier for the dataset.

        Returns:
            True if the dataset exists, False otherwise.
        """
        resp = self._get_session().get(
            f"{self._get_session().discover_url}/repositories/{self.omixatlas_id}/datasets/{dataset_id}"
        )
        if resp.status_code == 404:
            return False
        handle_errors_or_warnings(resp)
        return True

    def __repr__(self):
        return f"Catalog(omixatlas_id='{self.omixatlas_id}')"


def copy_dataset(
    src_omixatlas_id: str,
    src_dataset_id: str,
    dest_omixatlas_id: str,
    dest_dataset_id: str,
    overwrite: bool = False,
    *,
    ingestion_params: Optional[dict] = None,
    other_params: Optional[dict] = None,
    **kwargs,
) -> Dataset:
    """
    Copies a dataset from one omixatlas catalog to another.

    Any supplementary files attached to the dataset are also copied.

    The transfer happens remotely, the data is not downloaded locally.

    Args:
        src_omixatlas_id: The source omixatlas_id
        src_dataset_id: The source dataset_id
        dest_omixatlas_id: The destination omixatlas_id
        dest_dataset_id: The destination dataset_id
        overwrite: If True, overwrites the destination dataset if it already exists

    Returns:
        The dataset in the destination catalog.

    Examples:
        >>> from polly.data_management import copy_dataset
        >>> copy_dataset('9', 'GSE123', '17', 'GSE123_copy')
    """
    validate_user_defined_id(dest_dataset_id, "dest_dataset_id")

    print("Copying dataset")
    src_catalog = Catalog(src_omixatlas_id)
    src_dataset = src_catalog.get_dataset(src_dataset_id)

    if src_omixatlas_id == dest_omixatlas_id:
        # when copying within the same catalog
        # the destination dataset points to the same file as source dataset
        dest_dataset = _copy_dataset(
            src_dataset,
            Catalog(dest_omixatlas_id),
            dest_dataset_id,
            dest_location=src_dataset.data_location,  # same as src location
            overwrite=overwrite,
            ingestion_params=ingestion_params,
            other_params=other_params,
            **kwargs,
        )
        print("Copying supplementary files")
        for file in src_catalog.list_files(src_dataset.dataset_id):
            _copy_supplementary_file(
                src_omixatlas_id, src_dataset, dest_omixatlas_id, dest_dataset, file
            )
        return dest_dataset

    client_manager = S3ClientManager(src_omixatlas_id, dest_omixatlas_id)
    bucket, prefix = client_manager.get_upload_path()

    dest_path_without_extension = "s3://" + join_paths(
        bucket, prefix, f"v2/{dest_dataset_id}/{dest_dataset_id}"
    )
    extension = extract_extension_from_s3_uri(src_dataset.data_location)

    s3_uri_with_version = copy_file(
        src_dataset.data_location,
        dest_path_without_extension + extension,
        s3_client=client_manager.get_client(),
    )
    dest_catalog = Catalog(dest_omixatlas_id)

    dest_dataset = _copy_dataset(
        src_dataset,
        dest_catalog,
        dest_dataset_id,
        s3_uri_with_version,
        overwrite,
        ingestion_params=ingestion_params,
        other_params=other_params,
        **kwargs,
    )
    print("Copying supplementary files")
    for file in src_catalog.list_files(src_dataset.dataset_id):
        _copy_supplementary_file(
            src_omixatlas_id, src_dataset, dest_omixatlas_id, dest_dataset, file
        )
    return dest_dataset


def _copy_dataset(
    src_dataset: Dataset,
    dest_catalog: Catalog,
    dest_dataset_id: str,
    dest_location: str,
    overwrite: bool,
    *,
    ingestion_params: Optional[dict] = None,
    other_params: Optional[dict] = None,
    **kwargs,
) -> Dataset:
    if overwrite and dest_dataset_id in dest_catalog:
        return dest_catalog.update_dataset(
            dest_dataset_id,
            src_dataset.data_type,
            metadata=src_dataset.metadata(),
            data=dest_location,
            data_format=src_dataset.data_format,
            study_id=src_dataset.study_id,
            ingestion_params=ingestion_params,
            other_params=other_params,
            **kwargs,
        )

    return dest_catalog.create_dataset(
        dest_dataset_id,
        src_dataset.data_type,
        data=dest_location,
        metadata=src_dataset.metadata(),
        data_format=src_dataset.data_format,
        study_id=src_dataset.study_id,
        ingestion_params=ingestion_params,
        other_params=other_params,
        **kwargs,
    )


def _copy_supplementary_file(
    src_catalog_id: str,
    src_dataset: Dataset,
    dest_catalog_id: Catalog,
    dest_dataset: Dataset,
    file: SupplementaryFile,
) -> SupplementaryFile:
    if src_catalog_id == dest_catalog_id:
        # pass s3 uri directly
        return Catalog(dest_catalog_id).attach_file(
            dest_dataset.dataset_id,
            path=file.file_location,
            tag=file.tag,
            file_name=file.file_name,
            file_format=file.file_format,
            source_version_id=(
                dest_dataset.version_id if file.derived_from is not None else None
            ),
        )

    client_manager = S3ClientManager(src_catalog_id, dest_catalog_id)
    bucket, prefix = client_manager.get_upload_path()

    dest_s3_uri = "s3://" + join_paths(
        bucket, prefix, f"v2/{dest_dataset.dataset_id}/.sfiles/{file.file_name}"
    )

    # Copy the file to the destination S3 URI
    copy_file(file.file_location, dest_s3_uri, s3_client=client_manager.get_client())

    # Attach the copied file to the destination dataset
    return Catalog(dest_catalog_id).attach_file(
        dest_dataset.dataset_id,
        path=dest_s3_uri,
        file_name=file.file_name,
        file_format=file.file_format,
        tag=file.tag,
        source_version_id=(
            dest_dataset.version_id if file.derived_from is not None else None
        ),
    )
