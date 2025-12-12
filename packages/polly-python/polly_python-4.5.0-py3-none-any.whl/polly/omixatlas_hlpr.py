import os
from functools import lru_cache
import requests
import json
from polly.errors import (
    paramException,
    extract_error_message_details,
    UnauthorizedException,
    EmptyPayloadException,
    InvalidSchemaJsonException,
    InvalidSyntaxForRequestException,
)

import pandas as pd
import polly.constants as const
from polly.errors import error_handler
import polly.helpers as helpers
import polly.http_response_codes as http_codes
from polly import application_error_info as app_err_info


# used in move data and delete dataset
def parameter_check_for_repo_id(repo_id):
    """Checking for validity of repo id
    Args:
        repo_id (): Repository Id of omixatlas

    Raises:
        paramException: Error if repo id is empty or is not str or int
    """
    if not repo_id:
        raise paramException(
            title="Param Error",
            detail="repo_id should not be empty",
        )
    elif type(repo_id) is not str and type(repo_id) is not int:
        raise paramException(
            title="Param Error",
            detail=f"repo_id, {repo_id} should be str or int",
        )


# used in validation
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


# used in delete dataset
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


# used in move_data
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


# used in lot of functions of base omixatlas
def str_params_check(str_params: list):
    """Checking if string parameters are of valid format
    Args:
        str_params (list): list of string parameters

    Raises:
        paramException: Error if any of string parameters are empty or is not str
    """
    for param in str_params:
        if not isinstance(param, str):
            raise paramException(
                title="Param Error", detail=f"{param} should be a string"
            )


# used in delete dataset
def make_repo_id_string(repo_id: int) -> str:
    """If repo id is int, change to string

    Args:
        repo_id (int/str): repo_id of the omixatlas

    Returns:
        str: return repo_id as string
    """
    if isinstance(repo_id, int):
        repo_id = str(repo_id)
    return repo_id


def create_move_data_payload(
    payload_datasets: list, src_repo_key: str, dest_repo_key: str, priority: str
) -> dict:
    """_summary_

    Args:
        payload_datasets (list): _description_
        src_repo_key (str): _description_
        dest_repo_key (str): _description_
        priority (str): _description_
    Returns:
        Dict : Dictionary of the move data payload
    """
    move_data_payload = {}
    move_data_payload["data"] = {}
    move_data_payload["data"]["type"] = "ingestion-transaction"
    move_data_payload["data"]["attributes"] = {}
    move_data_payload["data"]["attributes"]["datasets"] = payload_datasets
    move_data_payload["data"]["attributes"]["source_repo_id"] = src_repo_key
    move_data_payload["data"]["attributes"]["destination_repo_id"] = dest_repo_key
    move_data_payload["data"]["attributes"]["priority"] = priority
    move_data_payload["data"]["attributes"]["flags"] = {}
    move_data_payload["data"]["attributes"]["flags"]["file_metadata"] = "true"
    move_data_payload["data"]["attributes"]["flags"]["col_metadata"] = "true"
    move_data_payload["data"]["attributes"]["flags"]["row_metadata"] = "true"
    move_data_payload["data"]["attributes"]["flags"]["data_required"] = "true"
    return move_data_payload


# used in move_data
def parameter_check_for_priority(priority: str):
    if not isinstance(priority, str) or priority not in ["low", "medium", "high"]:
        raise paramException(
            title="Param Error",
            detail="`priority` should be a string. Only 3 values are allowed i.e. `low`, `medium`, `high`",
        )


def move_data_params_check(
    src_repo_key: str, dest_repo_key: str, dataset_ids: list, priority: str
):
    """Check move data params

    Args:
        src_repo_key (str/int): source repo id
        dest_repo_key (str/int): destination repo id
        dataset_ids (list): List of dataset ids
        priority (str): priority of the operation
    """
    try:
        parameter_check_for_repo_id(src_repo_key)
        parameter_check_for_repo_id(dest_repo_key)
        parameter_check_for_priority(priority)
        parameter_check_for_list_dataset_ids(dataset_ids)
    except Exception as err:
        raise err


