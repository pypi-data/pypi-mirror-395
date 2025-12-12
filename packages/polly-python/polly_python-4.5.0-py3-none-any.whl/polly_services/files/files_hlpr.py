from polly.errors import paramException
from polly import helpers
from polly_services import polly_services_hlpr
import json
from polly import constants as const
from functools import lru_cache
import pandas as pd
import copy
import os
import warnings
from pathlib import Path
from tqdm import tqdm
import pathlib
from tempfile import TemporaryDirectory as TempDir
import requests
from cryptography.fernet import Fernet
from polly.errors import error_handler, ValidationError
import boto3
from boto3.s3.transfer import TransferConfig
from boto3.exceptions import S3UploadFailedError
import polly.http_response_codes as http_codes


dataset_level_metadata_files_not_uploaded = []
data_files_whose_metadata_failed_validation = []


def reset_global_variables_with_validation_results():
    """
    Reset Global variables storing value to default after
    add and update datasets are complete
    """
    global dataset_level_metadata_files_not_uploaded
    dataset_level_metadata_files_not_uploaded = []

    global data_files_whose_metadata_failed_validation
    data_files_whose_metadata_failed_validation = []


def parameter_check_for_add_dataset(
    repo_id: int, source_folder_path: dict, priority: str
):
    """_summary_

    Args:
        repo_id (int): _description_
        source_folder_path (dict): _description_
        priority (str): _description_
    """
    try:
        polly_services_hlpr.parameter_check_for_repo_id(repo_id)
        data_metadata_parameter_check(source_folder_path)
        data_metadata_file_ext_check(source_folder_path)
        check_data_metadata_file_path(source_folder_path)
        parameter_check_for_priority(priority)
    except Exception as err:
        raise err


def parameter_check_for_update_dataset(
    repo_id: int, source_folder_path: dict, priority: str, file_mapping: dict
):
    """_summary_

    Args:
        repo_id (int): _description_
        source_folder_path (dict): _description_
        priority (str): _description_
        file_mapping(list)
    """
    try:
        polly_services_hlpr.parameter_check_for_repo_id(repo_id)
        data_metadata_parameter_check(source_folder_path, update=True)
        data_metadata_file_ext_check(source_folder_path)
        check_data_metadata_file_path(source_folder_path)
        parameter_check_for_priority(priority)
        check_file_mapping(file_mapping)
    except Exception as err:
        raise err


def check_file_mapping(file_mapping: dict):
    """_summary_

    Args:
        file_mapping (list): _description_
    """
    if not isinstance(file_mapping, dict):
        raise paramException(
            title="Param Error",
            detail="file_mapping parameter should be dictionary, where each entry  "
            + "is a should be a mapping of dataset_file_name & dataset_id {dataset_file_name: dataset_id}.",
        )

    # cannot put dummy entry -> or the dummy entry will start getting used in the code
    # so no need to check this -> will need to handle this case where file_mapping list is used
    # for item in file_mapping:
    #     if not isinstance(item, dict):
    #         raise paramException(
    #             title="Param Error",
    #             detail=f"{item} is not a valid entry in the file_mapping list, "
    #             + "each entry is a dictionary containing mapping of {dataset_file_name: dataset_id}. ",
    #         )


def create_file_list(source_folder_path: dict):
    """Create file list for both data and metadata files

    Args:
        source_folder_path (dict): _description_
    """
    data_source_folder_path = source_folder_path.get("data", "")
    metadata_source_folder_path = source_folder_path.get("metadata", "")
    metadata_file_list = []
    if metadata_source_folder_path:
        metadata_file_list = metadata_files_for_upload(metadata_source_folder_path)

    data_file_list = []
    if data_source_folder_path:
        data_file_list = data_files_for_upload(data_source_folder_path)
    return data_file_list, metadata_file_list


def get_session_tokens(polly_session, repo_id: str, destination_folder_path="") -> dict:
    """
    Get the upload session tokens for uploading the files to s3
    Args:
        | repo_id(str/int): repo_name/repo_id for that Omixatlas
        | destination_folder_path(str): Destination folder structure in s3
    """
    # post request for upload urls
    payload = const.GETTING_UPLOAD_URLS_PAYLOAD
    payload["data"]["attributes"]["folder"] = destination_folder_path

    # post request
    repository_url = (
        f"{polly_session.discover_url}/repositories/{repo_id}/files?tokens=true"
    )
    resp = polly_session.session.post(repository_url, json=payload)
    error_handler(resp)
    if resp.status_code != const.OK:
        raise Exception(resp.text)
    else:
        response_data = resp.json()
        session_tokens = {}
        bucket_name = (
            response_data.get("data", {}).get("attributes", {}).get("bucket_name")
        )
        package_name = (
            response_data.get("data", {}).get("attributes", {}).get("package_name")
        )
        metadata_directory = (
            response_data.get("data", {})
            .get("attributes", {})
            .get("metadata_directory")
        )
        session_tokens["access_key"] = (
            response_data.get("data", {})
            .get("attributes", {})
            .get("tokens", {})
            .get("AccessKeyId")
        )
        session_tokens["secret_access_key"] = (
            response_data.get("data", {})
            .get("attributes", {})
            .get("tokens", {})
            .get("SecretAccessKey")
        )
        session_tokens["session_token"] = (
            response_data.get("data", {})
            .get("attributes", {})
            .get("tokens", {})
            .get("SessionToken")
        )
        session_tokens["expiration_stamp"] = (
            response_data.get("data", {})
            .get("attributes", {})
            .get("tokens", {})
            .get("Expiration")
        )
    return session_tokens, bucket_name, package_name, metadata_directory


# may need to refactor it a bit more -> while doing update datasets
# so that parts of this function -> can be used in both add and update datasets
def map_data_metadata_files(
    data_file_list: list, metadata_file_list: list, source_folder_path: dict
):
    """
    Map data and metadata file names and create a dict and return
    If for a data file name, there is not metadata file raise an error
    """
    # checking if folders are empty
    try:
        data_file_names_str = []
        # data_file_names_str = create_file_name_with_extension_list(data_file_list)
        data_file_names_str = data_file_list
        metadata_file_names_str = []
        # convert metadata file names from bytes to strings
        metadata_file_names_str = create_file_name_with_extension_list(
            metadata_file_list, file_ext_req=False
        )
        (
            data_metadata_mapping_dict,
            unmapped_data_file_names,
            unmapped_metadata_file_names,
        ) = data_metadata_file_dict(metadata_file_names_str, data_file_names_str)

        final_data_metadata_mapping_dict = data_metadata_file_mapping_conditions(
            unmapped_data_file_names,
            unmapped_metadata_file_names,
            data_metadata_mapping_dict,
        )
        return final_data_metadata_mapping_dict
    except Exception as err:
        raise err


def map_metadata_files_for_update(
    data_file_list: list, metadata_file_list: list, source_folder_path: dict
):
    """Map data and metadata files for update

    Args:
        source_folder_path (dict): _description_
    """
    try:
        data_file_names_str = []
        data_source_folder_path = source_folder_path.get("data", "")
        if data_source_folder_path:
            # data_file_names = helpers.get_files_in_dir(data_source_folder_path)
            data_file_names_str = create_file_name_with_extension_list(data_file_list)

        metadata_file_names_str = []
        metadata_source_folder_path = source_folder_path.get("metadata", "")
        if metadata_source_folder_path:
            # metadata_file_names = helpers.get_files_in_dir(metadata_source_folder_path)
            metadata_file_names_str = create_file_name_with_extension_list(
                metadata_file_list, file_ext_req=False
            )

        (
            data_metadata_mapping_dict,
            unmapped_data_file_names,
            unmapped_metadata_file_names,
        ) = data_metadata_file_dict(metadata_file_names_str, data_file_names_str)

        return (
            data_metadata_mapping_dict,
            unmapped_data_file_names,
            unmapped_metadata_file_names,
        )
    except Exception as err:
        raise err


def metadata_files_for_upload(source_metadata_path: str) -> list:
    """Find List of all the metadata files to be uploaded

    Args:
        repo_id (str): Repo Id of the OmixAtlas
        source_metadata_path (str): metadata path for the files
        data_metadata_mapping (dict): dictionary containing the data metadata mapping

    Returns:
        list: List of metadata files to be uploaded
    """
    metadata_directory = os.fsencode(source_metadata_path)
    metadata_file_list = []
    for file in os.listdir(metadata_directory):
        if not isinstance(file, str):
            file = file.decode("utf-8")
        # skip hidden files
        # skip the validation_status.json
        if not file.startswith(".") and file != const.VALIDATION_STATUS_FILE_NAME:
            metadata_file_list.append(file)
    return metadata_file_list


# can above and below functions be merged into one
# see where its use it and try to merge
def create_file_name_with_extension_list(file_names: list, file_ext_req=True) -> list:
    """Decode the file name in bytes to str

    Args:
        data_file_names (list): data file name in bytes
    Returns:
        list: data file names in str
    """
    file_names_str = []
    # convert file names from bytes to strings
    # file name is kept with extension here
    for file in file_names:
        if not isinstance(file, str):
            file = file.decode("utf-8")
        if not file.startswith(".") and file != const.VALIDATION_STATUS_FILE_NAME:
            if not file_ext_req:
                file = pathlib.Path(file).stem
            file_names_str.append(file)
    return file_names_str


def data_files_for_upload(data_source_folder_path: str) -> list:
    """Gives the list of data files for upload

    Args:
        data_source_path (str): folder path containing all the data files

    Returns:
        list: List of data files for upload
    """
    data_directory = os.fsencode(data_source_folder_path)
    data_files_list = []
    for file in os.listdir(data_directory):
        if not isinstance(file, str):
            file = file.decode("utf-8")
        # skip hidden files
        if not file.startswith("."):
            data_files_list.append(file)
    return data_files_list


def map_data_metadata_files_after_validation(
    data_file_list: list, metadata_file_list: list
):
    """After files are validated, need to recreate data_metadata_mapping file
    In add datasets for every data_file -> there should be metadata_file

    Args:
        data_file_list (list): _description_
        metadata_file_list (list): _description_
    """
    metadata_file_names_without_ext = create_file_name_with_extension_list(
        metadata_file_list, file_ext_req=False
    )
    data_metadata_mapping_dict = {}
    for data_file in data_file_list:
        data_file_name = get_file_name_without_suffixes(data_file)
        # this check is only to verify that for a data_file_name
        # corresponding metadata_file exists
        if data_file_name in metadata_file_names_without_ext:
            # {<metadata_file_name>: <data_file_name_with_ext>}
            # data_file_name without extension and metadata_file_name without extension
            # are mandated to be same
            data_metadata_mapping_dict[data_file_name] = data_file

    return data_metadata_mapping_dict


