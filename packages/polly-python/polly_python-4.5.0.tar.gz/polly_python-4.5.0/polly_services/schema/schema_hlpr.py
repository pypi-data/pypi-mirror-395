from polly.errors import paramException
from polly_services import polly_services_hlpr
import json
from polly_services.schema import schema_const as sc_const
from polly import constants as const
import copy
import pandas as pd
from collections import namedtuple
from polly.errors import wrongParamException, error_handler


def get_schema_param_check(
    repo_key: str, schema_level: list, source: str, data_type: str, return_type: str
):
    """Sanity check for get schema params

    Args:
        repo_key (str): _description_
        schema_level (list): _description_
        source (str): _description_
        data_type (str): _description_
    """
    try:
        polly_services_hlpr.parameter_check_for_repo_id(repo_key)
        if not isinstance(schema_level, list):
            raise paramException(
                title="Param Error",
                detail="schema_level should be a list",
            )
        str_params = [source, data_type]
        polly_services_hlpr.str_params_check(str_params)
        return_type_param_check(return_type)
    except Exception as err:
        raise err


def return_type_param_check(return_type: str):
    """
    get_schema parameters sanity check
    """
    if not isinstance(return_type, str):
        raise paramException(
            title="Param Error",
            detail="return_type should be a string",
        )

    return_type_vals = copy.deepcopy(const.GET_SCHEMA_RETURN_TYPE_VALS)

    if return_type not in return_type_vals:
        raise paramException(
            title="Param Error",
            detail=f"return_type take only two vals : {return_type_vals}",
        )


def schema_param_check(repo_key: str, body: dict):
    """Do sanity checks for the parameters passed in schema functions

    Args:
        repo_key (str): _description_
        body (dict): _description_
    Raises:
        paramError: In case of any issue with the parameter
    """
    try:
        if not body or not isinstance(body, dict):
            raise paramException(
                title="Param Error",
                detail="body should not be empty and it should be of type dict",
            )
        polly_services_hlpr.parameter_check_for_repo_id(repo_key)
    except Exception as err:
        raise err


def schema_update_replace_hlpr(polly_session, repo_key: str, body: dict):
    """Helper function for schema writing.
    => Sanity checks on body
    => prepare url
    => convert body to json

    Args:
        polly_session (_type_): _description_
        repo_key (str): _description_
        body (dict): _description_
    """
    try:
        repo_id = body.get("data").get("attributes").get("repo_id")
        repo_key = polly_services_hlpr.make_repo_id_string(repo_key)
        compare_repo_key_and_repo_id(polly_session, repo_key, repo_id)

        schema_type = body.get("data", "").get("attributes", "").get("schema_type", "")
        schema_base_url = f"{polly_session.discover_url}/repositories"
        schema_url = f"{schema_base_url}/{repo_key}/schemas/{schema_type}"
        body = json.dumps(body)
        return schema_url, body
    except Exception as err:
        raise err


def schema_write_result_hlpr(resp):
    """Print the appropriate status based on schema write result

    Args:
        resp (json): write response of schema put/patch operation
    """

    schema_update_verdict = (
        resp.get("data", {}).get("attributes", {}).get("schema_update_verdict", "")
    )
    # There are 3 cases for schema updation using patch or put operation
    # In case 1 -> if user changes attributes in the field
    # other than `original_name`, `type`, `is_array`, `is_keyword`
    # `is_searchable`
    # In those cases -> schema update is performed instantly
    # In the schema_update_verdict key -> value is none

    # In case 2 -> If user renames a field or drops a field
    # from the schema -> then schema updation job happens
    # In the schema_update_verdict key -> value is schema_update

    # In case 3 -> if for any field 1 of
    # `is_searchable`
    # `original_name`, `type`, `is_array`, `is_keyword` is changed
    # or a source or datatype is added or renamed or dropped
    # schema reingestion job takes place
    # In the schema_update_verdict key -> value is reingestion

    # SCHEMA_VERDICT_DICT
    # {"schema_update": SCHEMA_UPDATE_SUCCESS, "no_change": SCHEMA_NO_CHANGE_SUCCESS,
    # "reingeston": SCHEMA_REINGEST_SUCCESS}
    # if schema_update_verdict from API matches any of the keys in the dict then
    # its corresponding value will be printed

    schema_update_verdict_val = const.SCHEMA_VERDICT_DICT.get(schema_update_verdict, "")
    if schema_update_verdict_val:
        print(schema_update_verdict_val)
    else:
        print(const.SCHEMA_UPDATE_GENERIC_MSG)


