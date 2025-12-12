from pydantic import (
    BaseModel,
    constr,
    create_model,
    field_validator,
    ValidationError,
    conint,
    ValidationInfo,
)
from typing import Optional
import pandas as pd
import copy
from enum import Enum
import re
from polly.constants import DDL_CONST_LIST, DML_CONST_LIST, FIELD_NAME_LOC


class FieldType(str, Enum):
    Boolean = "boolean"
    Integer = "integer"
    Float = "float"
    Text = "text"
    Object = "object"

    def __str__(self) -> str:
        return self.value


class AttributeModel(BaseModel):
    original_name: constr(strict=True, min_length=1, max_length=50)
    type: FieldType
    is_keyword: Optional[bool] = None
    is_array: Optional[bool] = None
    is_column: Optional[bool] = None
    is_curated: Optional[bool] = None
    is_searchable: Optional[bool] = None
    filter_size: conint(ge=1, le=3000) = 500
    display_name: constr(strict=True, min_length=1, max_length=50)
    description: constr(strict=True, min_length=1, max_length=300)
    is_ontology: Optional[bool] = None
    is_filter: Optional[bool] = None

    @field_validator("is_filter")
    @classmethod
    def is_filter_check(cls, is_filter, info: ValidationInfo):
        values = info.data
        if is_filter:
            if not values.get("is_keyword"):
                raise ValueError(
                    f'is_keyword is False and is_filter is True for {values["original_name"]}'
                )
        if values.get("is_ontology", False):
            if not is_filter:
                raise ValueError(
                    f'is_filter is False and is_ontology is True for {values["original_name"]}'
                )
            if not values["is_keyword"]:
                raise ValueError(
                    f'is_keyword is False and is_ontology is True  for {values["original_name"]}'
                )
        return is_filter


def _check_field_name(cls, field_name):
    """
    Check the field name passed in the schema.
    Rules on which it is validated are
    1. Lowercase only
    2. Start with alphabets
    3. Cannot include special characters except `_`
    4. Cannot be longer than 255 characters
    5. Cannot be SQL reserved DDL and DML keywords
    """
    field_name_size = len(field_name)
    if field_name_size < 1 or field_name_size > 255:
        raise ValueError(
            "Size of field name greater than 255 characters or less than 1"
        )

    # regex pattern
    # alphabets character at start
    # no whitespace and special characters in between
    # underscores allowed in between and end
    pattern = r"^[a-z]+[a-z0-9_]*$"
    res = re.match(pattern, field_name)
    if not res:
        raise ValueError(
            f"The field name {field_name} did not match the defined naming conditions. "
            + "Lowercase only, Start with alphabets,  Cannot include special characters except `_`, "
            + "Cannot be longer than 255 characters, Cannot be SQL reserved DDL and DML keywords."
        )

    ddl_consts = [x.lower() for x in DDL_CONST_LIST]
    dml_consts = [x.lower() for x in DML_CONST_LIST]

    if field_name in ddl_consts:
        raise ValueError(f"The field name {field_name} matches reserved DDL Constants.")

    if field_name in dml_consts:
        raise ValueError(f"The field name {field_name} matches reserved DML Constants.")

    return field_name


def _build_schema_validation_model(field_name: str, validators):
    """
    Return a schema validation model using pydantic create model
    """
    schema_model = create_model(
        "SchemaValidation",
        field_name=(str, ...),
        __validators__=validators,
        __base__=AttributeModel,
    )
    return schema_model


def _validate_schema_values(field_dict: dict):
    """
    Create pydantic model to validate schema values
    """
    field_name = field_dict["field_name"]

    # Create a field_validator for the field_name in V2 style
    def check_field_name_wrapper(cls, value):
        return _check_field_name(cls, value)

    validators = {
        "check_field_name": field_validator("field_name")(
            classmethod(check_field_name_wrapper)
        )
    }
    schema_model = _build_schema_validation_model(field_name, validators)
    try:
        schema_model(**field_dict)
    except ValidationError as s_errors:
        error_data_list = []
        for error in s_errors.errors():
            error_data = {"field_name": field_name}
            # getting 1st element from tuple loc
            # which contains location of the error
            if len(error.get("loc")) > 0:
                error_loc = error.get("loc")[0]
            else:
                error_loc = ""
            if error_loc == FIELD_NAME_LOC:
                error_data["attribute"] = "Not Applicable"
            else:
                attribute_name = error_loc
                error_data["attribute"] = attribute_name
            error_data["message"] = error.get("msg")
            error_data_list.append(error_data)
        schema_errors = pd.DataFrame(error_data_list)
        return schema_errors


def check_schema_for_errors(fields_dict: dict, source: str, datatype: str):
    """
    Check list of field dictionaries for possible errors
    """
    errors_all = []
    for field_dict_key, field_dict_attributes in fields_dict.items():
        field_dict = {}
        field_dict = copy.deepcopy(field_dict_attributes)
        field_dict["field_name"] = field_dict_key
        errors = _validate_schema_values(field_dict)
        if errors is not None:
            errors_all.append(errors)

    if errors_all:
        error_df = pd.concat(errors_all, ignore_index=True)
        error_df.insert(0, "Source", source)
        error_df.insert(1, "Datatype", datatype)
        return error_df
    else:
        error_df = pd.DataFrame()
        return error_df