def check_create_omixatlas_parameters(
    display_name: str,
    description: str,
    repo_name: str,
    image_url: str,
    components: list,
    category: str,
    data_type: str,
    org_id: str,
    controls: dict,
):
    """Sanity check for Parameters passed in Create Method
    Args:
        display_name (str): Display name of the Omixatlas
        description (str): Description of the Omixatlas
        repo_name (str): proposed repo name for the omixatlas
        image_url (str): image url provided for the icon for the omixatlas
        components (list): components to be added in the omixatlas
        category (str): category definition of the omixatlas
        data_type(str): datatype of the omixatlas. By default it is None
        org_id(str): org id of the Organisation. By default it is empty
    """
    try:
        str_params = [display_name, description, repo_name, image_url]
        str_params_check(str_params)
        check_components_parameter(components)
        check_controls_parameter(controls)

        if not isinstance(category, str) or (
            category not in const.OMIXATLAS_CATEGORY_VALS
        ):
            raise paramException(
                title="Param Error",
                detail=f"category should be a string and its value must be one of {const.OMIXATLAS_CATEGORY_VALS}",
            )
        check_org_id(org_id)
        check_data_type_parameter(data_type)
    except Exception as err:
        raise err


def check_org_id(org_id: str):
    """Sanity check for org id

    Args:
        org_id (str): org id of the Organisation. By default it is empty
    """
    if org_id:
        if not isinstance(org_id, str):
            raise paramException(
                title="Param Error",
                detail="org id should be a string.",
            )


def check_data_type_parameter(data_type: str):
    """Check for data type parameter

    Args:
        data_type (str): datatype of the omixatlas. By default it is None
    """
    if data_type:
        if not isinstance(data_type, str) or (
            data_type not in const.OMIXATLAS_DATA_TYPE_VALS
        ):
            raise paramException(
                title="Param Error",
                detail=(
                    "data_type should be a string and its value must be one of "
                    + f"{const.OMIXATLAS_DATA_TYPE_VALS}"
                ),
            )


def check_components_parameter(components: list):
    """Check components parameter

    Args:
        components (list): components to be added in the omixatlas
    """
    if not isinstance(components, list):
        raise paramException(
            title="Param Error", detail=f"{components} should be a list"
        )


def check_controls_parameter(controls: dict):
    """Check controls parameter

    Args:
        controls (dict): UI controls to be added in the omixatlas
    """
    if not isinstance(controls, dict):
        raise paramException(
            title="Param Error", detail=f"{controls} should be a dictionary"
        )


def check_update_omixatlas_parameters(
    display_name: str,
    description: str,
    repo_key: str,
    image_url: str,
    components: list,
    workspace_id: str,
    controls: dict,
):
    """Sanity check for Parameters passed in Update Method
    Args:
        display_name (str): Display name of the Omixatlas
        description (str): Description of the Omixatlas
        repo_name (str): proposed repo name for the omixatlas
        image_url (str): image url provided for the icon for the omixatlas
        components (list): components to be added in the omixatlas
        workspace_id (str): ID of the Workspace to be linked to the Omixatlas.
        data_type(str): datatype of the omixatlas. By default it is None
    """
    try:
        parameter_check_for_repo_id(repo_key)
        # this can be refactored using args -> just passing **args into the function
        # have a discussion on this
        if (
            not display_name
            and not description
            and not image_url
            and not components
            and not workspace_id
            and not controls
        ):
            raise paramException(
                title="Param Error",
                detail=(
                    "No parameters passed to update, please pass at least one of the following"
                    + " params [display_name, description, image_url, components, workspace_id, data_type]."
                ),
            )

        str_params = [display_name, description, image_url, workspace_id]
        str_params_check(str_params)
        check_components_parameter(components)
        check_controls_parameter(controls)
    except Exception as err:
        raise err


# TODO -> can we remove this function altogether
# and use extract_error_message_details in errors module
# to follow the DRY principle
# extract_error_message should be at only 1 place and should be generic enough
# to handle all the cases
def extract_error_message(error_msg) -> str:
    """
    Extract error message from the error
    """
    error_msg = json.loads(error_msg)
    error = error_msg.get("error")
    if error is None:
        error = error_msg.get("errors")[0]
    if "detail" in error:
        detail = error.get("detail")

    if "title" in error:
        title = error.get("title")

    error_msg_dict = {"title": title, "detail": detail}

    return error_msg_dict


# used in delete dataset and other places also
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


# used in delete dataset and other places also
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


# used in delete dataset and other places also
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
# cached for the cases when this function is called internally when same
# result is needed multiple times