def validate_schema_param_check(body: dict):
    """Do Sanity check for body passed for validate schema

    Args:
        body (dict): payload to be validated
    """

    if "data" not in body:
        raise paramException(
            title="Param Error",
            detail="schema_dict not in correct format, attributes key not present."
            + "Please recheck the schema dict format and values.",
        )

    data = body["data"]
    if "attributes" not in data:
        raise paramException(
            title="Param Error",
            detail="schema_dict not in correct format, attributes key not present."
            + "Please recheck the schema dict format and values.",
        )
    attributes = data["attributes"]
    if "repo_id" not in attributes:
        raise paramException(
            title="Param Error",
            detail="schema_dict not in correct format, repo_id key not present."
            + "Please recheck the schema dict format and values.",
        )

    if "schema" not in attributes:
        raise paramException(
            title="Param Error",
            detail="schema_dict not in correct format, schema key not present."
            + "Please recheck the schema dict format and values.",
        )


def compare_repo_key_and_repo_id(polly_session, repo_key: str, id: str):
    """Compare repo_key in params and repo_id in the payload
    if repo_key is repo_id => check the equality of repo_key and repo_id
    if repo_key is repo_name => fetch repo_id for the repo and then check equality

    Args:
        repo_key (str): repo_id/repo_name for the repository
        repo_id (str): repo_id in the payload
    """
    repo_id = ""
    if repo_key.isdigit():
        # repo_key is repo_id
        repo_id = repo_key
    else:
        # repo key is repo name
        # fetch the repo id
        repo_data = polly_services_hlpr.get_omixatlas(polly_session, repo_key)
        repo_id = repo_data["data"]["attributes"]["repo_id"]

    polly_services_hlpr.compare_repo_id_and_id(repo_id, id)


def get_schema_type_info(
    polly_session, repo_key: str, schema_level: list, data_type: str
) -> dict:
    """
    Return schema type dict for valid schema level or table name values
    Earlier when feature was first developed
    there were only two schema_level values ->  ["dataset", "sample"]

    But going furthers tables in the repo db were passed as arguments in schema level
    So as to support all the possible levels for the repo present in db

    To support the tables and also be backward compatibility with schema level,
    the function consists cases for both of them
    """

    # if schema level passed then return schema type accordingly
    if schema_level:
        schema_levels_const = copy.deepcopy(sc_const.schema_levels)
        schema_table_name_const = copy.deepcopy(sc_const.schema_table_names)

        # check if schema level parameter is a subset of schema_levels_const
        # a.issubset(b) => schema_level.issubset(schema_level_const)
        schema_levels_const_set = set(schema_levels_const)
        schema_table_name_const_set = set(schema_table_name_const)
        schema_level_set = set(schema_level)
        if schema_level_set.issubset(schema_levels_const_set):
            schema_type_dict = get_schema_type(schema_level, data_type)
        elif schema_level_set.issubset(schema_table_name_const_set):
            schema_type_dict = schema_table_name_schema_type_mapping(
                polly_session, repo_key, schema_level
            )
        else:
            raise paramException(
                title="Param Error",
                detail="schema_level input is incorrect. Use the query SHOW TABLES IN <repo_name>"
                + "to fetch valid table names for schema_level input",
            )
        # else if check schema level is subset of schema table names
        # else raise errors
    else:
        # return all the schema types, in the default condition
        # default condition is no schema level or table name passed by user
        schema_type_dict = schema_table_name_schema_type_mapping(
            polly_session, repo_key, schema_level
        )

    return schema_type_dict