def filter_files_after_dataset_lvl_validation(
    data_file_list: list,
    metadata_file_list: list,
    validation_dataset_lvl: dict,
    source_folder_path: dict,
    data_metadata_mapping: dict,
) -> list:
    """If validation is activated by the user, then filter

    Args:
        data_file_list (list): _description_
        metadata_file_list (list): _description_

    Returns:
        list: two seperate lists of filtered data files and filtered metadata files
    """
    validation_dataset_lvl_grouped = group_passed_and_failed_validation(
        validation_dataset_lvl
    )
    metadata_source_folder_path = source_folder_path.get("metadata", "")

    filtered_metadata_file_list = []
    # apply validation layer on metadata files
    filtered_metadata_file_list = apply_validation_on_metadata_files(
        metadata_file_list, metadata_source_folder_path, validation_dataset_lvl_grouped
    )
    filtered_data_file_list = []
    filtered_data_file_list = filter_data_files_whose_metadata_not_uploaded(
        data_file_list, data_metadata_mapping
    )
    return filtered_data_file_list, filtered_metadata_file_list


def group_passed_and_failed_validation(validation_dataset_lvl: dict) -> dict:
    """Group Dataset Level Metadata Files who have passed and who have failed validation

    Args:
        validation_dataset_lvl (dict): validation status of metadata file
    Returns:
        Dict -> containing two sets of files
        validation_passed_metadata_files: Metadata Files Passed Validation
        validation_failed_metadata_files: Metadata Files failed Validation
    """
    validation_dataset_lvl_grouped = {}
    validation_dataset_lvl_grouped["passed"] = []
    validation_dataset_lvl_grouped["failed"] = []
    for dataset_id, status_val_dict in validation_dataset_lvl.items():
        if status_val_dict["status"]:
            validation_dataset_lvl_grouped["passed"].append(
                status_val_dict["file_name"]
            )
        else:
            validation_dataset_lvl_grouped["failed"].append(
                status_val_dict["file_name"]
            )

    if validation_dataset_lvl_grouped["failed"]:
        print("\n")
        failed_validation_files = validation_dataset_lvl_grouped["failed"]
        warnings.formatwarning = lambda msg, *args, **kwargs: f"WARNING: {msg}\n"
        warnings.warn(
            f"These {failed_validation_files} file have failed validation. "
            + "These files will only be ingested if force_ingest key in metadata is set to True"
        )
    return validation_dataset_lvl_grouped


def apply_validation_on_metadata_files(
    metadata_file_list: list,
    metadata_path: str,
    validation_dataset_lvl_grouped: dict,
) -> list:
    """Apply Validation on Metadata Files
    Rules
    => The Files which have passed validation would included in final list
    => Files which have failed validation, if `force_ingest` flag for them is true
    Then they will be included in the final list

    Args:
        metadata_file_list (list): List of all the metadata Files

    Returns:
        list: Returns the list metadata files which will be uploaded
    """
    final_metadata_file_list = []
    for file in metadata_file_list:
        file_path = str(Path(metadata_path) / Path(os.fsdecode(file)))
        with open(file_path, "r") as file_to_upload:
            res_dict = json.load(file_to_upload)
            # checking if validate key is true or not in metadata
            # if validate key is true then the file name
            # should be in valid_dataset_level_files
            # If the file name is not in valid_dataset_level_files
            # then it should be have `force_ingest` set to true
            # if the both the conditions are False
            # Then the file will not be ingested
            validate_param = (
                res_dict.get("__index__", {})
                .get("validation_check", {})
                .get("dataset", {})
                .get("validate", "")
            )
            force_ingest = (
                res_dict.get("__index__", {})
                .get("validation_check", {})
                .get("dataset", {})
                .get("force_ingest", "")
            )
            if (
                validate_param
                and file in validation_dataset_lvl_grouped["failed"]
                and not force_ingest
            ):
                # skip this file for ingesting
                # if force ingest not true then file will be skipped
                continue
            else:
                # if validate_param == true and file not in valid_dataset_id and force_ingest == True
                # if validate_param == true and file in valid_dataset_id
                # if validate_param == false
                # In all these cases continue the ingestion process

                # pop out the file from invalid_dataset_level_files
                if file in validation_dataset_lvl_grouped["failed"] and force_ingest:
                    # this file has has not passed validation
                    # but it is force ingested by the user
                    validation_dataset_lvl_grouped["failed"].remove(file)

                # append the files which will be uploaded
                final_metadata_file_list.append(file)

    global dataset_level_metadata_files_not_uploaded

    dataset_level_metadata_files_not_uploaded = validation_dataset_lvl_grouped["failed"]
    return final_metadata_file_list


def filter_data_files_whose_metadata_not_uploaded(
    data_files_list: list, data_metadata_mapping: dict
) -> list:
    """Filter Data Files whose metadata Not Valid

    Args:
        data_files_list (list): all the data files

    Returns:
        list: list of data files which can be uploaded
    """

    # this means no metadata files were given by user
    # no mapping dict generated
    if not data_metadata_mapping:
        return data_files_list

    # used to filter data files as metadata and data file names same
    not_uploaded_metadata_file_names = []

    # construct a list with metadata file names without extension
    for metadata_file in dataset_level_metadata_files_not_uploaded:
        metadata_file_name = pathlib.Path(metadata_file).stem
        not_uploaded_metadata_file_names.append(metadata_file_name)

    dataset_whose_metadata_not_valid = []

    # construct list of dataset files whose metadata is not valid
    for metadata_file_name in not_uploaded_metadata_file_names:
        data_file_name = data_metadata_mapping[metadata_file_name]
        dataset_whose_metadata_not_valid.append(data_file_name)

    global data_files_whose_metadata_failed_validation
    data_files_whose_metadata_failed_validation = dataset_whose_metadata_not_valid
    final_data_files_list = []

    for file in data_files_list:
        if file not in dataset_whose_metadata_not_valid:
            final_data_files_list.append(file)

    return final_data_files_list


def data_metadata_file_mapping_conditions(
    unmapped_data_file_names: list,
    unmapped_metadata_file_names: list,
    data_metadata_mapping_dict: dict,
) -> dict:
    """Different conditions to check for data metadata mapping

    Args:
        unmapped_file_names (list): data file names which are not mapped
        metadata_file_names_str (list): metadata file names list
        data_metadata_mapping_dict (dict): dict of data metadata mapping

    Returns:
        dict: data_metadata mapping dict if conditions succeed
    """
    # data and metadata file names are unmapped
    if len(unmapped_data_file_names) > 0 and len(unmapped_metadata_file_names) > 0:
        raise paramException(
            title="Missing files",
            detail=f" No metadata for these data files {unmapped_data_file_names}. "
            + f"No data for these metadata files {unmapped_metadata_file_names}. "
            + "Please add the relevant files or remove them.",
        )
    elif len(unmapped_data_file_names) > 0:
        raise paramException(
            title="Missing files",
            detail=f" No metadata for these data files {unmapped_data_file_names}"
            + ". Please add the relevant files or remove them.",
        )
    elif len(unmapped_metadata_file_names) > 0:
        raise paramException(
            title="Missing files",
            detail=f"No data for these metadata files {unmapped_metadata_file_names}"
            + ". Please add the relevant files or remove them.",
        )
    else:
        return data_metadata_mapping_dict


def data_metadata_file_dict(
    metadata_file_names_str: list, data_file_names_str: list
) -> list:
    """Construct data metadata file name dict and also return list of files which are unmapped
    Convention Followed in naming -> Metadata and Data File Name -> Will always be same
    Extension will be different -> Name always same

    Args:
        metadata_file_names_str (list): List of all metadata file names
        data_file_names_str (list): list of all data file names with extensions

    Returns:
        list: Returns list of mapped and unmapped files
    """
    # metadata file name -> key, data file name with extension -> value
    data_metadata_mapping_dict = {}
    unmapped_file_names = []
    for data_file in data_file_names_str:
        # data_file_name -> data_file with out ext
        data_file_name = get_file_name_without_suffixes(data_file)
        # check for matching data and metadata file name
        # convention for the system to know data and metadata mapping
        # also removing the metadata file from the list
        # which maps to data file
        # so as to return the unmapped metadata files at last if any
        if data_file_name in metadata_file_names_str:
            data_metadata_mapping_dict[data_file_name] = data_file
            # the metadata file whose pair data file exists
            # remove it from the metadata_file_names_str
            metadata_file_names_str.remove(data_file_name)
        else:
            # put the full data file name -> data file
            unmapped_file_names.append(data_file)

    # metadata_file_names_str -> only list of unmapped metadata file names without extension
    # unmapped_file_names -> unmapped full data file names
    return data_metadata_mapping_dict, unmapped_file_names, metadata_file_names_str


def parameter_check_for_priority(priority: str):
    if not isinstance(priority, str) or priority not in ["low", "medium", "high"]:
        raise paramException(
            title="Param Error",
            detail="`priority` should be a string. Only 3 values are allowed i.e. `low`, `medium`, `high`",
        )


def get_file_name_without_suffixes(data_file: str) -> str:
    """
    Returns just the file name without the suffixes.
    This functionality is written according to the rules of data file naming
    i) Data Files can have single extension
    ii) Data Files can have multiple extension
        => Multiword Extensions only possible if
        => Data file name has one main extension and one compressed extension
        => Examples are -> `.gct.bz`, `.h5ad.zip`
    iii) Data Files can have `.`'s in the names
    """
    file_format = get_file_format_constants()
    file_format_data = file_format.get("data", [])
    file_ext = pathlib.Path(data_file).suffixes
    if len(file_ext) == 1:
        # single word extension
        data_file_name = pathlib.Path(data_file).stem
    elif len(file_ext) > 1:
        # Either file with multi word extension
        # or `.`'s present in file name
        # check for multiword extensions
        compression_type_check = file_ext[-1]

        # compression types
        compression_types = copy.deepcopy(const.COMPRESSION_TYPES)
        # concatenating 2nd last and last word together to check
        # for multiword extension
        # pathlib.Path('my/library.tar.gz').suffixes
        # ['.tar', '.gz']

        if compression_type_check in compression_types:
            # multi word extension case
            # data_file -> file name with extension and compression format
            # file name with extension attached with `.`
            file_name_with_extension = pathlib.Path(data_file).stem

            # check if file_name_with_extension has an extension or is it a name
            # for ex
            # Case 1 => abc.gct.bz => after compression ext split
            # abc.gct => .gct => valid supported extension
            # Case 2 => abc.tar.gz => after compression ext split
            # abc.tar => .tar => valid compression type
            # Case 3 => abc.bcd.gz => Only zip as extension, no other extension

            file_main_ext = pathlib.Path(file_name_with_extension).suffix
            if file_main_ext in file_format_data:
                # file name
                data_file_name = pathlib.Path(file_name_with_extension).stem
            elif file_main_ext in compression_types:
                # second compression type
                data_file_name = pathlib.Path(file_name_with_extension).stem
            else:
                data_file_name = file_name_with_extension
        else:
            # single word extension with `.`'s in file which is accepted
            data_file_name = pathlib.Path(data_file).stem
    elif len(file_ext) == 0:
        # this case will never arise when we are passing files from add or
        # update function i.e. data and metadata files
        # Because this check is applied in the parameter check

        # this case will arise if somebody has ingested a file without extension
        # through quilt. In that case while we are updating either data or
        # metadata files in the repo, we are fetching all the files of that repo
        # there a file can exist which does not have extension, for that edgecase
        # this check is helpful
        warnings.formatwarning = lambda msg, *args, **kwargs: f"WARNING: {msg}\n"
        warnings.warn(
            f"{data_file}"
            + " does not have an extension. "
            + "This file is invalid. Please delete this file. "
            + "For any questions, please reach out to polly.support@elucidata.io."
        )
        data_file_name = ""
    return data_file_name


