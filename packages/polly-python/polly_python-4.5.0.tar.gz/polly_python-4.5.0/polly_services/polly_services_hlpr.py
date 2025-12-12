import json
from polly.errors import error_handler, paramException, wrongParamException
from polly.tracking import Track


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

    if not isinstance(repo_id, (str, int)):
        raise paramException(
            title="Param Error",
            detail=f"repo_id, {repo_id} should be str or int",
        )


def verify_repo_identifier(repo_identifier: str):
    """Verify if the repository_idenfier is repo_id for a repo

    Args:
        repo_identifier (str): Identifier of a repo
    """
    if not repo_identifier.isdigit():
        raise paramException(
            title="Param Error",
            detail="Value of repo_id key in the schema payload dict is not valid repo_id. "
            + "repo_id should contain digits only. Please correct it.",
        )


def compare_repo_id_and_id(repo_id: str, id: str):
    """Repo id in the schema payload and the payload identifier(id) should be same
    id is the payload identifier as per JSON schema spec conventions.

    Args:
        repo_id (str): repo_id of the repo
        id (str): payload identifier of the schema payload
    """
    if repo_id != id:
        raise paramException(
            title="Param Error",
            detail="Value of repo_id key and id key is not same in the payload or "
            + "Value of repo_key in the parameter and repo_id in the payload not same. "
            + "Please correct it. ",
        )


def get_omixatlas(polly_session, repo_key: str):
    """get details of an omixatlas

    Args:
        polly_session (session_object): polly session object
        repo_key (str): repo key for the omixatlas
    """
    if repo_key and isinstance(repo_key, str):
        url = f"{polly_session.resource_url}/{repo_key}"
        response = polly_session.session.get(url)
        error_handler(response)
        return response.json()
    else:
        raise paramException(
            title="param error", detail="repo_id is either empty or not string"
        )


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


@Track.track_decorator
def omixatlas_summary(
    polly_session,
    repo_key: str,
    query_api_version="v2",
    count_by_source=True,
    count_by_data_type=True,
):
    """
    This function will return you a object that contain summary of a given Omixatlas.\
    Please use the function with the default values for optional parameters.
    Args:
        repo_key (str): repo_id or repo_name.
        query_api_version (str, optional): query api version
        count_by_source (bool, optional): count by source
        count_by_data_type (bool, optional): count by data_type
    Returns:
        It will return a JSON object. (see examples)

    Raises:
        wrongParamException: invalid paramter passed.
    """

    url = f"{polly_session.resource_url}/{repo_key}"
    if query_api_version == "v2":
        if count_by_source and count_by_data_type:
            params = {
                "summarize": "true",
                "v2": "true",
                "count_by_source": "true",
                "count_by_data_type": "true",
            }
        elif count_by_source:
            params = {"summarize": "true", "v2": "true", "count_by_source": "true"}
        elif count_by_data_type:
            params = {
                "summarize": "true",
                "v2": "true",
                "count_by_data_type": "true",
            }
        else:
            params = {
                "summarize": "true",
                "v2": "true",
            }
    elif query_api_version == "v1":
        params = {"summarize": "true"}
    else:
        raise wrongParamException("Incorrect query param version passed")
    if params:
        response = polly_session.session.get(url, params=params)
    error_handler(response)
    return response.json()


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
