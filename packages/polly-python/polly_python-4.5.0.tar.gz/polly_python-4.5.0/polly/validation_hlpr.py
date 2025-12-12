import os
import copy
import requests
import warnings
import json
from pathlib import Path
from polly.errors import paramException, error_handler
from tqdm import tqdm
from polly.omixatlas import OmixAtlas

# import pandas as pd
import polly.constants as const
from cryptography.fernet import Fernet
import polly.omixatlas_hlpr as omix_hlpr


def create_status_file(status_dict: dict, metadata_path: str):
    """Creates an encrypted status dict and places it inside
        metadata folder and mark the file hidden
    Args:
        status_dict (dict): Status of the files validated
        metadata_path: Metadata folder path
    """

    # fetch key
    response = requests.get(const.ENCRYPTION_KEY_URL)
    error_handler(response)
    encryption_key = response.text

    # initialize encryption
    f = Fernet(encryption_key)

    modified_status_dict = modify_status_dataset(status_dict, metadata_path)

    # convert dict to string
    status_dict_str = json.dumps(modified_status_dict)

    # string with encoding 'utf-8'
    status_dict_str_bytes = bytes(status_dict_str, "utf-8")

    # encrypt the string
    encrypted_status_str = f.encrypt(status_dict_str_bytes)

    validation_status_file_path = str(
        metadata_path / Path(os.fsdecode(const.VALIDATION_STATUS_FILE_NAME))
    )

    if os.path.isfile(validation_status_file_path):
        # read the file and update -> `r+` mode
        with open(validation_status_file_path, "rb+") as validation_status_file:
            validation_status_file.write(encrypted_status_str)
    else:
        # opening file with `with` block closes the file at the end of with block
        # opening the file in w+ mode allows to both read and write files
        with open(validation_status_file_path, "wb+") as validation_status_file:
            validation_status_file.write(encrypted_status_str)


def get_dataset_level_schema(repo_id: str, schema_config: dict) -> dict:
    """Return the schema for the repo_id

    Args:
        repo_id (str): repo_id
        schema_config(dict): schema_config
    """
    omix_obj = OmixAtlas()
    schema_dict_tuple = omix_obj.get_schema(repo_id, return_type="dict")
    schema_dict_datasets = schema_dict_tuple.datasets
    schema_dict_datasets = (
        schema_dict_datasets.get("data", {}).get("attributes", {}).get("schema", {})
    )
    if schema_config:
        source = schema_config.get("source")
        datatype = schema_config.get("datatype")
        source_datatype_schema = schema_dict_datasets.get(source, {}).get(datatype, {})
        if not source_datatype_schema:
            raise paramException(
                title="param Error",
                detail=f"schema does not exist for the combination of source: {source} and "
                + f"datatype: {datatype} in the schema of repo_id: {repo_id}",
            )
        else:
            return source_datatype_schema
    elif not schema_config:
        # check if the schema_dict_datasets has only 1 source and datatype
        source_datatype_pairs = []
        for source_key, source_val in schema_dict_datasets.items():
            for datatype_key, datatype_val in source_val.items():
                # appending tuple of source and datatype in the list
                source_datatype_pairs.append((source_key, datatype_key))

        # if there are more than 1 source and datatype -> show error to the user
        # that the repo has multiple source and datatype -> then user must pass
        # a valid combination of source and datatype
        if len(source_datatype_pairs) > 1:
            raise paramException(
                title="param Error",
                detail=f"repo_id: {repo_id} has multiple source and datatypes. Please pass a valid  "
                + "source and datatype combination on which metadata needs to be validated.",
            )
        else:
            # list of tuples is source_datatype_pairs
            # In the list only 1 element is there and that is a tuple
            # accessing source and datatype from the tuple
            # PAIR is the best datastructure to represent the source and datatype pair
            # In python tuple is a pair of 2 elements so used tuple
            # dict cannot be used here as {source:datatype} as source not unique
            single_source_val = source_datatype_pairs[0][0]
            single_datatype_val = source_datatype_pairs[0][1]
            source_datatype_schema = schema_dict_datasets.get(
                single_source_val, {}
            ).get(single_datatype_val, {})
            return source_datatype_schema