# this function is also used by Vivek -> don't remove this function and related functions
@lru_cache(maxsize=None)
def list_files(
    self, repo_id: str, metadata="true", data="true", version="current"
) -> list:
    """helper function to integrate list files API response

    Args:
        self (polly_session_object): polly_session
        repo_id (str): repo id of the omixatlas
    Returns:
        list_files_resp -> list of objects with requests type
    """
    # endpoints for list files API
    files_api_endpoint = f"{self.discover_url}/repositories/{repo_id}/files"

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
            next_endpoint = f"{self.discover_url}{next_link}"
            response = self.session.get(next_endpoint)

            if response.status_code == http_codes.PAYLOAD_TOO_LARGE:
                page_after = extract_page_after_from_next_link(next_link)
                list_api_crash_messaging_tracking(self, page_after, default_page_size)

                default_page_size = reduce_page_size(
                    default_page_size, reduction_percentage
                )
                helpers.debug_print(
                    self, f"--reduced page size---: {default_page_size}"
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

            response = self.session.get(files_api_endpoint, params=query_params)
            # in case of payload too large error, reduce the page size
            if response.status_code == http_codes.PAYLOAD_TOO_LARGE:
                list_api_crash_messaging_tracking(self, page_after, default_page_size)

                default_page_size = reduce_page_size(
                    default_page_size, reduction_percentage
                )

                helpers.debug_print(
                    self, f"--reduced page size---: {default_page_size}"
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
        helpers.debug_print(self, f"next link--: {next_link}")
    return responses_list


# used in delete dataset and other places
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


def check_params_for_get_metadata(repo_key, dataset_id, table_name):
    """
    Args:
        repo_key(str): repo_name/repo_id of the repository.
        dataset_id(str): dataset_id of the dataset.
        table_name(str): table name for the desired metadata, 'samples' supported for now.
    """
    if not (repo_key and (isinstance(repo_key, str) or isinstance(repo_key, int))):
        raise paramException(
            title="Param Error",
            detail="Argument 'repo_key' is either empty or invalid. \
It should either be a string or an integer. Please try again.",
        )
    if not (dataset_id and isinstance(dataset_id, str)):
        raise paramException(
            title="Param Error",
            detail="Argument 'dataset_id' is either empty or invalid. It should be a string. Please try again.",
        )
    if not (table_name and isinstance(table_name, str)):
        raise paramException(
            title="Param Error",
            detail="Argument 'table_name' is either empty or invalid. It should be a string. Please try again.",
        )
    if table_name.lower() not in const.TABLE_NAME_SAMPLE_LEVEL_INDEX_MAP:
        raise paramException(
            title="Param Error",
            detail=const.ERROR_MSG_GET_METADATA,
        )


def param_check_download_dataset(
    repo_key: str, dataset_ids: list, folder_path: str
) -> None:
    parameter_check_for_list_dataset_ids(dataset_ids)
    if not (repo_key and isinstance(repo_key, str)):
        raise paramException(
            title="Param Error",
            detail="repo_key (either id or name) is required and should be a string",
        )
    if (not isinstance(folder_path, str)) or (not os.path.isdir(folder_path)):
        raise paramException(
            title="Param Error",
            detail="folder_path if provided should be a string and a valid folder path.",
        )


def handle_elastic_discover_api_error(response):
    if response.status_code == http_codes.UNAUTHORIZED:
        raise UnauthorizedException("User is unauthorized to access this")
    elif response.status_code == http_codes.BAD_REQUEST:
        title, details = extract_error_message_details(response)
        if title == app_err_info.EMPTY_PAYLOAD_CODE:
            raise EmptyPayloadException()
        elif app_err_info.INVALID_MODEL_NAME_TITLE in title:
            raise InvalidSyntaxForRequestException()
    elif response.status_code == http_codes.INTERNAL_SERVER_ERROR:
        raise InvalidSchemaJsonException()
    else:
        (
            title,
            details,
        ) = extract_error_message_details(response)
        raise Exception("Exception Occurred :" + str(details))


def normalise_destination_path(self, destination_folder_path: str, repo_id: str) -> str:
    status_info = return_destination_folder_status(
        self, destination_folder_path, repo_id
    )
    pathExists = status_info[0]
    # if destination_folder does not exist, then normalise the path, otherwise not
    if not pathExists:
        destination_folder_path = return_normalise_destination_path(
            destination_folder_path
        )
    return destination_folder_path


def return_normalise_destination_path(destination_folder_path: str) -> str:
    normalised_path = os.path.normpath(destination_folder_path)
    return normalised_path


def return_destination_folder_status(
    self, destination_folder_path: str, repo_id: str
) -> tuple:
    """
    Function to check if the destination_folder_path already exist.
    Args:
        destination_folder_path (str): destination folder passed
        repo_id(str): repo_id of the repository
    """
    list_oa_response = list_files(self, repo_id, metadata=False)
    oa_data_files_list = []
    for response in list_oa_response:
        response_json = response.json()
        response_data = response_json.get("data")
        for item in response_data:
            file_id = item.get("id")
            oa_data_files_list.append(file_id)

    valid_folder_list = helpers.get_folder_list_from_list_of_filepaths(
        oa_data_files_list
    )

    # return status(whether destination_folder_path exists or not) and valid_folder_list as a tuple

    if destination_folder_path not in valid_folder_list:
        return False, valid_folder_list
    return True, valid_folder_list


def check_params_for_fetch_quilt_metadata(repo_key, dataset_id):
    """
    Args:
        repo_key(str/int): repo_name/repo_id of the repository.
        dataset_id(str): dataset_id of the dataset.
    """
    if not (repo_key and (isinstance(repo_key, str) or isinstance(repo_key, int))):
        raise paramException(
            title="Param Error",
            detail="Argument 'repo_key' is either empty or invalid. \
It should either be a string or an integer. Please try again.",
        )
    if not (dataset_id and isinstance(dataset_id, str)):
        raise paramException(
            title="Param Error",
            detail="Argument 'dataset_id' is either empty or invalid. It should be a string. Please try again.",
        )


def return_sorted_dict(single_dict: dict) -> dict:
    """
    Function that takes in a dictionary and returns an alphabetically sorted dictionary,
    except for keys - dataset_id and src_dataset_id.
    If either/both of the two keys are present,it will get inserted in the beginning of the dictionary.
    """
    # checking presence of either of the dataset_id related cols in the df
    id_cols_present = set.intersection(
        set(["dataset_id", "src_dataset_id"]), set(single_dict.keys())
    )
    final_dict = {}
    if len(id_cols_present) == 0:
        # None of the two keys present, sort the dictionary
        final_dict = dict(sorted(single_dict.items()))
    elif len(id_cols_present) == 1:
        # Sort the dictionary except for the key that is present,
        # insert the key after the rest of the dict is sorted
        key = id_cols_present.pop()
        col_data = single_dict.pop(key)
        sorted_dict = dict(sorted(single_dict.items()))
        final_dict[key] = col_data
        # updating the dictionary to append the dataset keys first
        final_dict.update(sorted_dict)
    else:
        # Both the keys present, sort the rest of the dict and insert the keys at the beginning of the sorted dictionary.
        dataset_id_data = single_dict.pop("dataset_id")
        src_dataset_id_data = single_dict.pop("src_dataset_id")
        sorted_dict = dict(sorted(single_dict.items()))
        final_dict["dataset_id"] = dataset_id_data
        final_dict["src_dataset_id"] = src_dataset_id_data
        # updating the dictionary to append the dataset keys first
        final_dict.update(sorted_dict)
    return final_dict


def update_frontendinfo_value(
    frontendinfo_curr_data: dict,
    image_url: str,
    description: str,
    display_name: str,
    controls: dict,
) -> dict:
    if image_url:
        frontendinfo_curr_data["icon_image_url"] = image_url
    if description:
        frontendinfo_curr_data["description"] = description
    if display_name:
        frontendinfo_curr_data["display_name"] = display_name
    if controls:
        frontendinfo_curr_data["controls"] = controls
    return frontendinfo_curr_data


def repo_creation_response_df(original_response) -> pd.DataFrame:
    """
    This function is used to create dataframe from json reponse of
    creation api

    Args:
        | original response(dict): creation api response
    Returns:
        | DataFrame consisting of 6 columns
        | ["Repository Id", "Repository Name", "Display Name", "Description", "Category", "Datatype"]

    """
    response_df_dict = {}
    if original_response["data"]:
        if original_response["data"]["attributes"]:
            attribute_data = original_response["data"]["attributes"]
            response_df_dict["Repository Id"] = attribute_data.get("repo_id", "")
            response_df_dict["Repository Name"] = attribute_data.get("repo_name", "")
            response_df_dict["Category"] = attribute_data.get("category", "")
            if "data_type" in attribute_data:
                response_df_dict["Datatype"] = attribute_data.get("data_type", "")
            if attribute_data["frontend_info"]:
                front_info_dict = attribute_data["frontend_info"]
                response_df_dict["Display Name"] = front_info_dict.get(
                    "display_name", ""
                )
                response_df_dict["Description"] = front_info_dict.get("description", "")
    rep_creation_df = pd.DataFrame([response_df_dict])
    return rep_creation_df


def create_repo_name(display_name) -> str:
    """
    This function is used to repo_name from display_name
    Args:
        | display_name(str): display name of the omixatlas
    Returns:
        | Constructed repo name
    """
    repo_name = display_name.lower().replace(" ", "_")
    return repo_name