def get_schema_type(schema_level: list, data_type: str) -> dict:
    """
    Compute schema_type based on data_type and schema_level
    Old Schema Level Value Mapping and New Schema Level Value Mapping
    Backward compatible

    Old Schema Level Value Mapping
    |  schema_level   --------    schema_type
    |  dataset       --------     file
    |  sample    --------      gct_metadata
    |  sample and  ------       h5ad_metadata
    |  single cell

    """
    if schema_level and isinstance(schema_level, list):
        if "dataset" in schema_level and "sample" in schema_level:
            if data_type != "single_cell" or data_type == "":
                schema_type_dict = {"dataset": "files", "sample": "gct_metadata"}
            elif data_type == "single_cell":
                schema_type_dict = {"dataset": "files", "sample": "h5ad_metadata"}
            else:
                raise wrongParamException(
                    title="Incorrect Param Error",
                    detail="Incorrect value of param passed data_type ",
                )
        elif "dataset" in schema_level or "sample" in schema_level:
            if "dataset" in schema_level:
                schema_type_dict = {"dataset": "files"}
            elif "sample" in schema_level:
                if data_type != "single_cell" or data_type == "":
                    schema_type_dict = {"sample": "gct_metadata"}
                elif data_type == "single_cell":
                    schema_type_dict = {"sample": "h5ad_metadata"}
                else:
                    raise wrongParamException(
                        title="Incorrect Param Error",
                        detail="Incorrect value of param passed data_type ",
                    )
        else:
            raise wrongParamException(
                title="Incorrect Param Error",
                detail="Incorrect value of param passed schema_level ",
            )
    else:
        raise paramException(
            title="Param Error",
            detail="schema_level is either empty or its datatype is not correct",
        )
    return schema_type_dict


def schema_table_name_schema_type_mapping(
    polly_session, repo_key: str, schema_table_names: list
) -> dict:
    """
    New Schema Level Value mapping
    |   Table Name  Schema Type
    |   datasets ----- file
    |   samples ----- gct_metadata
    |   features ---- gct_row_metadata
    |   samples_singlecell ---- h5ad_metadata
    """
    # all the table and index name mapping present
    # for the repo is fetched
    schema_base_url = f"{polly_session.discover_url}/repositories"
    schema_url = f"{schema_base_url}/{repo_key}/schemas"
    meta_true_query_param = "?meta=true"
    schema_mapping_url = f"{schema_url}{meta_true_query_param}"
    schema_mapping_info = polly_session.session.get(schema_mapping_url)
    error_handler(schema_mapping_info)
    schema_mapping_info = schema_mapping_info.json()
    # schema mapping info structure
    # table name, index name mapping dict fetched from it
    # {"data":{"type":"<type>", "repository_id":"<repo_id>", "attributes":{"schemas":{<schema-mapping>}}}}
    schema_mapping = schema_mapping_info.get("data").get("attributes").get("schemas")

    # if user has passed table names
    # then only those are filtered
    # from the table and index name mapping dict
    # else the whole mapping dict returnedß

    if schema_table_names:
        schema_mapping_res = {
            schema_table: schema_mapping[schema_table]
            for schema_table in schema_table_names
        }
    else:
        schema_mapping_res = schema_mapping

    return schema_mapping_res


def get_full_schema_payload_from_api(
    polly_session, repo_key: str, schema_type_dict: str
):
    """
    Get full schema payload from the API for the repo for the schema_tables in schema_type_dict
    """
    resp_dict = {}
    print("---schema type dict-----")
    print(schema_type_dict)
    schema_base_url = f"{polly_session.discover_url}/repositories"
    for schema_table_key, val in schema_type_dict.items():
        schema_type = val
        dataset_url = f"{schema_base_url}/{repo_key}/schemas/{schema_type}"
        resp = polly_session.session.get(dataset_url)
        error_handler(resp)
        resp_dict[schema_table_key] = resp.json()
    return resp_dict


def remove_links_key_in_schema_payload(schema_payload_dict: dict) -> dict:
    """
    Remove links key from the schema response
    """
    for schema_level_key, schema_level_value in schema_payload_dict.items():
        if "data" in schema_level_value:
            val_data_dict = schema_level_value.get("data", {})
            if "links" in val_data_dict:
                val_data_dict.pop("links", None)

    return schema_payload_dict


def return_schema_data(df_map: dict):
    """
    Return schema data as named tuple
    """
    Schema = namedtuple("Schema", (key for key, value in df_map.items()))
    return Schema(**df_map)