def schema_config_check(schema_config: dict):
    """Schema config parameter check

    Args:
        schema_config (dict): Dictionary containing two keys
        source and datatype
    """
    if not isinstance(schema_config, dict):
        raise paramException(
            title="Param Error", detail="Schema config should be a dict"
        )
    else:
        # https://stackoverflow.com/questions/9623114/check-if-two-unordered-lists-are-equal
        # code used int this link -> set conversion is only done for comparison
        if set(schema_config.keys()) != set(const.SCHEMA_CONFIG_KEY_NAMES):
            raise paramException(
                title="Param Error",
                detail="schema_config dict should have source and datatype keys "
                + f"in the format {const.SCHEMA_CONFIG_FORMAT} ",
            )


def modify_status_dataset(status_dataset: dict, metadata_path: str) -> dict:
    """Modify the status dataset to also add the validation level
    Status Dataset Dict contains File Name and Validation Status Right now
    Args:
        status_dataset (dict):status dict of files
        validation_level (str):validation level passed by the user
    Returns
    """
    modified_status_dataset = {}
    metadata_file_list = omix_hlpr.metadata_files_for_upload(metadata_path)
    # metadata_directory = os.fsencode(metadata_path)

    for file in tqdm(metadata_file_list, desc="Generating Status File of Validation"):
        # file = file.decode("utf-8")
        # # skip hidden files and validation status file
        # if not file.startswith(".") and file != const.VALIDATION_STATUS_FILE_NAME:
        file_path = str(Path(metadata_path) / Path(os.fsdecode(file)))
        with open(file_path, "r") as file_to_upload:
            res_dict = json.load(file_to_upload)
            dataset_id = res_dict.get("dataset_id")
            if dataset_id in status_dataset:
                modified_status_dataset[dataset_id] = {}
                modified_status_dataset[dataset_id]["file_name"] = file
                # status dataset => {`dataset_id`: `status`}
                modified_status_dataset[dataset_id]["status"] = status_dataset[
                    dataset_id
                ]
    return modified_status_dataset


def construct_combined_metadata_for_validation(source_folder_path: dict) -> dict:
    """Construct Combined Metadata DataStructure
    List of metadata dictionaries grouped together on the basis of validation level
    Validation Lib Takes List of Metadata Dicts and validation level param
    That is the reason the grouping is created
    Args:
        source_folder_path (dict): Source folder path of data and metadata files.
    Returns:
        dict: {
            <validation_level> : [{..metadata dict 1...}, {{..metadata dict 1...},......]
        }
    """
    metadata_path = source_folder_path["metadata"]
    metadata_file_list = omix_hlpr.metadata_files_for_upload(metadata_path)
    combined_metadata_dict_list = {}
    try:
        for file in tqdm(
            metadata_file_list,
            desc="Combining Metadata Files for Validation",
        ):
            # file = file.decode("utf-8")
            # skip hidden files and validation status file
            # if not file.startswith(".") and file != const.VALIDATION_STATUS_FILE_NAME:
            file_path = str(Path(metadata_path) / Path(os.fsdecode(file)))
            with open(file_path, "r") as file_to_upload:
                res_dict = json.load(file_to_upload)
                # only put a file for validation
                # if validate is True in the metadata dict
                validate_val = (
                    res_dict.get("__index__", {})
                    .get("validation_check", {})
                    .get("dataset", {})
                    .get("validate", "")
                )
                check_for_validate_key_val(validate_val, file)
                if validate_val:
                    # validation level needed for grouping
                    # metadata dicts with same validation level
                    scope = (
                        res_dict.get("__index__", {})
                        .get("validation_check", {})
                        .get("dataset", {})
                        .get("scope", "")
                    )
                    if scope:
                        check_for_scope_key_val(scope, file)
                        # converting scope to validate_on param that needs to
                        # passed to validation library
                        validate_on_val = compute_validate_on_param(scope)
                        if validate_on_val in combined_metadata_dict_list:
                            combined_metadata_dict_list.get(validate_on_val).append(
                                res_dict
                            )
                        else:
                            combined_metadata_dict_list[validate_on_val] = []
                            combined_metadata_dict_list.get(validate_on_val).append(
                                res_dict
                            )
                    else:
                        # raise warning and skip
                        # validation config does not have scope defined for validation
                        warning_validation_scope_not_defined(file)
                else:
                    # raise warning -> validation config not correctly defined
                    # validation skipped for the file
                    warning_validation_config_incorrectly_defined(file)

        return combined_metadata_dict_list
    except Exception as err:
        raise err