def check_data_metadata_file_path(source_folder_path: dict):
    """
    Check Metadata and Data files folders to test for empty case.
    in case of update, data/metadata folders are optional.
    Only if present in the source_folder_path dict and is a directory, empty case checked.
    """
    data_source_folder_path = source_folder_path.get("data", "")
    metadata_source_folder_path = source_folder_path.get("metadata", "")

    if data_source_folder_path:
        if not os.path.isdir(data_source_folder_path):
            raise paramException(
                title="Param Error",
                detail=f"{data_source_folder_path} is not a folder path. "
                + "Please pass a folder path containing data files. ",
            )

        data_directory = os.fsencode(data_source_folder_path)

        if not os.listdir(data_directory):
            raise paramException(
                title="Param Error",
                detail=f"{data_source_folder_path} does not contain any datafiles. "
                + "Please add the relevant data files and try again",
            )
    if metadata_source_folder_path:
        if not os.path.isdir(metadata_source_folder_path):
            raise paramException(
                title="Param Error",
                detail=f"{data_source_folder_path} is not a folder path. "
                + "Please pass a folder path containing metadata files. ",
            )

        metadata_directory = os.fsencode(metadata_source_folder_path)

        if not os.listdir(metadata_directory):
            raise paramException(
                title="Param Error",
                detail=f"{metadata_source_folder_path} does not contain any metadatafiles. "
                + "Please add the relevant metadata files and try again",
            )


def check_for_single_word_multi_word_extension(
    data_file_list: list, data_file_format_constants: list
):
    """iterate the data directory and check for different types of extensions
    in data files

    Args:
        data_directory (list): dataset files directory
        data_file_format_constants (list): List of approved formats
    """
    for file in data_file_list:
        file_ext = pathlib.Path(file).suffixes
        if len(file_ext) == 0:
            # file without extension
            raise paramException(
                title="Param Error",
                detail=f"File format for file {file} is not available"
                + f"It can be => {data_file_format_constants}",
            )
        elif len(file_ext) == 1:
            # file with single word extension
            file_ext_single_word = file_ext[-1]
            if file_ext_single_word not in data_file_format_constants:
                raise paramException(
                    title="Param Error",
                    detail=f"File format for file {file} is invalid."
                    + f"It can be => {data_file_format_constants}",
                )
        elif len(file_ext) > 1:
            # file with multi word extension
            # or `.`'s present in file name
            # check for multiword extensions
            compression_type_check = file_ext[-1]

            # compression types
            compression_types = copy.deepcopy(const.COMPRESSION_TYPES)
            # concatenating 2nd last and last word together to check
            # for multiword extension
            # pathlib.Path('my/library.tar.gar').suffixes
            # ['.tar', '.gz']
            file_type_multi_word = file_ext[-2] + file_ext[-1]
            if (compression_type_check in compression_types) and (
                file_type_multi_word in data_file_format_constants
            ):
                # multi word extension
                continue
            elif file_ext[-1] in data_file_format_constants:
                # single word extension with `.`'s in file which is accepted
                continue
            elif file_ext[-1] not in data_file_format_constants:
                raise paramException(
                    title="Param Error",
                    detail=f"File format for file {file} is invalid."
                    + f"It can be => {data_file_format_constants}",
                )


def check_status_file(source_folder_path: dict):
    """Check if status file is present or not
    If Present
    => Return Status Dict If files that have validation True are Validated
    => If all files that have validation true are not validated then raise error

    If not present
    => Check if all files have validation false
    => IF not then raise error
    Args:
        source_folder_path (dict): Source Folder Path containing data & metadata paths
    """
    metadata_folder_path = source_folder_path.get("metadata", "")
    encrypted_status_data = ""

    status_file_path = f"{metadata_folder_path}/{const.VALIDATION_STATUS_FILE_NAME}"
    # check if this path exists
    # if path exists then save the status data in encrypted_status_data
    if os.path.isfile(status_file_path):
        status_file_path = str(
            Path(metadata_folder_path)
            / Path(os.fsdecode(const.VALIDATION_STATUS_FILE_NAME))
        )
        with open(status_file_path, "rb") as encrypted_file:
            encrypted_status_data = encrypted_file.read()

    try:
        metadata_file_list = metadata_files_for_upload(metadata_folder_path)
        # if status file not present
        if not encrypted_status_data:
            empty_status_dict = check_validation_false_in_all_files(
                metadata_file_list, metadata_folder_path
            )
            return empty_status_dict
        elif encrypted_status_data:
            # decrypt status file
            f = initialize_fernet_encryption()
            decrypted_status_data = f.decrypt(encrypted_status_data)
            decrypted_status_data_dict = json.loads(decrypted_status_data)

            # check if all the files which have `validate:True` is validated or not
            # i.e. their entry is present in status dict or not
            check_all_files_validated(
                metadata_file_list, decrypted_status_data_dict, metadata_folder_path
            )
            return decrypted_status_data_dict
    except Exception as err:
        raise err


def check_all_files_validated(
    metadata_file_list: str, decrypted_status_data_dict: dict, metadata_folder_path
):
    """
        Check if the files which have `validate: True` are validated or not
        Check the files which are to be validated, have entry in decrypted_status_data_dict
    Args:
        metadata_file_list(list): list of metadata files to be checked
        metadata_folder_path (str): Folder path for metadata file
        decrypted_status_data_dict (dict): status dict containing status of all validated files
    """
    for file in metadata_file_list:
        file_path = str(Path(metadata_folder_path) / Path(os.fsdecode(file)))
        with open(file_path, "r") as file_to_upload:
            res_dict = json.load(file_to_upload)
            validate_param = (
                res_dict.get("__index__", {})
                .get("validation_check", {})
                .get("dataset", {})
                .get("validate", "")
            )

            # dataset id represents metadata file entry in status dict
            # if validate is true
            # the dataset id of res_dict
            # should exist in status dict
            # if dataset_id does not exist in status dict
            # that means the file has not been validated
            dataset_id = res_dict.get("dataset_id", "")
            if not dataset_id:
                raise Exception(f"Dataset Id not present in metadata file {file}")
            if validate_param and dataset_id not in decrypted_status_data_dict:
                raise Exception(
                    f"This {file} has validate set to True but not validated"
                )


def check_validation_false_in_all_files(
    metadata_file_list: list, metadata_folder_path: str
) -> dict:
    """Check if all the files have validation status False

    Args:
        metadata_file_list (list): List of all metadata files to be checked
    """

    # first check if all the `validate:False` or not
    # if every file has `validate:False` then every file has bypassed validation
    # in that case `validation_status` file is not needed
    # But if any file has `validate:True` and validation status is not there
    # This means the files have not gone through validation step

    for file in metadata_file_list:
        file_path = str(Path(metadata_folder_path) / Path(os.fsdecode(file)))
        with open(file_path, "r") as file_to_upload:
            res_dict = json.load(file_to_upload)
            validate_param = (
                res_dict.get("__index__", {})
                .get("validation_check", {})
                .get("dataset", {})
                .get("validate", "")
            )

            if validate_param:
                # for this file `validate:True`
                # this means file has not gone through validation
                # raise error
                raise ValidationError(
                    f"Metadata File {file} have not been validated and `validate` is set to True. "
                    + "Please run the validation step first."
                )

    # return empty dictionary
    # no status data present
    # no error is raised
    return {}


def initialize_fernet_encryption():
    """Initialize Fernet Encryption"""
    # fetch key
    response = requests.get(const.ENCRYPTION_KEY_URL)
    error_handler(response)
    encryption_key = response.text
    # initialize decryption
    f = Fernet(encryption_key)
    return f


def get_file_format_constants() -> dict:
    """
    Returns file format info from public assests url
    """
    response = copy.deepcopy(const.FILE_FORMAT_CONSTANTS)
    return response


def data_metadata_parameter_check(source_folder_path: dict, update=False):
    """
    Sanity check for data and metadata path parameters.
    This is done for both add and update functions
    In Update
    => No need to have both data and metadata file paths. Only 1 is sufficient.
    => This is because either data or metadata files can also be updated.
    In Add
    => Both file paths, data and metadata are required.
    => As file is getting ingested for the first time, both files are needed.
    """
    try:
        if not source_folder_path or not isinstance(source_folder_path, dict):
            raise paramException(
                title="Param Error",
                detail="source_folder_path should be a dict with valid data and"
                + f" metadata path values in the format {const.FILES_PATH_FORMAT} ",
            )
        if update:
            update_dataset_parameter_check(source_folder_path)
        else:
            add_dataset_parameter_check(source_folder_path)
    except Exception as err:
        raise err


def update_dataset_parameter_check(source_folder_path: dict):
    """Check update dataset parameter check

    Args:
        source_folder_path (dict): _description_

    Raise:
        Param Exception: In case parameters not as per requirement
    """
    for key in source_folder_path.keys():
        if key not in const.INGESTION_FILES_PATH_DIR_NAMES:
            raise paramException(
                title="Param Error",
                detail="source_folder_path should be a dict with valid data and"
                + f"metadata path values in the format {const.FILES_PATH_FORMAT} ",
            )
        else:
            data_directory = os.fsencode(source_folder_path[key])
            if not os.path.exists(data_directory):
                raise paramException(
                    title="Param Error",
                    detail=f"{key} path passed is not found. "
                    + "Please pass the correct path and call the function again",
                )


# TODO: Make it Similar to update_dataset_parameter_check
# where there is loop on source_folder_path.keys()
# In this way, keys to pick from source_folder_path will be picked
# from the looping variable
# Use the set substraction functionality to figure out which data or metadata path is missing
# or is there additional key present in source_folder_path
# Ex - https://github.com/ElucidataInc/polly-python-code/pull/257/files#r1048116264
# check the above link
def add_dataset_parameter_check(source_folder_path: dict):
    """Check update dataset parameter check

    Args:
        source_folder_path (dict): _description_

    Raise:
        Param Exception: In case parameters not as per requirement
    """
    # check that both data and metadata keys are present or not
    # as the keys in the dict are unique. Converting it into set will not
    # delete any keys
    # doing set comparison to check for equality
    if set(source_folder_path.keys()) == set(const.INGESTION_FILES_PATH_DIR_NAMES):
        # checking if data path passed exists or not
        data_directory = os.fsencode(source_folder_path["data"])
        if not os.path.exists(data_directory):
            raise paramException(
                title="Param Error",
                detail="`data` path passed is not found. "
                + "Please pass the correct path and call the function again",
            )
        # checking if metadata passed path exists or not
        metadadata_directory = os.fsencode(source_folder_path["metadata"])
        if not os.path.exists(metadadata_directory):
            raise paramException(
                title="Param Error",
                detail="`metadata` path passed is not found. Please pass the correct path and call the function again",
            )
    else:
        # if any of the metadata or data keys or both keys are not present
        if "data" not in source_folder_path:
            raise paramException(
                title="Param Error",
                detail=f"{source_folder_path} does not have `data` path."
                + f" Format the source_folder_path_dict like this  {const.FILES_PATH_FORMAT}",
            )
        if "metadata" not in source_folder_path:
            raise paramException(
                title="Param Error",
                detail=f"{source_folder_path} does not have `metadata` path. "
                + f"Format the source_folder_path_dict like this  {const.FILES_PATH_FORMAT}",
            )


