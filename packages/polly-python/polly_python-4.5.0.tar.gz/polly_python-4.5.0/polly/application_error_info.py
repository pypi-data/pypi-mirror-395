PARAM_EXCEPTION = "parameter passed is either empty or wrong datatype"
PARAM_EXCEPTION_TITLE = "parameter error"

WRONG_PARAMS_EXCEPTION = "Incorrect value of param passed"
WRONG_PARAMS_EXCEPTION_TITLE = "parameter error"


VALIDATION_ERROR = "Entity Passed has Failed Validation"
VALIDATION_ERROR_TITLE = "Validation Failed"

API_ERROR_EXCEPTION_TITLE = "API ERROR"
API_ERROR_EXCEPTION = ""

INCORRECT_DATA = "Data is Incorrect"

BAD_REQUEST_CODE = "bad_req"
BAD_REQUEST_TITLE = "Bad Request"
BAD_REQUEST_DETAIL = "Server could not understand the request due to invalid" " syntax"


FORBIDDEN_CODE = "forbidden"
FORBIDDEN_TITLE = "Access denied"
FORBIDDEN_DETAIL = "Access denied for requested resource"

NOT_FOUND_CODE = "resource_not_found"
NOT_FOUND_TITLE = "Resource not found"
NOT_FOUND_DETAIL = "Requested resource does not exist"

INVALID_PAYLOAD_CODE = "invalid_payload"
INVALID_PAYLOAD_TITLE = "Invalid Payload"
INVALID_PAYLOAD_DETAIL = "Parameters passed into the request are" "invalid or missing"

BAD_GATEWAY_CODE = "bad_gateway"
BAD_GATEWAY_TITLE = "Received an invalid response from the upstream service"

GATEWAY_TIMEOUT_CODE = "gateway_timeout"
GATEWAY_TIMEOUT_TITLE = "Gateway Timeout"
GATEWAY_TIMEOUT_DETAIL = "Request timed out"

EMPTY_PAYLOAD_CODE = "bad_req"
EMPTY_PAYLOAD_TITLE = "no payload found"
EMPTY_PAYLOAD_DETAIL = "Server could not understand the request due to invalid syntax"

INVALID_MODEL_NAME_TITLE = "doesn't exist"
JSON_SCHEMA_REQUEST_ERROR_DETAIL = (
    "Schema error in the json request file; update and try again"
)

REPOSITORY_LOCKED = "Repository Locked"
REPOSITORY_LOCKED_DETAIL = (
    "Your schema update is in progress. During this the repository has been locked for any data changes. "
    + "Please refer to the ingestion monitoring dashboard for visibility on this process. "
    + "Once completed, you can edit your datasets or schema. "
)

PAYLOAD_MAX_OUT_TITLE = "Payload too large"