def get_schema_from_api(
    polly_session, repo_key: str, schema_type_dict: dict, source: str, data_type: str
) -> dict:
    """
    Gets the schema of a repo id for the given repo_key and
    schema_type definition at the top level

    repo_key (str) : repo id or repo name
    schema_type_dict (dictionary) : {schema_level:schema_type}
    example -> {'dataset': 'files', 'sample': 'gct_metadata'}

    {
        "data": {
            "id": "<REPO_ID>",
            "type": "schema",
            "attributes": {
                "schema_type": "files | gct_metadata | h5ad_metadata",
                "schema": {
                    ... field definitions
                }
            }
        }
    }
    """
    resp_dict = {}
    schema_base_url = f"{polly_session.discover_url}/repositories"
    summary_query_param = "?response_format=summary"
    filter_query_params = ""
    if source:
        if data_type:
            filter_query_params = f"&source={source}&datatype={data_type}"
        else:
            filter_query_params = f"&source={source}"
    if repo_key and schema_type_dict and isinstance(schema_type_dict, dict):
        for schema_table_key, val in schema_type_dict.items():
            schema_type = val
            if filter_query_params:
                dataset_url = (
                    f"{schema_base_url}/{repo_key}/"
                    + f"schemas/{schema_type}"
                    + f"{summary_query_param}{filter_query_params}"
                )
            else:
                dataset_url = f"{schema_base_url}/{repo_key}/schemas/{schema_type}{summary_query_param}"
            resp = polly_session.session.get(dataset_url)
            error_handler(resp)
            # print(f"----schema table key------: {schema_table_key}")
            # print("----resp-----")
            # print(resp.json())
            resp_dict[schema_table_key] = resp.json()
    else:
        raise paramException(
            title="Param Error",
            detail="repo_key and schema_type_dict are either empty or its datatype is not correct",
        )
    return resp_dict


def flatten_nested_schema_dict(nested_schema_dict: dict) -> dict:
    """
    Flatten the nested dict

    Args:
        schema:{
                 "<SOURCE>": {
                     "<DATATYPE>": {
                         "<FIELD_NAME>": {
                         "type": "text | integer | object",
                         "description": "string", (Min=1, Max=100)
                         },
                         ... other fields
                     }
                     ... other Data types
              }
                ... other Sources
        }

    Returns
        {
            'Source':source_list,
            'Datatype': datatype_list,
            'Field Name':field_name_list,
            'Field Description':field_desc_list,
            'Field Type': field_type_list
        }

    """
    reformed_dict = {}
    source_list = []
    data_type_list = []
    field_name_list = []
    field_description_list = []
    field_type_list = []
    is_curated_list = []
    is_array_list = []
    for outer_key, inner_dict_datatype in nested_schema_dict.items():
        for middle_key, inner_dict_fields in inner_dict_datatype.items():
            for inner_key, field_values in inner_dict_fields.items():
                source_list.append(outer_key)
                data_type_list.append(middle_key)
                field_name_list.append(inner_key)
                for key, value in field_values.items():
                    if key == "description":
                        field_description_list.append(field_values[key])
                    if key == "type":
                        field_type_list.append(field_values[key])
                    if key == "is_curated":
                        is_curated_list.append(field_values[key])
                    if key == "is_array":
                        is_array_list.append(field_values[key])

    reformed_dict["Source"] = source_list
    reformed_dict["Datatype"] = data_type_list
    reformed_dict["Field Name"] = field_name_list
    reformed_dict["Field Description"] = field_description_list
    reformed_dict["Field Type"] = field_type_list
    if is_curated_list:
        reformed_dict["Is Curated"] = is_curated_list
    reformed_dict["Is Array"] = is_array_list

    return reformed_dict


def nested_dict_to_df(schema_dict: dict) -> pd.DataFrame:
    """
    Convert flatten dict into df and print it

    Args:
        {
            'Source':source_list,
            'Datatype': datatype_list,
            'Field Name':field_name_list,
            'Field Description':field_desc_list,
            'Field Type': field_type_list
        }

    Returns:
        DataFrame

    """
    pd.options.display.max_columns = None
    pd.options.display.width = None
    multiIndex_df = pd.DataFrame.from_dict(schema_dict, orient="columns")
    # sort Field Name in an ascending order
    multiIndex_df.sort_values(by=["Field Name"], inplace=True, ignore_index=True)
    return multiIndex_df