def data_metadata_file_ext_check(source_folder_path: dict):
    """
    Check extension for data and metadata file names
    """
    format_constants = get_file_format_constants()
    data_file_format_constants = format_constants.get("data")
    data_source_folder_path = source_folder_path.get("data", "")

    if data_source_folder_path:
        data_file_list = data_files_for_upload(data_source_folder_path)
        try:
            check_for_single_word_multi_word_extension(
                data_file_list, data_file_format_constants
            )
        except Exception as err:
            raise err

    metadata_file_format_constants = format_constants["metadata"]
    metadata_source_folder_path = source_folder_path.get("metadata", "")
    if metadata_source_folder_path:
        metadata_file_list = metadata_files_for_upload(metadata_source_folder_path)
        for file in metadata_file_list:
            file_ext = pathlib.Path(file).suffixes
            file_ext_single_word = file_ext[-1]
            if file_ext_single_word not in metadata_file_format_constants:
                raise paramException(
                    title="Param Error",
                    detail=f"File format for file {file} is invalid."
                    + f"It can be => {metadata_file_format_constants}",
                )


def upload_metadata_in_add(
    polly_session,
    repo_id: str,
    priority: str,
    metadata_file_list: list,
    metadata_upload_details: dict,
    metadata_source_folder_path: str,
    file_status_dict: dict,
    data_metadata_mapping: dict,
    data_file_list: list,
):
    """Upload metadata in add datasets helper function

    Args:
        polly_session (_type_): _description_
        repo_id (str): _description_
        priority (str): _description_
        metadata_file_list (list): _description_
        metadata_upload_details (dict): _description_
        metadata_source_folder_path (str): _description_
        file_status_dict (dict): _description_
        data_metadata_mapping (dict): _description_

    Returns:
        _type_: _description_
    """
    if not metadata_file_list:
        # no metadata files in the list
        # no files to upload
        # return empty status dict
        return {}

    combined_metadata_dict, data_file_list = construct_metadata_dict_from_files_for_add(
        polly_session,
        repo_id,
        metadata_file_list,
        priority,
        data_metadata_mapping,
        metadata_source_folder_path,
        data_file_list,
    )

    # if combined_metadata_dict has metadata file dict -> then only it will be uploaded
    if combined_metadata_dict:
        file_status_dict = upload_metadata_to_s3(
            combined_metadata_dict,
            metadata_upload_details,
            file_status_dict,
            repo_id,
            polly_session,
        )

    return file_status_dict, data_file_list


def upload_metadata_in_update(
    polly_session,
    repo_id: str,
    priority: str,
    metadata_file_list: list,
    metadata_upload_details: dict,
    metadata_source_folder_path: str,
    file_status_dict: dict,
    data_metadata_mapping: dict,
    data_file_list: list,
):
    """_summary_

    Args:
        polly_session (_type_): _description_
        repo_id (str): _description_
        priority (str): _description_
        metadata_file_list (list): _description_
        metadata_upload_details (dict): _description_
        metadata_source_folder_path (str): _description_
        file_status_dict (dict): _description_
        data_metadata_mapping (dict): _description_
        data_file_list (list): _description_
    """

    (
        combined_metadata_dict,
        data_file_list,
    ) = construct_metadata_dict_from_files_for_update(
        polly_session,
        repo_id,
        metadata_file_list,
        priority,
        data_metadata_mapping,
        metadata_source_folder_path,
        data_file_list,
    )

    if combined_metadata_dict:
        file_status_dict = upload_metadata_to_s3(
            combined_metadata_dict,
            metadata_upload_details,
            file_status_dict,
            repo_id,
            polly_session,
        )

    return file_status_dict, data_file_list


def upload_metadata_to_s3(
    combined_metadata_dict: dict,
    metadata_upload_details: dict,
    file_status_dict: dict,
    repo_id: str,
    polly_session: dict,
):
    """Logic to upload metadata to s3.
    Once the upload is done, put the status of the file uploaded in the file_status dict.

    -> Temp Dir is created
    -> combinated_metadata_file put in that
    -> Upload initiated
    -> In case if upload failed, code goes in except -> again initiate upload of the file
    -> Put the file_name, status of upload mapping in the status_dict

    Args:
        combined_metadata_dict (dict): _description_
        metadata_upload_details (dict): _description_
        file_status_dict (dict): _description_
    """
    with TempDir() as metadata_dir:
        combined_metadata_file_path = str(
            f"{metadata_dir}/{Path(os.fsdecode(const.COMBINED_METADATA_FILE_NAME))}"
        )
        # opening file with `with` block closes the file at the end of with block
        # opening the file in w+ mode allows to both read and write files
        with open(combined_metadata_file_path, "w+") as combined_metadata_file:
            json.dump(combined_metadata_dict, combined_metadata_file, indent=4)

        try:
            upload_file_to_s3(
                metadata_upload_details["session_tokens"],
                metadata_upload_details["bucket_name"],
                combined_metadata_file_path,
                metadata_upload_details["metadata_directory"],
            )
            file_status_dict[const.COMBINED_METADATA_FILE_NAME] = (
                const.UPLOAD_URL_CREATED
            )
        except Exception as err:
            if isinstance(err, S3UploadFailedError) and const.EXPIRED_TOKEN in str(err):
                (
                    session_tokens,
                    bucket_name,
                    package_name,
                    metadata_directory,
                ) = get_session_tokens(polly_session, repo_id)

                # Update upload details
                metadata_upload_details = {
                    "session_tokens": session_tokens,
                    "bucket_name": bucket_name,
                    "metadata_directory": metadata_directory,
                }
                upload_file_to_s3(
                    metadata_upload_details["session_tokens"],
                    metadata_upload_details["bucket_name"],
                    combined_metadata_file_path,
                    metadata_upload_details["metadata_directory"],
                )
                file_status_dict[const.COMBINED_METADATA_FILE_NAME] = (
                    const.UPLOAD_URL_CREATED
                )
            else:
                file_status_dict[const.COMBINED_METADATA_FILE_NAME] = (
                    const.UPLOAD_ERROR_CODE
                )
                raise err
    return file_status_dict


def upload_file_to_s3(
    aws_cred: dict, bucket_name: str, file_path: str, object_key: str
):
    """
    This function is used to upload file in S3 bucket.
    Args:
        | aws_cred(dict): Dictionary which includes session tokens for authorisation.
        | bucket_name(str): Name of the bucket where file should be uploaded.
        | file_path(str): Specifies file path.
        | object_key(str): Directory path in S3.
    """
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_cred.get("access_key"),
        aws_secret_access_key=aws_cred.get("secret_access_key"),
        aws_session_token=aws_cred.get("session_token"),
    )
    # Transfer config is the configuration class for enabling
    # multipart upload on S3. For more information, please refer -
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html#boto3.s3.transfer.TransferConfig
    file_size = float(os.path.getsize(file_path))
    multipart_chunksize = const.MULTIPART_CHUNKSIZE_SMALL_FILE_SIZE
    io_chunksize = const.IO_CHUNKSIZE_SMALL_FILE_SIZE

    if file_size > const.SMALL_FILE_SIZE and file_size <= const.MEDIUM_FILE_SIZE:
        multipart_chunksize = const.MULTIPART_CHUNKSIZE_MEDIUM_FILE_SIZE
        io_chunksize = const.IO_CHUNKSIZE_MEDIUM_FILE_SIZE
    elif file_size > const.MEDIUM_FILE_SIZE:
        multipart_chunksize = const.MULTIPART_CHUNKSIZE_LARGE_FILE_SIZE
        io_chunksize = const.IO_CHUNKSIZE_LARGE_FILE_SIZE

    config = TransferConfig(
        multipart_threshold=const.MULTIPART_THRESHOLD,
        max_concurrency=const.MAX_CONCURRENCY,
        multipart_chunksize=multipart_chunksize,
        io_chunksize=io_chunksize,
        use_threads=True,
    )

    try:
        s3_client.upload_file(file_path, bucket_name, object_key, Config=config)
    except Exception as err:
        raise err


def construct_metadata_dict_from_files_for_add(
    polly_session,
    repo_id: str,
    metadata_file_list: list,
    priority: str,
    data_metadata_mapping: dict,
    metadata_path: str,
    data_file_list: list,
):
    """
    AIM:- To create a dictionary with by combining metadata of all the files in one nested dict
    This is the format needed by the API in order to ingest the data to S3
    For more information on this
    Refer this doc for more information on it -> Technical Proposal -> Section -> File level metadata format
    https://elucidatainc.atlassian.net/wiki/spaces/DIS/pages/3654713403/Data+ingestion+APIs+-+technical+proposal

    -> Iterate over metadata_file_list.

    (Create a seperate function for below one point)
    -> Check if the metadata and data file has been ingested previously
    -> If yes then raise a warning that this data-metadata file has been ingested
    Use update_dataset in that case

    -> Find the data_file corresponding to metadata file using data_metadata_mapping dict
    -> format the metadata_dict -> add current metadata dict to a bigger dict with extra attributes

    -> Once the loop ends add the ingestion_level dict to the combined_dict
    -> Return the final_combined_metadata_list

    Args:
        polly_session (_type_): _description_
        repo_id (str): _description_
        metadata_file_list (list): _description_
        priority (str): _description_
        data_metadata_mapping (dict): _description_
        metadata_path (str): _description_
    """
    combined_metadata_dict = {}
    # loop over files and append into a single dict
    for file in tqdm(
        metadata_file_list,
        desc="Processing Metadata files",
    ):
        file_path = str(Path(metadata_path) / Path(os.fsdecode(file)))
        with open(file_path, "r") as file_to_upload:
            metadata_dict = json.load(file_to_upload)
            metadata_file_name_for_upload = file

        # check if the file has been ingested before or not
        # if there is destination_folder that exists for the file
        # means file is ingested previously -> raise a warning in that case
        dataset_id = metadata_dict.get("dataset_id", "")
        # if dataset_id empty -> raise warning
        if not dataset_id:
            raise_warning_empty_dataset_id(repo_id, metadata_file_name_for_upload)
            # skip the further processing for this file
            metadata_file_name_without_ext = pathlib.Path(
                metadata_file_name_for_upload
            ).stem
            # corresponding data_file also removed
            data_file = data_metadata_mapping[metadata_file_name_without_ext]
            data_file_list.remove(data_file)
            continue

        # destination_folder is file_paths in the API
        destination_folders = check_destination_folder_for_dataset_id(
            polly_session, dataset_id, repo_id
        )
        # if a file has file_path -> it has been ingested -> raise warning
        if destination_folders:
            raise_warning_dataset_already_ingested_add(repo_id, dataset_id)
            metadata_file_name_without_ext = pathlib.Path(
                metadata_file_name_for_upload
            ).stem
            # corresponding data_file also removed
            data_file = data_metadata_mapping[metadata_file_name_without_ext]
            data_file_list.remove(data_file)
        else:
            modified_metadata_dict = format_metadata_dict_for_add(
                repo_id,
                metadata_dict,
                metadata_file_name_for_upload,
                data_metadata_mapping,
            )
            if "data" in combined_metadata_dict.keys():
                combined_metadata_dict["data"].append(modified_metadata_dict)
            else:
                combined_metadata_dict["data"] = [modified_metadata_dict]

    # add ingestion level dict in the final and put combined dict there
    final_combined_metadata_dict = {}
    if combined_metadata_dict:
        final_combined_metadata_dict = insert_ingestion_level_dict(
            priority, combined_metadata_dict
        )
    return final_combined_metadata_dict, data_file_list


