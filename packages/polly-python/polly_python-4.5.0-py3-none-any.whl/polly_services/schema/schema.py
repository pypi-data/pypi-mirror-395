from polly_interfaces.ISchema import ISchema
from polly.errors import error_handler
from polly import constants as const
import json
from polly import helpers
from polly_services import polly_services_hlpr
from polly_services.schema import schema_hlpr
from polly_services.schema.validate_schema_hlpr import check_schema_for_errors
import polly.http_response_codes as http_codes


class Schema(ISchema):
    def __init__(self):
        pass

    def insert_schema(self, polly_session, repo_key, body: dict):
        """Function to insert schema

        Args:
            polly_session (session_object): session_object containing session vars
            repo_key (str/int): repo_id of the omixatlas
            body (dict): payload of the schema
        """
        try:
            schema_hlpr.schema_param_check(repo_key, body)
            # validate payload
            error_df = self.validate_schema(polly_session, body)

            # if there are no errors in the schema payload
            # which means error df is empty then only proceed
            # with schema insert operation
            if error_df.empty:
                repo_id = body.get("data").get("attributes").get("repo_id")
                repo_key = polly_services_hlpr.make_repo_id_string(repo_key)
                schema_hlpr.compare_repo_key_and_repo_id(
                    polly_session, repo_key, repo_id
                )
                schema_base_url = f"{polly_session.discover_url}/repositories"
                schema_url = f"{schema_base_url}/{repo_key}/schemas"
                body = json.dumps(body)
                resp = polly_session.session.post(schema_url, data=body)
                error_handler(resp)
                if resp.status_code == http_codes.CREATED:
                    print(const.SCHEMA_INSERT_SUCCESS)
        except Exception as err:
            raise err

    def update_schema(self, polly_session, repo_key, body: dict):
        """Function to update the schema

        Args:
            polly_session (session_object): session_object containing session vars
            repo_key (str/int): repo_id of the omixatlas
            body (dict): payload of the schema
        """
        try:
            schema_hlpr.schema_param_check(repo_key, body)
            # validate payload
            error_df = self.validate_schema(polly_session, body)
            # if there are no errors in the schema payload
            # which means error df is empty then only proceed
            # with schema update operation
            if error_df.empty:
                schema_url, body = schema_hlpr.schema_update_replace_hlpr(
                    polly_session, repo_key, body
                )
                resp = polly_session.session.patch(schema_url, data=body)
                error_handler(resp)
                # converting requests output to JSON
                resp = resp.json()
                schema_hlpr.schema_write_result_hlpr(resp)
        except Exception as err:
            raise err

    def replace_schema(self, polly_session, repo_key, body: dict):
        """Function to replace the schema

        Args:
            polly_session (session_object): session_object containing session vars
            repo_key (str/int): repo_id of the omixatlas
            body (dict): payload of the schema
        """
        try:
            schema_hlpr.schema_param_check(repo_key, body)
            # validate payload
            error_df = self.validate_schema(polly_session, body)
            # if there are no errors in the schema payload
            # which means error df is empty then only proceed
            # with schema update operation
            if error_df.empty:
                schema_url, body = schema_hlpr.schema_update_replace_hlpr(
                    polly_session, repo_key, body
                )
                resp = polly_session.session.put(schema_url, data=body)
                error_handler(resp)
                # converting requests output to JSON
                resp = resp.json()
                schema_hlpr.schema_write_result_hlpr(resp)
        except Exception as err:
            raise err

    def validate_schema(self, polly_session, body: dict):
        """validate the schema

        Args:
            body (dict): payload of the schema
        """
        try:
            schema_hlpr.validate_schema_param_check(body)
            repo_identifier = body.get("data", "").get("attributes", "").get("repo_id")

            # only repo_id allowed in payload, repo_name not allowed in payload
            polly_services_hlpr.verify_repo_identifier(repo_identifier)

            id = body.get("data", "").get("id", "")

            # check for similarity in id and repo_identifier passed in payload
            polly_services_hlpr.compare_repo_id_and_id(repo_identifier, id)

            # to check if repo_identifier is a valid repo_id
            # if an atlas is present for the repo_identifier then only
            # it is a valid repo_id
            polly_services_hlpr.get_omixatlas(polly_session, repo_identifier)

            schema_dict = body.get("data", "").get("attributes", "").get("schema", "")
            errors_res_list = []

            # schema dict format
            # {"<src_1>":
            #       {"<dp1>":
            #           {"<field1>":{"<attribiutes>"}
            #           ...multiple fields
            #           }
            #           ...multiple dps
            #       }
            #       ...multiple sources
            # }
            for source, datatype in schema_dict.items():
                for datatype_key, datatype_val in datatype.items():
                    error_res = check_schema_for_errors(
                        datatype_val, source, datatype_key
                    )
                    errors_res_list.append(error_res)

            error_res_combined = helpers.merge_dataframes_from_list(errors_res_list)
            if error_res_combined.empty:
                print("Schema has no errors")
            else:
                print(
                    "Schema insert/update/replace/validate didn't go through because there are errors in "
                    + "the schema. Those errors is summarised in the table below: "
                )
                print("\n")
                print(error_res_combined.to_string(index=False))
            return error_res_combined

        except Exception as err:
            raise err

    def get_schema(
        self,
        polly_session,
        repo_key: str,
        schema_level=[],
        source="",
        data_type="",
        return_type="dataframe",
    ):
        """Function to get Schema

        Args:
            polly_session (_type_): _description_
            repo_key (_type_): _description_
            schema_level (list, optional): _description_. Defaults to [].
            source (str, optional): _description_. Defaults to "".
            data_type (str, optional): _description_. Defaults to "".
            return_type (str, optional): _description_. Defaults to "dataframe".

        Raises:
            err: _description_

        Returns:
            _type_: _description_
        """
        try:
            schema_hlpr.get_schema_param_check(
                repo_key, schema_level, source, data_type, return_type
            )

            # function signature made to abide by the interface
            schema_type_dict = schema_hlpr.get_schema_type_info(
                polly_session, repo_key, schema_level, data_type
            )

            if return_type == "dict":
                schema_payload_dict = schema_hlpr.get_full_schema_payload_from_api(
                    polly_session, repo_key, schema_type_dict
                )
                schema_payload_dict = schema_hlpr.remove_links_key_in_schema_payload(
                    schema_payload_dict
                )
                return schema_hlpr.return_schema_data(schema_payload_dict)
            else:
                schema = schema_hlpr.get_schema_from_api(
                    polly_session, repo_key, schema_type_dict, source, data_type
                )
                for key, val in schema.items():
                    # print("---schema-----")
                    # print(schema)
                    if schema[key]["data"]["attributes"]["schema"]:
                        schema[key] = schema[key]["data"]["attributes"]["schema"]

                df_map = {}
                for key, val in schema.items():
                    flatten_dict = schema_hlpr.flatten_nested_schema_dict(schema[key])
                    df_map[key] = schema_hlpr.nested_dict_to_df(flatten_dict)

                return schema_hlpr.return_schema_data(df_map)

        except Exception as err:
            raise err
