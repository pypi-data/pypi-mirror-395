import sys
from polly import application_error_info as app_err_info
from polly import http_response_codes as http_res_codes

# setting stack trace to default
sys.tracebacklimit = 1000


class RequestException(Exception):
    def __init__(self, title, detail=None):
        self.title = title
        self.detail = detail


class BaseExceptionError(Exception):
    """
    Base Exception class for v2 APIs.
    All custom exceptions are created by extending this class.
    Exception has 4 attributes corresponding to details sent in 'error' object
    in response JSON -
        status - http status code
        code - application specific error code
        title - title of error
        detail - details of error
    """

    def __init__(self, status, code, title, detail):
        Exception.__init__(self)
        self.title = title
        self.detail = detail

    def as_dict(self):
        return {"title": self.title, "detail": self.detail}

    def as_str(self):
        exception_str = "Exception Type : " + self.__class__.__name__
        exception_str += "\nTitle - " + self.title if self.title else ""
        exception_str += "\nDetails - " + self.detail if self.detail else ""
        return exception_str

    def __str__(self):
        return f"{self.__class__.__name__} ({self.title}): {self.detail}"


class ElasticException(Exception):
    def __str__(self):
        if self.detail:
            return f"{self.title}: {self.detail}"
        return self.title


class UnauthorizedException(Exception):
    def __str__(self):
        return "Expired or Invalid Token"


class ValidationError(Exception):
    detail = app_err_info.VALIDATION_ERROR

    def __init__(self, title=None, detail=None):
        self.title = app_err_info.WRONG_PARAMS_EXCEPTION_TITLE
        if detail:
            self.detail = detail


class UnfinishedQueryException(Exception):
    def __init__(self, query_id):
        self.query_id = query_id

    def __str__(self):
        return f'Query "{self.query_id}" has not finished executing'


class QueryFailedException(Exception):
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return f"Query failed to execute\n\treason: {self.reason}"


class OperationFailedException(Exception):
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return f"{self.reason}"


class InvalidPathException(Exception):
    def __str__(self):
        return "This path does not represent a file or a directory. Please try again."


class InvalidDirectoryPathException(Exception):
    def __str__(self):
        return "This path does not represent an existing directory. Please try again."


class RequestFailureException(Exception):
    def __str__(self):
        return "Sorry, we're unable to fetch the metadata now. Please contact polly.support@elucidata.io"


class InvalidDatatypeException(Exception):
    def __str__(self):
        return "Single Cell Datatype is not incorporated. Please contact Polly Support."


class MissingKeyException(Exception):
    def __init__(self, key):
        self.key = key

    def __str__(self):
        return f"Missing keys {self.key}"


class InvalidParameterException(Exception):
    def __init__(self, parameter):
        self.parameter = parameter

    def __str__(self):
        return f"Empty or Invalid Parameters = {self.parameter}."


class IncompatibleDataSource(Exception):
    def __init__(self, parameter):
        self.parameter = parameter

    def __str__(self):
        return f"The datasets cannot be added due to conflicting data sources = {self.parameter}."


class InvalidFormatException(Exception):
    def __str__(self):
        return "This file format is not supported."


class UnsupportedRepositoryException(Exception):
    def __str__(self):
        return "Report Generation feature is enabled for 'GEO' repository. Please try again."


class InvalidDirectoryPath(Exception):
    def __init__(self, parameter):
        self.parameter = parameter

    def __str__(self):
        return f" This path - '{self.parameter}' does not represent a directory. Please try again."


class InvalidWorkspaceDetails(Exception):
    def __str__(self):
        return "Workspace path should start with 'polly://'. Please enter the arguments correctly and try again. "


class paramException(BaseExceptionError):
    detail = app_err_info.PARAM_EXCEPTION

    def __init__(self, title=None, detail=None):
        self.title = app_err_info.PARAM_EXCEPTION_TITLE
        if detail:
            self.detail = detail


class wrongParamException(BaseExceptionError):
    detail = app_err_info.WRONG_PARAMS_EXCEPTION

    def __init__(self, title=None, detail=None):
        self.title = app_err_info.WRONG_PARAMS_EXCEPTION_TITLE
        if detail:
            self.detail = detail