def construct_metadata_dict_from_files_for_update(
    polly_session,
    repo_id: str,
    metadata_file_list: list,
    priority: str,
    data_metadata_mapping: dict,
    metadata_path: str,
    data_file_list: list,
):
    """
    AIM:- To create a dictionary with by combining metadata of all the files in one nested dict
    This is the format needed by the API in order to ingest the data to S3
    For more information on this
    Refer this doc for more information on it -> Technical Proposal -> Section -> File level metadata format
    https://elucidatainc.atlassian.net/wiki/spaces/DIS/pages/3654713403/Data+ingestion+APIs+-+technical+proposal

    Args:
        polly_session (_type_): _description_
        repo_id (str): _description_
        metadata_file_list (list): _description_
        priority (str): _description_
        data_metadata_mapping (dict): _description_
        metadata_path (str): _description_
        data_file_list (list): _description_
    """
    combined_metadata_dict = {}

    # loop over files and append into a single dict
    for file in tqdm(
        metadata_file_list,
        desc="Processing Metadata files",
    ):
        file_path = str(Path(metadata_path) / Path(os.fsdecode(file)))
        with open(file_path, "r") as file_to_upload:
            metadata_dict = json.load(file_to_upload)
            metadata_file_name_for_upload = file

        # check if the file has been ingested before or not
        # if there is destination_folder that exists for the file
        # means file is ingested previously -> raise a warning in that case
        dataset_id = metadata_dict.get("dataset_id", "")
        # if dataset_id empty -> raise warning
        if not dataset_id:
            raise_warning_empty_dataset_id(repo_id, metadata_file_name_for_upload)
            # skip the further processing for this file
            metadata_file_name_without_ext = pathlib.Path(
                metadata_file_name_for_upload
            ).stem
            # corresponding data_file also removed if present
            data_file = ""
            data_file = data_metadata_mapping.get(metadata_file_name_without_ext, "")
            if data_file:
                data_file_list.remove(data_file)
            continue

        # destination_folders is file_paths in the API
        destination_folders = check_destination_folder_for_dataset_id(
            polly_session, dataset_id, repo_id
        )

        # if for a file destination_folders is not present for update datasets -> raise warning
        if not destination_folders:
            raise_warning_if_destination_folder_not_present(repo_id, dataset_id)
            metadata_file_name_without_ext = pathlib.Path(
                metadata_file_name_for_upload
            ).stem
            # corresponding data_file also removed if present
            data_file = ""
            data_file = data_metadata_mapping.get(metadata_file_name_without_ext, "")
            if data_file:
                data_file_list.remove(data_file)
        elif len(destination_folders) > 1:
            raise_warning_for_multiple_destination_folders(
                repo_id, dataset_id, destination_folders
            )
            metadata_file_name_without_ext = pathlib.Path(
                metadata_file_name_for_upload
            ).stem
            # corresponding data_file also removed if present
            data_file = ""
            data_file = data_metadata_mapping.get(metadata_file_name_without_ext, "")
            if data_file:
                data_file_list.remove(data_file)
        else:
            curr_s3_key = ""
            # file_paths -> list will have only 1 entry
            # file_paths -> have s3_key has entry where file is ingested
            curr_s3_key = destination_folders[0]

            modified_metadata_dict = format_metadata_dict_for_update(
                repo_id,
                metadata_dict,
                metadata_file_name_for_upload,
                data_metadata_mapping,
                curr_s3_key,
            )
            if "data" in combined_metadata_dict.keys():
                combined_metadata_dict["data"].append(modified_metadata_dict)
            else:
                combined_metadata_dict["data"] = [modified_metadata_dict]

    # add ingestion level dict in the final and put combined dict there
    final_combined_metadata_dict = {}
    if combined_metadata_dict:
        final_combined_metadata_dict = insert_ingestion_level_dict(
            priority, combined_metadata_dict
        )

    return final_combined_metadata_dict, data_file_list


def insert_ingestion_level_dict(priority: str, combined_metadata_dict: dict) -> dict:
    """
    Ingestion level metadata appended in combined metadata dict
    """
    ingestion_level_metadata = copy.deepcopy(const.INGESTION_LEVEL_METADATA)
    ingestion_level_metadata["attributes"]["priority"] = priority
    if combined_metadata_dict and "data" in combined_metadata_dict:
        combined_metadata_dict["data"].insert(0, ingestion_level_metadata)
    # combined_metadata_dict["data"].append(ingestion_level_metadata)
    return combined_metadata_dict


def check_destination_folder_for_dataset_id(
    polly_session, dataset_id: str, repo_id: str
) -> str:
    """Function to call an API to check if destination folder exists
    for this dataset id.
    Return all the destination folder paths where the dataset_id file exits

    IMP ->  destination_folder is file_paths in the API

    Args:
        dataset_id (str): dataset id of the repository
    """
    try:
        destination_folder_endpoint = (
            f"{polly_session.discover_url}/repositories/{repo_id}/files"
        )
        query_params = f"?list_folders=true&dataset_id={dataset_id}"
        destination_folder_endpoint = f"{destination_folder_endpoint}/{query_params}"
        response = polly_session.session.get(destination_folder_endpoint)
        # empty file_paths initialised
        file_paths = []
        # check if response of API is 404 which means file_id does not exists
        # for this dataset id -> return empty file_paths
        if response.status_code == http_codes.NOT_FOUND:
            return file_paths
        error_handler(response)
        response_data = response.json()
        file_paths = (
            response_data.get("data", {}).get("attributes", {}).get("file_paths", [])
        )
        return file_paths
    except Exception as err:
        raise err


def format_metadata_dict(
    metadata_dict: dict,
    metadata_file_name_for_upload: str,
    data_metadata_mapping: dict,
    s3_key: str = "",
):
    """_summary_

    Args:
        metadata_dict (dict): _description_
        metadata_file_name_for_upload (str): _description_
        data_metadata_mapping (dict): _description_
        destination_folder (str, optional): _description_. Defaults to "".
    """
    formatted_metadata = {}
    metadata_file_name_without_ext = pathlib.Path(metadata_file_name_for_upload).stem
    # fetching data file for corresponding metadata file name
    # {<metadata_file_name_without_ext>: <data_file_name>}
    data_file_name = data_metadata_mapping.get(metadata_file_name_without_ext, "")
    # no matter if the data_file_name comes with the path or not, we just keep the file name
    # append the destination file path later
    # if somebody has file_name and path both in the file -> an edgecase for ticket -> LIB-314
    data_file_name_without_path = os.path.basename(data_file_name)

    if s3_key:
        # if s3_key is present -> then put the file_id as s3 key
        formatted_metadata["id"] = f"{s3_key}"
    else:
        # if s3_key is not present -> file is ingested for the first time
        # put the data file_name
        formatted_metadata["id"] = f"{data_file_name_without_path}"

    formatted_metadata["type"] = "file_metadata"
    formatted_metadata["attributes"] = metadata_dict

    return formatted_metadata


def format_metadata_dict_for_add(
    repo_id: str,
    metadata_dict: dict,
    metadata_file_name_for_upload: str,
    data_metadata_mapping: dict,
):
    """Format the metadata_dict as defined in the API document
    {
        id:"file_name",
        type:<>,
        attributes:{
            ....<metadata_dict>.....
        }
    }

    Args:
        repo_id (str): _description_
        metadata_dict (dict): _description_
        metadata_file_name_for_upload (str): _description_
        data_metadata_mapping (dict): _description_
    """
    return format_metadata_dict(
        metadata_dict, metadata_file_name_for_upload, data_metadata_mapping
    )


def format_metadata_dict_for_update(
    repo_id: str,
    metadata_dict: dict,
    metadata_file_name_for_upload: str,
    data_metadata_mapping: dict,
    s3_key: str,
):
    """
    {
        id:"s3_key",
        type:<>,
        attributes:{
            ....<metadata_dict>.....
        }
    }

    Args:
        repo_id (str): _description_
        metadata_dict (dict): _description_
        metadata_file_name_for_upload (str): _description_
        data_metadata_mapping (dict): _description_
        s3_key (str): _description_
    """
    return format_metadata_dict(
        metadata_dict,
        metadata_file_name_for_upload,
        data_metadata_mapping,
        s3_key,
    )


def raise_warning_empty_dataset_id(repo_id: str, metadata_file_name: str):
    """Raise warning if dataset_id not present in the metadata file

    Args:
        repo_id (str): _description_
        metadata_file_name (str): _description_
    """
    warnings.formatwarning = lambda msg, *args, **kwargs: f"WARNING: {msg}\n"
    warnings.warn(
        f"The dataset_id is not present in the file: {metadata_file_name} for repo: {repo_id}. "
        + "This file is skipped in ingestion. Please put the dataset_id in the metadata file, "
        + "and ingest again."
    )


def raise_warning_missing_dataset_id(repo_id: str, data_file_name: str):
    """_summary_

    Args:
        repo_id (str): _description_
        data_file_name (str): _description_
    """
    warnings.formatwarning = lambda msg, *args, **kwargs: f"WARNING: {msg}\n"
    warnings.warn(
        f"The dataset_id is not present in the file: {data_file_name} for repo: {repo_id} "
        + "in the file_mapping_dict passed as argument in update_datasets. This file is skipped in ingestion. "
        + "Please put the dataset_file and dataset_id mapping in file_mapping dict, and ingest again."
    )