def check_for_validate_key_val(validate_val, file):
    """check validate_val is of correct type

    Args:
        validate_val (): validate key val
        file : file where value defined
    """
    if not isinstance(validate_val, bool):
        raise paramException(
            title="Param Error",
            detail=f"validate key is set to incorrect type in {file}. Only boolean allowed",
        )


def check_for_scope_key_val(scope_val, file):
    """check for scope key correct type

    Args:
        scope_val (): scope key val
        file : file where value defined
    """
    if scope_val not in const.VALIDATION_SCOPE_CONSTANTS:
        raise paramException(
            title="Param Error",
            detail=f"scope key is set to incorrect type/val in {file}. "
            + f"Only {const.VALIDATION_SCOPE_CONSTANTS} allowed.",
        )


def get_indexing_configs():
    """Get Indexing Configs default value"""
    indexing_configs_dict = {}
    indexing_configs_dict["file_metadata"] = True
    indexing_configs_dict["col_metadata"] = True
    indexing_configs_dict["row_metadata"] = True
    indexing_configs_dict["data_required"] = True
    return indexing_configs_dict


def get_dataset_level_validation_config():
    """Get dataset level validation config"""
    dataset = {}
    dataset["validate"] = True
    dataset["scope"] = "advanced"
    dataset["force_ingest"] = False
    return dataset


def get_sample_level_validation_configs():
    """Get sample level validation config"""
    sample = {}
    sample["validate"] = True
    sample["scope"] = "advanced"
    sample["force_ingest"] = False
    return sample


def warning_validation_scope_not_defined(file: str):
    """Warning to show when validation scope is not present in validation config
    Args:
        file (str): file that needs to be validated
    """
    warnings.formatwarning = lambda msg, *args, **kwargs: f"WARNING: {msg}\n"
    warnings.warn(
        f"Unable to validate metadata file: {file} "
        + " because the validation_config key did not have scope defined for dataset level. "
        + "Please use `get_ingestion_configs` to get ingestion_configs in the right format. "
        + "For any questions, please reach out to polly.support@elucidata.io. "
    )
    print("\n")


def warning_validation_config_incorrectly_defined(file: str):
    """Warning to show when validation config is incorrect in the
    file
    Args:
        file(str): file that needs to be validated
    """
    warnings.formatwarning = lambda msg, *args, **kwargs: f"WARNING: {msg}\n"
    warnings.warn(
        f"Unable to validate metadata file: {file} "
        + " because the validation_config keys were not present in the right format. "
        + "Please use `get_ingestion_configs` to get ingestion_configs in the right format. "
        + "For any questions, please reach out to polly.support@elucidata.io. "
    )
    print("\n")


def compute_validate_on_param(validation_level: str) -> str:
    """Compute validate_on param based on validation level
    Args:
        validation_level (str): Passed by the user
    Returns:
        str: returns validation_on parameter
    """
    validation_level_const = copy.deepcopy(const.VALIDATION_LEVEL_CONSTANTS)
    validation_on_val = validation_level_const.get(validation_level, "")
    if not validation_on_val:
        keys = [key for key, val in validation_level_const.items()]
        raise paramException(
            detail=f"Incorrect value of validation_level param. It can be one of {keys}"
        )
    return validation_on_val


def data_metadata_parameter_check(source_folder_path: dict):
    """Sanity Check for Data and Metadata path parameters in source folder path
    Both the data and metadata keys need not be present.
    The data that has to be validated must be present.
    As this function is common for both dataset level and sample level validation
    Passing both data and metadata keys are optional. It is on user to pass
    the relevant data and metadata paths for validation
    Args:
        source_folder_path (dict): dictionary containing data and metadata paths
    """
    if not isinstance(source_folder_path, dict):
        raise paramException(
            title="Param Error", detail="source_folder_paths needs to a dict"
        )

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