class apiErrorException(BaseExceptionError):
    detail = app_err_info.API_ERROR_EXCEPTION

    def __init__(self, title=None, detail=None):
        self.title = app_err_info.API_ERROR_EXCEPTION_TITLE
        if detail:
            self.detail = detail


class invalidDataException(BaseExceptionError):
    def __init__(self, title=None, detail=None):
        self.title = app_err_info.INCORRECT_DATA
        if detail:
            self.detail = detail


class invalidApiResponseException(BaseExceptionError):
    def __init__(self, title=None, detail=None):
        if title:
            self.title = title
        if detail:
            self.detail = detail


class BadRequestError(BaseExceptionError):
    status = http_res_codes.BAD_REQUEST
    code = app_err_info.BAD_REQUEST_CODE
    title = app_err_info.BAD_REQUEST_TITLE
    detail = app_err_info.BAD_REQUEST_DETAIL

    def __init__(self, code=None, status=None, title=None, detail=None):
        if code:
            self.code = code
        if status:
            self.status = status
        if title:
            self.title = title
        if detail:
            self.detail = detail


class AccessDeniedError(BaseExceptionError):
    status = http_res_codes.FORBIDDEN
    code = app_err_info.FORBIDDEN_CODE
    title = app_err_info.FORBIDDEN_TITLE
    detail = app_err_info.FORBIDDEN_DETAIL

    def __init__(self, title=None, detail=None):
        if title:
            self.title = title
        if detail:
            self.detail = detail


class ResourceNotFoundError(BaseExceptionError):
    status = http_res_codes.NOT_FOUND
    code = app_err_info.NOT_FOUND_CODE
    title = app_err_info.NOT_FOUND_TITLE
    detail = app_err_info.NOT_FOUND_DETAIL

    def __init__(self, title=None, detail=None):
        if title:
            self.title = title
        if detail:
            self.detail = detail


class InvalidSchemaJsonException(Exception):
    def __str__(self):
        return "Schema error in the json request file; update and try again"


class InvalidSyntaxForRequestException(Exception):
    def __str__(self):
        return "Invalid syntax for this request was provided"


class EmptyPayloadException(Exception):
    def __str__(self):
        return "The specified payload could not be found. Inspect and try again."


class InvalidJobFunctionParameterException(Exception):
    def __init__(self, parameter):
        self.parameter = parameter

    def __str__(self):
        return (
            f"The specified {self.parameter} could not be found. Inspect and try again."
        )


class RepositoryNotFoundException(Exception):
    def __init__(self, parameter):
        self.parameter = parameter

    def __str__(self):
        return f"The specified repository: {self.parameter} could not be found in the schema. Please contact Polly Support."


class DatatypeNotFoundException(Exception):
    def __init__(self, parameter):
        self.parameter = parameter

    def __str__(self):
        return f"The specified datatype: {self.parameter} could not be found in the schema. Please contact Polly Support."


def error_handler(response):
    is_error, jsonResponse = has_error_message(response)
    if is_error:
        title, detail = extract_json_api_error(jsonResponse)
        if title == app_err_info.REPOSITORY_LOCKED:
            detail = app_err_info.REPOSITORY_LOCKED_DETAIL
        raise RequestException(title, detail)
    elif jsonResponse.status_code == 401:
        raise UnauthorizedException

    response.raise_for_status()


def has_error_message(response):
    try:
        for key in response.json().keys():
            if key in {"error", "errors"}:
                return True, response.json()
        for key in response.json()["data"].keys():
            if key in {"error", "errors"}:
                return True, response.json()["data"]
        return False, response
    except Exception:
        return False, response


def extract_json_api_error(response):
    error = response.get("error")
    if error is None:
        error = response.get("errors")[0]
    if "title" in error:
        title = error.get("title")
    if "detail" in error:
        detail = error.get("detail")
    return title, detail


def extract_error_message_details(error_response):
    error = error_response.json().get("error")
    if error is None:
        error = error_response.json().get("errors")[0]

    type_ = error.get("type", None) or error.get("code", None)
    reason = error.get("reason", None) or error.get("title", None)
    details = error.get("details", None) or error.get("detail", None)

    return type_, reason, details


def is_unfinished_query_error(exception):
    return isinstance(exception, UnfinishedQueryException)