def raise_warning_dataset_already_ingested_add(repo_id: str, dataset_id: str):
    """Dataset already been ingested warning. Use update instead of add for this file

    Args:
        repo_id (str): _description_
        dataset_id (str): _description_
    """
    warnings.formatwarning = lambda msg, *args, **kwargs: f"WARNING: {msg}\n"
    warnings.warn(
        f"The dataset_id: {dataset_id} is already ingested for repo: {repo_id}. "
        + "Please use update_dataset function to update the file. "
    )


def upload_data_in_add(
    repo_id: str,
    data_file_list: list,
    data_upload_details: dict,
    data_source_folder_path: str,
    file_status_dict: dict,
    polly_session,
):
    """Upload data in add datasets helper function

    Args:
        polly_session (_type_): _description_
        repo_id (str): _description_
        data_file_list (list): _description_
        data_upload_details (dict): _description_
        data_source_folder_path (str): _description_
        file_status_dict (dict): _description_
        data_metadata_mapping (dict): _description_
    """
    if not data_file_list:
        # data file list empty
        return file_status_dict

    for file in tqdm(data_file_list, desc="Uploading data files", unit="files"):
        file_path = str(Path(data_source_folder_path) / Path(os.fsdecode(file)))
        data_file_name_for_upload = file
        try:
            upload_file_to_s3(
                data_upload_details["session_tokens"],
                data_upload_details["bucket_name"],
                file_path,
                data_upload_details["package_name"] + data_file_name_for_upload,
            )
            file_status_dict[data_file_name_for_upload] = const.UPLOAD_URL_CREATED
        except Exception as err:
            if isinstance(err, S3UploadFailedError) and const.EXPIRED_TOKEN in str(err):
                (
                    session_tokens,
                    bucket_name,
                    package_name,
                    metadata_directory,
                ) = get_session_tokens(polly_session, repo_id)

                data_upload_details = {
                    "session_tokens": session_tokens,
                    "bucket_name": bucket_name,
                    "package_name": package_name,
                }
                upload_file_to_s3(
                    data_upload_details["session_tokens"],
                    data_upload_details["bucket_name"],
                    file_path,
                    data_upload_details["package_name"] + data_file_name_for_upload,
                )
                file_status_dict[data_file_name_for_upload] = const.UPLOAD_URL_CREATED
            else:
                file_status_dict[data_file_name_for_upload] = const.UPLOAD_ERROR_CODE
                raise err
    return file_status_dict


def generating_response_from_status_dict(
    file_status_dict: dict, result_list: list
) -> list:
    """
    Generating the response with File Name and Error Message
    Store the response in the list format
    Response Message Cases
    1. If the whole metadata file not uploaded => `Reupload the metadata again`
    2. If File is uploaded => `File Uploaded`
    3. If the data file is not uploaded => `Reupload the data file and its metadata also`
    """

    for key, value in file_status_dict.items():
        if key == const.COMBINED_METADATA_FILE_NAME and value in [400, 404, 409]:
            response = []
            response.append(key)
            response.append("Metadata Not uploaded, reupload the metadata again")
            result_list.append(response)
        elif value == 204:
            response = []
            response.append(key)
            response.append("File Uploaded")
            result_list.append(response)
        elif value in [400, 404, 409]:
            response = []
            response.append(key)
            response.append(
                "File Not Uploaded, reupload the file again and also upload the corresponding metadata"
            )
            result_list.append(response)
    return result_list


def commit_data_to_repo(polly_session, repo_id: str):
    """
    Inform the infra to commit the data uploaded
    Not raising error in this if commit API Fails because
    even if manual commit fails, files will be picked up in
    automatic update. Users need not know about this
    Args:
        repo_id: str
    """
    try:
        schema_base_url = f"{polly_session.discover_url}/repositories"
        url = f"{schema_base_url}/{repo_id}/files?action=commit"
        resp = polly_session.session.post(url)
        error_handler(resp)
        # 202 is the success code for commit message success
        if resp.status_code == http_codes.ACCEPTED:
            print("\n")
            print(const.DATA_COMMIT_MESSAGE)
    except Exception:
        # no error needs to be raised
        # in case of error manual commit will not happen
        # data will be auto-committed which is the current process
        pass


def print_dataframe(
    max_rows: int, max_columns: int, width: int, data_upload_results_df: pd.DataFrame
):
    """Print the data frame with the paramters in the arguments

    Args:
        max_rows (int): _description_
        max_columns (int): _description_
        width (int): _description_
    """
    with pd.option_context(
        "display.max_rows",
        max_rows,
        "display.max_columns",
        max_columns,
        "display.width",
        width,
    ):
        print("\n", data_upload_results_df)


def check_for_unmapped_files_in_oa(
    data_metadata_mapping: dict,
    data_file_list: list,
    metadata_file_list: list,
    unmapped_data_file_names: list,
    unmapped_metadata_file_names: list,
    file_mapping: list,
    polly_session,
    source_folder_path: dict,
    repo_id: str,
):
    """_summary_

    Args:
        data_metadata_mapping (dict): _description_
        data_file_list (list): _description_
        metadata_file_list (list): _description_
        unmapped_data_file_names (list): _description_
        unmapped_metadata_file_names (list): _description_
    """
    metadata_path = source_folder_path.get("metadata", "")
    # unmapped_metadata_file_names -> list of unmapped metadata file names without ext
    if metadata_path and unmapped_metadata_file_names:
        (
            data_metadata_mapping,
            metadata_file_list,
            unmapped_metadata_file_names,
        ) = check_for_unmapped_metadata_files_in_oa_for_update(
            polly_session,
            data_metadata_mapping,
            metadata_file_list,
            unmapped_metadata_file_names,
            metadata_path,
            repo_id,
        )

    data_path = source_folder_path.get("data", "")

    # unmapped_data_file_names -> list of unmapped data file names with ext
    if data_path and unmapped_data_file_names and file_mapping:
        (
            data_metadata_mapping,
            data_file_list,
            unmapped_data_file_names,
        ) = check_for_unmapped_data_files_in_oa_for_update(
            polly_session,
            data_metadata_mapping,
            data_file_list,
            unmapped_data_file_names,
            file_mapping,
            data_path,
            repo_id,
        )
    elif data_path and unmapped_data_file_names and not file_mapping:
        # if datapath is present and there are unmapped data files(corresponding metadata file not given)
        # but the user has not passed file_mapping dict
        raise paramException(
            title="file_mapping required",
            detail="If only data files are getting updated, then file_mapping dict required",
        )

    return (
        data_metadata_mapping,
        data_file_list,
        metadata_file_list,
        unmapped_metadata_file_names,
        unmapped_data_file_names,
    )


def check_for_unmapped_metadata_files_in_oa_for_update(
    polly_session,
    data_metadata_mapping: dict,
    metadata_file_list: list,
    unmapped_metadata_file_names: list,
    metadata_path: str,
    repo_id: str,
):
    """_summary_

    Args:
        polly_session (_type_): _description_
        data_metadata_mapping (dict): _description_
        metadata_file_list (list): _description_
    """

    final_unmapped_files_list = []

    for metadata_file in unmapped_metadata_file_names:
        # unmapped file_names -> have only names of metadata files
        # adding the extension -> as every file will have extension as json
        metadata_file_with_ext = metadata_file + ".json"
        file_path = str(Path(metadata_path) / Path(os.fsdecode(metadata_file_with_ext)))
        with open(file_path, "r") as file_to_upload:
            metadata_dict = json.load(file_to_upload)
            metadata_file_name_for_upload = metadata_file_with_ext

        # check if the file has been ingested before or not
        # if there is destination_folder that exists for the file
        # means file is ingested previously -> raise a warning in that case
        dataset_id = metadata_dict.get("dataset_id", "")
        if not dataset_id:
            raise_warning_empty_dataset_id(repo_id, metadata_file_name_for_upload)
            # remove the file from metadata_file_list
            # metadata file list -> will have metadata file name with ext
            metadata_file_list.remove(metadata_file_name_for_upload)
            # append the current file in the final_unmapped_files_list
            final_unmapped_files_list.append(metadata_file)

            # skip the further processing for this file
            continue

        # destination_folder is file_paths in the API
        destination_folders = check_destination_folder_for_dataset_id(
            polly_session, dataset_id, repo_id
        )

        # dataset not ingested, please use add_dataset to ingest data first
        if not destination_folders:
            raise_warning_if_destination_folder_not_present(repo_id, dataset_id)
            # remove the file from metadata_file_list
            # metadata file list -> will have metadata file name with ext
            metadata_file_list.remove(metadata_file_name_for_upload)

            # append the current file in the final_unmapped_files_list
            final_unmapped_files_list.append(metadata_file)
        elif len(destination_folders) > 1:
            # more than one destination folders present for the dataset id
            raise_warning_for_multiple_destination_folders(
                repo_id, dataset_id, destination_folders
            )
            # remove the file from metadata_file_list
            # metadata file list -> will have metadata file name with ext
            metadata_file_list.remove(metadata_file_name_for_upload)
            # append the current file in the final_unmapped_files_list
            final_unmapped_files_list.append(metadata_file)
        else:
            # unmapped metadata file -> has the corresponding dataset file in the OA
            # THIS FILE NOT UNMAPPED NOW
            # update the dataset_mapping -> with the metadata and data mapping
            # destination folder list -> will contain only 1 entry
            # s3 key in the file_path will the s3_key -> that has dataset_file_name
            dataset_file = get_dataset_file_from_file_path(destination_folders[0])

            data_metadata_mapping[metadata_file] = dataset_file

            # remove the current metadata file from the unmapped metadata file list
            # as the system has found its mapping in the OA
            # unmapped_metadata_file_names -> will have metadata file names without extension
            # unmapped_metadata_file_names.remove(metadata_file)

    return data_metadata_mapping, metadata_file_list, final_unmapped_files_list


def check_for_unmapped_data_files_in_oa_for_update(
    polly_session,
    data_metadata_mapping: dict,
    data_file_list: list,
    unmapped_data_file_names: list,
    file_mapping: list,
    data_path: dict,
    repo_id,
):
    """_summary_

    Args:
        polly_session (_type_): _description_
        data_metadata_mapping (dict): _description_
        data_file_list (list): _description_
        unmapped_data_file_names (list): _description_
        file_mapping (list): _description_
    """
    final_unmapped_data_files = []

    # unmapped_data_file_names -> full data file names with ext
    for data_file in unmapped_data_file_names:
        # for a data_file -> dataset_id is paired in file_mapping
        dataset_id = ""
        dataset_id = fetch_dataset_id_for_data_file(file_mapping, data_file)

        if not dataset_id:
            raise_warning_missing_dataset_id(repo_id, data_file)

            # remove the file from metadata_file_list
            # data_file_list -> contains data_file name with extension
            data_file_list.remove(data_file)
            final_unmapped_data_files.append(data_file)
            # skip the further processing for this file
            continue

        # destination_folder is file_paths in the API
        destination_folders = check_destination_folder_for_dataset_id(
            polly_session, dataset_id, repo_id
        )
        # dataset not ingested, please use add_dataset to ingest data first
        if not destination_folders:
            raise_warning_if_destination_folder_not_present(repo_id, dataset_id)
            # remove the file from metadata_file_list
            # data_file_list -> contains data_file name with extension
            data_file_list.remove(data_file)
            final_unmapped_data_files.append(data_file)
            # skip the further processing for this file
        elif len(destination_folders) > 1:
            # more than one destination folders present for the dataset id
            raise_warning_for_multiple_destination_folders(
                repo_id, dataset_id, destination_folders
            )
            # remove the file from metadata_file_list
            # data_file_list -> contains data_file name with extension
            data_file_list.remove(data_file)
            final_unmapped_data_files.append(data_file)
        else:
            # unmapped metadata file -> has the corresponding dataset file in the OA
            # THIS FILE NOT UNMAPPED NOW
            # update the dataset_mapping -> with the metadata and data mapping
            # destination folder list -> will contain only 1 entry

            # naming convention of data and metadata file is same
            # their extension can be different
            # adding metadata and data file mapping in data_metadata_mapping
            # metadata_file_name == data_file_without_ext
            data_file_without_ext = get_file_name_without_suffixes(data_file)
            # data_mapping_dict format -> {<metadata_file_name_with_ext>: <data_file>}
            data_metadata_mapping[data_file_without_ext] = data_file

            # remove data_file from the unmapped data files list
            # unmapped_data_file_names -> has full data_file name with ext
            # unmapped_data_file_names.remove(data_file)

    return data_metadata_mapping, data_file_list, final_unmapped_data_files


def fetch_dataset_id_for_data_file(file_mapping: list, data_file: str):
    """Fetch dataset_id for data file

    Args:
        file_mapping (list): list of dicts containing file
    """
    if data_file in file_mapping:
        return file_mapping[data_file]


def raise_warning_for_multiple_destination_folders(
    repo_id: int, dataset_id: str, dest_fldrs: list
):
    """Raise warning if dataset is ingested in multiple destination folders

    Args:
        repo_id (int): _description_
        dataset_id (str): _description_
        dest_fldr (list): _description_
    """
    warnings.formatwarning = lambda msg, *args, **kwargs: f"WARNING: {msg}\n"
    warnings.warn(
        f"The dataset_id: {dataset_id} is ingested for repo: {repo_id} and "
        + f"in multiple destination folders: {dest_fldrs}. "
        + "Please use delete_datasets function to delete the exta paths. "
        + "Ideally dataset should be ingested in only one destination folder"
    )


def raise_warning_if_destination_folder_not_present(repo_id: int, dataset_id: str):
    """Raise warning if destination folder not present

    Args:
        repo_id (int): _description_
        dataset_id (str): _description_
    """
    warnings.formatwarning = lambda msg, *args, **kwargs: f"WARNING: {msg}\n"
    warnings.warn(
        f"The dataset_id: {dataset_id} is not ingested for repo: {repo_id}. "
        + "Please use add_datasets function to ingest the data first. "
    )


def get_dataset_file_from_file_path(file_path_str: str):
    """File path string containing destination folder and dataset file

    file_path[0]: "<s3_key>"
    s3_key has the dataset_file_name in the end

    Args:
        file_path_str (str): _description_
    """
    # returns the file_name from the full s3 key
    data_file = os.path.basename(file_path_str)
    return data_file


def raise_warning_for_unmapped_metadata_file_update(unmapped_metadata_files: list):
    """_summary_

    Args:
        unmapped_metadata_files (list): _description_
    """
    print("\n")
    warnings.formatwarning = lambda msg, *args, **kwargs: f"WARNING: {msg}\n"
    warnings.warn(
        f" These metadata files: {unmapped_metadata_files} do not have pair data_files in input."
        + "\n"
        + "Case 1:-"
        + "The pair data_files for these metadata files do not exist in the OA also. "
        + "These files have not been ingested, please use add_datasets for ingesting these files."
        + "\n"
        + "OR"
        + "\n"
        + "Case 2:-"
        + " These files are present in multiple destination folders. Please delete extra folders"
    )
    print("\n")


def raise_warning_for_unmapped_data_file_update(unmapped_data_files: list):
    """_summary_

    Args:
        unmapped_data_files (list): _description_
    """
    print("\n")
    warnings.formatwarning = lambda msg, *args, **kwargs: f"WARNING: {msg}\n"
    warnings.warn(
        f"These data files: {unmapped_data_files} do not have pair metadata_files in input. "
        + "\n"
        + "Case 1:-"
        + "The pair metadata_files for these data_files do not exist in the OA also. "
        + "These files have not been ingested, please use add_datasets for ingesting these files."
        + "\n"
        + "OR"
        + "\n"
        + "Case 2:-"
        + " These files are present in multiple destination folders. Please delete extra folders"
    )
    print("\n")


def parameter_check_for_list_dataset_ids(dataset_ids):
    """Checking for validity of repo id
    Args:
        dataset_id (): Dataset Id of the dataset

    Raises:
        paramException: Error if dataset id is empty or is not str
    """
    if not (dataset_ids and isinstance(dataset_ids, list)):
        raise paramException(
            title="Param Error",
            detail="dataset_ids should be list of strings",
        )


def dataset_file_path_dict_type_check_in_delete_datasets(dataset_file_path_dict: dict):
    """dataset_file_path_dict type check in delete datasets

    Args:
        dataset_file_path_dict (dict): dict of dataset_file_path_dict
    """
    if not isinstance(dataset_file_path_dict, dict):
        raise paramException(
            title="Param Error",
            detail=(
                "dataset_file_path_dict should be dict -> {<dataset_id>:<list_of_paths>}",
            ),
        )

    for key, val in dataset_file_path_dict.items():
        if not isinstance(val, list):
            raise paramException(
                title="File paths datatype is incorrect",
                detail=(
                    "File paths should be in the format of list of strings in the "
                    + "dataset_file_path_dict. Correct format -> {<dataset_id>:<list_of_paths>}"
                ),
            )
        if not isinstance(key, str):
            raise paramException(
                title="dataset_id datatype is incorrect",
                detail=(
                    "dataset_id should be in the format of string in the "
                    + "dataset_file_path_dict. Correct format -> {<dataset_id>:<list_of_paths>}"
                ),
            )


def dataset_file_path_is_subset_dataset_id(
    dataset_ids: list, dataset_file_path_dict: dict
):
    """Check if all the keys of dataset_file_path_dict which represents dataset id
    are present in dataset_ids list or not
    Ideally all the dataset id present as key in dataset_file_path_dict should be mandatorily
    present in the dataset_ids list
    i.e. All the keys of dataset_file_path_dict should be a subset of dataset_ids list
    The function is to check the subset validity

    Args:
        dataset_ids (list): List of dataset ids
        dataset_file_path_dict (dict): Dictionary containing dataset ids and file paths
        corresponding to it

    Raises:
        paramError: If Params are not passed in the desired format or value not valid.

    """
    dataset_file_path_dict_keys = dataset_file_path_dict.keys()

    # converting both the lists and checking for the error case
    # Error Case -> dataset_file_path_dict_keys list not a subset of dataset_ids list
    # in that case raise warnings for those dataset_ids
    # which are a part of dataset_file_path_dict but not dataset_ids
    # For Example
    # a = [1, 3, 5]
    # b = [1, 3, 5, 8]
    # set(a) <= set(b)
    # ANS -> TRUE
    if not set(dataset_file_path_dict_keys) <= set(dataset_ids):
        # find the difference of elements present in dataset_file_path_dict_keys list
        # that are not present in dataset_ids list
        # Example ->
        # list_1 = ['a', 'b', 'c']
        # list_2 = ['a', 'd', 'e']
        # result_1 = list(set(list_2).difference(list_1))
        # print(result_1)  # 👉️ ['e', 'd']
        invalid_dataset_ids = list(
            set(dataset_file_path_dict_keys).difference(dataset_ids)
        )
        warnings.formatwarning = lambda msg, *args, **kwargs: f"WARNING: {msg}\n"
        warnings.warn(
            f"Unable to delete these dataset_ids {invalid_dataset_ids} because "
            + "these are not present in dataset_ids list. "
            + "For any questions, please reach out to polly.support@elucidata.io. "
        )
        # break line added -> for better UX
        print("\n")


def normalize_file_paths(dataset_file_path_dict: dict):
    """Normalise all the file paths in the dataset_file_path_dict

    Args:
        dataset_file_path_dict (dict): key is dataset id and value is the file_path
    """
    # iterating over the dictionary containing dataset_id and list of file paths
    # format: {<dataset_id>:[<file_path_1>, ........., <file_path_n>]}
    for dataset_id, file_path_list in dataset_file_path_dict.items():
        # iterating over the list of file paths and
        # normalising each file path and storing in
        # normalised_file_path_list which will be mapped to
        # dataset_id
        normalised_file_path_list = []
        for file_path in file_path_list:
            normalised_file_path = os.path.normpath(file_path)
            normalised_file_path_list.append(normalised_file_path)
        dataset_file_path_dict[dataset_id] = normalised_file_path_list
    return dataset_file_path_dict


def parameter_check_for_delete_dataset(
    repo_id: int, dataset_ids: list, dataset_file_path_dict: dict
):
    """
    Sanity check for all the parameters of delete datasets
    """
    try:
        polly_services_hlpr.parameter_check_for_repo_id(repo_id)
        parameter_check_for_list_dataset_ids(dataset_ids)
        dataset_file_path_dict_type_check_in_delete_datasets(dataset_file_path_dict)
    except Exception as err:
        raise err


def parameter_check_for_dataset_id(dataset_id):
    """Checking for validity of repo id
    Args:
        dataset_id (): Dataset Id of the dataset

    Raises:
        paramException: Error if dataset id is empty or is not str
    """
    if not (dataset_id and isinstance(dataset_id, str)):
        raise paramException(
            title="Param Error",
            detail="Argument 'dataset_id' is either empty or invalid. It should be a string. Please try again.",
        )


# used in delete dataset
def fetch_list_api_control_levers() -> str:
    """Fetch List Files API control Levers"""
    response = requests.get(const.LIST_FILE_API_CONTROL_LEVER_LINK)
    error_handler(response)
    control_levers_dict = json.loads(response.text)
    default_page_size = control_levers_dict.get(
        const.DEFAULT_PAGE_SIZE_LIST_FILES_KEY_NAME
    )
    page_reduction_percentage = control_levers_dict.get(
        const.PAGE_REDUCTION_PERCENTAGE_LIST_FILES_KEY_NAME
    )
    return default_page_size, page_reduction_percentage


def get_all_file_paths_param_check(repo_id: int, dataset_id: str):
    """Function to do sanity checks on arguments of
    get_all_file_paths_param functions

    Args:
        repo_id (int): repo_id of the repo of the Omixatlas
        dataset_id (str): dataset id passed by the user
    """
    try:
        polly_services_hlpr.parameter_check_for_repo_id(repo_id)
        parameter_check_for_dataset_id(dataset_id)
    except Exception as err:
        raise err


# used in delete dataset
def reduce_page_size(default_page_size: int, reduction_percentage: int) -> int:
    """Reduce the page size based on the current reduction percentage

    Args:
        default_page_size (int): current page size

    Returns:
        int: reduced page size
    """
    # error_msg_dict = extract_error_message(response.text)
    # reduce the default page size

    # reduce page size by PAGE_REDUCTION_PERCENTAGE_LIST_FILES
    # reduction_multiplier = (100 - const.PAGE_REDUCTION_PERCENTAGE_LIST_FILES) / 100

    reduction_multiplier = (100 - reduction_percentage) / 100

    default_page_size = reduction_multiplier * default_page_size

    # TODO -> Put tracking to see how many times API is crashing
    # with the current default page size -> the tracking will help
    # to optimise the control lever

    # give nearest rounded integer value -> so that decimal does not come
    return round(default_page_size)


# used in delete dataset
def extract_page_after_from_next_link(next_link: str) -> int:
    """Extract page[after] from next_link

    Args:
        next_link (str): next_link given by the API in pagination

    Returns:
        int: page_after
    """
    # next link format ->
    # /repositories/1643016586529/files
    # ?page[size]=2500&page[after]=2500&version=latest&include_metadata=True

    # if page[after] exists in next_link then the page[after] value will be b/w
    # `page[after]=` and `&`

    if "page[after]" in next_link:
        page_after_str = helpers.find_between(next_link, "page[after]=", "&")
        # typecast the page[after] value to int and return
        return int(page_after_str)
    else:
        # return 0 as default page_size if "page[after]" does not exist
        # in the next_link -> this is an extreme case where the API is broken
        # in normal cases this error may never come
        return 0


# used in delete dataset
def list_api_crash_messaging_tracking(self, page_after: int, default_page_size: int):
    """Function to print API crashing and log events for tracking

    Args:
        page_after (int): page_after value after which API crashed
        default_page_size (int): page_size for which API crashed
    """
    helpers.debug_print(self, "------API crashed-------")
    helpers.debug_print(self, f"----current page[after] value: {page_after}")

    helpers.debug_print(self, f"--current_page_size: {default_page_size}")

    # tracking metadata
    # what parameters need to be shown on tracking dashboard
    # put in the properties dict and pass it
    properties_dict = {}
    properties_dict["api_name"] = "list_file_api"
    properties_dict["crashed_page_size"] = default_page_size
    properties_dict["current_page_after"] = page_after

    helpers.debug_logger(self, properties_dict)


# used in delete dataset
# cached for the cases when this function is called internally when same
# result is needed multiple times


# need to change this function -> as the per the new API developed
@lru_cache(maxsize=None)
def list_files(
    polly_session, repo_id: str, metadata="true", data="true", version="current"
) -> list:
    """helper function to integrate list files API response

    Args:
        self (polly_session_object): polly_session
        repo_id (str): repo id of the omixatlas
    Returns:
        list_files_resp -> list of objects with requests type
    """
    # endpoints for list files API
    files_api_endpoint = f"{polly_session.discover_url}/repositories/{repo_id}/files"

    # initialising an empty string of next link
    next_link = ""
    responses_list = []

    # page_size -> for paginating the API
    # set to the default page size mentioned in the constants
    # if the API crashes then -> it will reduced
    # default_page_size = const.DEFAULT_PAGE_SIZE_LIST_FILES
    default_page_size, reduction_percentage = fetch_list_api_control_levers()

    # initially set to 0, but will be updated
    # as the API request crashes request is called on next link
    # in that next_link will be set to empty string and page_after
    # will be updated to current page_after in the next_link
    page_after = 0

    # initially next_link will be empty string
    # once the pages will end -> next_link will be set to None by the API
    while next_link is not None:
        if next_link:
            next_endpoint = f"{polly_session.discover_url}{next_link}"
            response = polly_session.session.get(next_endpoint)

            if response.status_code == http_codes.PAYLOAD_TOO_LARGE:
                page_after = extract_page_after_from_next_link(next_link)
                list_api_crash_messaging_tracking(
                    polly_session, page_after, default_page_size
                )

                default_page_size = reduce_page_size(
                    default_page_size, reduction_percentage
                )
                helpers.debug_print(
                    polly_session, f"--reduced page size---: {default_page_size}"
                )
                # intialise next_link to empty str so that query_params
                # dict is intialised again with new default_page_size and page_after
                next_link = ""
                # go to the next iteation
                continue
        else:
            query_params = {
                "page[size]": default_page_size,
                "page[after]": page_after,
                "include_metadata": f"{metadata}",
                "data": f"{data}",
                "version": f"{version}",
            }

            response = polly_session.session.get(
                files_api_endpoint, params=query_params
            )
            # in case of payload too large error, reduce the page size
            if response.status_code == http_codes.PAYLOAD_TOO_LARGE:
                list_api_crash_messaging_tracking(
                    polly_session, page_after, default_page_size
                )

                default_page_size = reduce_page_size(
                    default_page_size, reduction_percentage
                )

                helpers.debug_print(
                    polly_session, f"--reduced page size---: {default_page_size}"
                )
                # go to the next iteation
                continue

        error_handler(response)
        response_json = response.json()
        # list of request objects
        # reponse object having both status and data of the response
        responses_list.append(response)
        # seeing after 1000 pages whose response is already fetched
        # if there are more pages
        next_link = response_json.get("links").get("next")
        helpers.debug_print(polly_session, f"next link--: {next_link}")
    return responses_list


def warning_invalid_path_delete_dataset_multiple_paths(
    invalid_path: str, datasetid_key: str
):
    """Function to raise warning for invalid path for dataset_ids present in
    multiple paths
    Args:
        invalid_path: str
    """
    warnings.formatwarning = lambda msg, *args, **kwargs: f"WARNING: {msg}\n"
    warnings.warn(
        "Unable to delete file from these file paths "
        + f"{invalid_path}"
        + " because in these file paths, file corresponding to the dataset id "
        + datasetid_key
        + " is not present. "
        + "Please run <omixatlas_obj>.get_all_file_paths(<repo_id>,<dataset_id>) to get all "
        + "valid paths for this dataset_id. For any questions, please reach out to polly.support@elucidata.io. "
    )
    # break line added -> for better UX
    print("\n")
    res = {
        "Message": "Dataset not deleted because file_path is incorrect.",
        "Folder Path": f"{invalid_path}",
    }
    return res


def user_file_path_incorrect(user_file_path: str, datasetid_key: str):
    """If user_file_path not equal to file_path passed by the user

    Args:
        user_file_path (str): file_path passed by the user in dataset_file_path_dict
        datasetid_key (str): dataset_id for which file_path passed
    """
    # passed file path by the user is does not contain the file
    # raise a warning and store an error message corresponding to
    # dataset_id and return
    warnings.formatwarning = lambda msg, *args, **kwargs: f"WARNING: {msg}\n"
    warnings.warn(
        "Unable to delete file from the file_path "
        + f"{user_file_path} because the file corresponding to the "
        + f"dataset id {datasetid_key} is not present in this file_path. "
        + "This dataset_id file is present only in 1 path so passing path "
        + "using optional parameter not required here. "
        + "For any questions, please reach out to polly.support@elucidata.io. "
    )
    # break line added -> for better UX
    print("\n")
    res = {
        "Message": "Dataset not deleted because file_path for the dataset_id is incorrect",
        "Folder Path": f"{user_file_path}",
    }
    return res


# TODO -> @shilpa to make a ticket for this to make this generic enough
# delete dataset used
def check_res_dict_has_file_deleted_entries(result_dict: dict) -> bool:
    """Check if result_dict has entries for deleted files
    If res_dict has entries of deleted files, then only commit API will be
    called else commit API will not be called
    This will ensure that commit API is only called when actually there is an
    entry in the DF where files are deleted

    Args:
        result_dict (dict): DF containing messages from the API corresponding to
        deletion request

    Returns:
        bool: Flag to show if any dataset_id from the result_dict have deleted message
    """
    # valid_deletion_entry is initalized to false -> if no deletion entry is valid
    # then False flag will be returned -> commit API will not be hit
    valid_deletion_entry = False
    # Example result_dict
    # {'GSE140509_GPL16791':
    # {'Message': 'Request Accepted. Dataset will be deleted in the next version of OmixAtlas',
    # 'Folder Path': 'transcriptomics_213/GSE140509_GPL16791.gct'}}

    # if message string has `Request Accepted` substring then deletion for that dataset_id
    # has been accepted
    # if in any of the other entries -> the deletion request is accepted -> means
    # at least one dataset_id has valid deletion entry -> commit will be hit then
    # for deletion request -> break the loop there

    # TODO ->
    # i. Make this more generic enough
    # ii. ( any(any('Request Accepted' in deletion_res["Message"])
    # for deletion_res in result_dict.values()) )

    for dataset_id, deletion_res_list in result_dict.items():
        if isinstance(deletion_res_list, dict):
            # deletion_res_list -> dict ->
            # {'Message': 'Dataset  for the dataset_id is incorrect',
            # 'Folder Path': 'transcriptomics_906s/GSE76311_GPL17586.gct'}
            message = deletion_res_list["Message"]
            if "Request Accepted" in message:
                valid_deletion_entry = True
                break
        elif isinstance(deletion_res_list, list):
            for deletion_res in deletion_res_list:
                # deletion_res -> dict ->
                # {'Message': 'Dataset  for the dataset_id is incorrect',
                # 'Folder Path': 'transcriptomics_906s/GSE76311_GPL17586.gct'}
                message = deletion_res["Message"]
                if "Request Accepted" in message:
                    valid_deletion_entry = True
                    break

    return valid_deletion_entry


def convert_delete_datasets_res_dict_to_df(result_dict: dict):
    """Convert result dict of delete datasets to df
    Key -> dataset_id
    Value -> Message from deleted files in a list
    DF
    Col 1 -> DatasetId
    Col 2 -> Message
    Col 3 -> File Path


    Args:
        result_dict (dict): Dict of delete datasets result
    """
    # res dict format -> {"<dataset_id>":[{"<Folder_Path>":<val>, "Message":<val>}]}
    # result dict format -> example
    # {'GSE101942_GPL11154': [{'Message': 'Dataset not deleted because file_path for
    #  the dataset_id is incorrect', 'Folder Path': 'transcriptomics_906s/GSE76311_GPL17586.gct'},
    # {'Message': 'Dataset not deleted because file_path for the dataset_id is incorrect',
    # 'Folder Path': 'transcriptomics_907s/GSE76311_GPL17586.gct'}]}
    df_list = []
    for key, val_list in result_dict.items():
        for val in val_list:
            df_1 = pd.DataFrame(
                val,
                index=[
                    "0",
                ],
            )
            # print(df_1)
            df_1.insert(0, "DatasetId", key)
            # df_1["Dataset Id"] = key
            df_list.append(df_1)

    data_delete_df = pd.concat(df_list, axis=0, ignore_index=True)
    print(data_delete_df.to_string(index=False, max_colwidth=10))
