from functools import lru_cache
import gzip
import json
import warnings
import ssl
import logging
import os
import platform
import tempfile
from tempfile import TemporaryDirectory as TempDir
from pathlib import Path
from typing import Generator, Union
import pandas as pd
from joblib import Parallel, delayed
import requests
from retrying import retry
from polly.help import example
from polly import constants as const
from polly import helpers
from polly.auth import Polly
from tqdm import tqdm
from polly.constants import (
    DATA_TYPES,
    ERROR_MSG_GET_METADATA,
    TABLE_NAME_SAMPLE_LEVEL_INDEX_MAP,
)
from polly.errors import (
    QueryFailedException,
    UnfinishedQueryException,
    InvalidParameterException,
    error_handler,
    is_unfinished_query_error,
    paramException,
    wrongParamException,
    invalidApiResponseException,
    invalidDataException,
    InvalidPathException,
    InvalidDirectoryPathException,
    RequestFailureException,
)
from polly_services.schema.schema import Schema
from polly_services.reporting.reporting import Reporting
from polly_services.files.files import Files
import polly.omixatlas_hlpr as omix_hlpr

import polly.http_response_codes as http_codes
from polly.tracking import Track


class OmixAtlas:
    """
    OmixAtlas class enables users to interact with functional properties of the omixatlas such as
    create and update an Omixatlas, get summary of it's contents, add, insert, update the schema,
    add, update or delete datasets, query metadata, download data, save data to workspace etc.

    Args:
        token (str): token copy from polly.

    Usage:
        from polly.OmixAtlas import OmixAtlas

        omixatlas = OmixAtlas(token)
    """

    example = classmethod(example)

    def __init__(self, token=None, env="", default_env="polly") -> None:
        # check if COMPUTE_ENV_VARIABLE present or not
        # if COMPUTE_ENV_VARIABLE, give priority
        # added dummy commit
        env = helpers.get_platform_value_from_env(
            const.COMPUTE_ENV_VARIABLE, default_env, env
        )
        self.session = Polly.get_session(token, env=env)
        self.base_url = f"https://v2.api.{self.session.env}.elucidata.io"
        self.base_url_auth = f"https://apis.{self.session.env}.elucidata.io/auth"
        self.discover_url = f"https://api.discover.{self.session.env}.elucidata.io"
        self.elastic_url = (
            f"https://api.datalake.discover.{self.session.env}.elucidata.io/elastic/v2"
        )
        self.resource_url = f"{self.base_url}/v1/omixatlases"
        self.resource_url_search = (
            f"https://apis.{self.session.env}.elucidata.io/mithoo/_search"
        )

    @Track.track_decorator
    def get_all_omixatlas(
        self, query_api_version="v2", count_by_source=True, count_by_data_type=True
    ):
        """
        This function will return the summary of all the Omixatlas on Polly which the user has access to.
        Please use this function with default values for the paramters.

        Args:
            query_api_version (str): query api version
            count_by_source (bool): count by source
            count_by_data_type (bool): count by data type

        Returns:
            list: It will return a list of JSON objects. (See Examples)

        Raises:
            wrongParamException: invalid parameter passed
        """

        url = self.resource_url
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
        response = self.session.get(url, params=params)
        error_handler(response)
        return response.json()

    @Track.track_decorator
    def omixatlas_summary(
        self,
        repo_key: str,
        query_api_version="v2",
        count_by_source=True,
        count_by_data_type=True,
    ):
        """
        This function will return you a object that contain summary of a given Omixatlas.
        Please use the function with the default values for optional parameters.

        Args:
            repo_key (str): repo_id or repo_name.
            query_api_version (str, optional): query api version
            count_by_source (bool, optional): count by source
            count_by_data_type (bool, optional): count by data_type

        Returns:
            object: It will return a JSON object. (see examples)

        Raises:
            wrongParamException: invalid paramter passed.
        """

        url = f"{self.resource_url}/{repo_key}"
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
            response = self.session.get(url, params=params)
        error_handler(response)
        return response.json()

    # TODO -> Make this function private while refactoring
    # a copy of this function has been move to polly_services_hlpr
    # need a discussion to keep it at both places or 1 place
    # this function is required in base class as well as polly_services

    # used in move_data function
    def _get_omixatlas(self, key: str):
        """
        This function will return a omixatlas repository in polly.

        ``Args:``
            |  ``key:`` repo name or repo id.

        ``Returns:``
            It will return a objects like this.

            .. code::


                    {
                    'repo_name': 'repo',
                    'repo_id': '1646',
                    'indexes': {
                    'gct_metadata': 'repo_gct_metadata',
                        'h5ad_metadata': 'repo_h5ad_metadata',
                        'csv': 'repo_csv',
                        'files': 'repo_files',
                        'json': 'repo_json',
                        'ipynb': 'repo_ipynb',
                        'gct_data': 'repo_gct_data',
                        'h5ad_data': 'repo_h5ad_data'
                        },
                    'diseases': [],
                    'organisms': [],
                    'sources': [],
                    'datatypes': [],
                    'dataset_count': 0,
                    'disease_count': 0,
                    'tissue_count': 0,
                    'organism_count': 0,
                    'cell_line_count': 0,
                    'cell_type_count': 0,
                    'drug_count': 0,
                    'data_type_count': 0,
                    'data_source_count': 0,
                    'sample_count': 0,
                    'normal_sample_count': 0
                    }

        | To use this function import Omixatlas class and make a object.


        .. code::


                from polly.omixatlas import OmixAtlas
                omixatlas = OmixAtlas(token)
                # to use OmixAtlas class functions
                omixatlas.get_omixatlas('9')

        """
        if key and isinstance(key, str):
            url = f"{self.resource_url}/{key}"
            response = self.session.get(url)
            error_handler(response)
            return response.json()
        else:
            raise paramException(
                title="param error", detail="repo_id is either empty or not string"
            )

    @Track.track_decorator
    def query_metadata(
        self,
        query: str,
        experimental_features=None,
    ) -> pd.DataFrame:
        """
        This function will return a dataframe containing the SQL response.
        In cases of data intensive queries, the data returned can be very large to process and it might lead to kernel failure
        , where in the runtime memory is exhausted and the process haults.
        In order to access the data, there are two options in this case, either increase the kernel memory,
        or use the function query_metadata_iterator() that returns an iterator.
        The function usage can be looked up in the documentation mentioned here under the
        Polly Python section - "https://docs.elucidata.io/index.html".

        Args:
           query (str): sql query  on  omixatlas.
           experimental_features : this section includes in querying metadata <target>.

        Returns:
            It will return a dataframe that contains the query response.

        Raises:
            UnfinishedQueryException: when query has not finised the execution.
            QueryFailedException: when query failed to execute.
        """
        query_id = self._get_query_id(query, experimental_features)
        iterator_function = False
        return self._process_query_to_completion(query_id, iterator_function)

    @Track.track_decorator
    def query_metadata_iterator(
        self,
        query: str,
        experimental_features=None,
    ) -> Generator[dict, None, None]:
        """
        This function will return a Generator object containing the SQL response.

        Args:
           query (str) : sql query  on  omixatlas.
           experimental_features : this section includes in querying metadata <target>.

        Returns:
            It will return a generator object having the SQL response.

        Raises:
            UnfinishedQueryException: when query has not finised the execution.
            QueryFailedException: when query failed to execute.
        """
        query_id = self._get_query_id(query, experimental_features)
        iterator_function = True
        return self._process_query_to_completion(query_id, iterator_function)

    def _get_query_id(self, query, experimental_features) -> str:
        """
        Function to return query_id for the respective SQL query.
        """
        queries_url = f"{self.resource_url}/queries"
        queries_payload = {
            "data": {
                "type": "queries",
                "attributes": {
                    "query": query,
                    "query_api_version": const.QUERY_API_V2,
                    "query_results_format": "JSON",
                },
            }
        }
        if experimental_features is not None:
            queries_payload.update({"experimental_features": experimental_features})

        response = self.session.post(queries_url, json=queries_payload)
        error_handler(response)

        query_data = response.json().get("data")
        query_id = query_data.get("id")
        return query_id

    @retry(
        retry_on_exception=is_unfinished_query_error,
        wait_exponential_multiplier=500,  # Exponential back-off starting 500ms
        wait_exponential_max=10000,  # After 10s, retry every 10s
        stop_max_delay=900000,  # Stop retrying after 900s (15m)
    )
    def _process_query_to_completion(
        self, query_id: str, iterator_function: bool
    ) -> Union[pd.DataFrame, Generator[dict, None, None]]:
        queries_url = f"{self.resource_url}/queries/{query_id}"
        response = self.session.get(queries_url)
        error_handler(response)

        query_data = response.json().get("data")
        query_status = query_data.get("attributes", {}).get("status")
        if query_status == "succeeded":
            return self._handle_query_success(query_data, iterator_function)
        elif query_status == "failed":
            self._handle_query_failure(query_data)
        else:
            raise UnfinishedQueryException(query_id)

    def _handle_query_failure(self, query_data: dict):
        fail_msg = query_data.get("attributes").get("failure_reason")
        raise QueryFailedException(fail_msg)

    def _handle_query_success(
        self, query_data: dict, iterator_function: bool
    ) -> Union[pd.DataFrame, Generator[dict, None, None]]:
        query_id = query_data.get("id")

        details = []
        time_taken_in_ms = query_data.get("attributes").get("exec_time_ms")
        if isinstance(time_taken_in_ms, int):
            details.append("time taken: {:.2f} seconds".format(time_taken_in_ms / 1000))
        data_scanned_in_bytes = query_data.get("attributes").get("data_scanned_bytes")
        if isinstance(data_scanned_in_bytes, int):
            details.append(
                "data scanned: {:.3f} MB".format(data_scanned_in_bytes / (1024**2))
            )

        if details:
            detail_str = ", ".join(details)
            print("Query execution succeeded " f"({detail_str})")
        else:
            print("Query execution succeeded")

        return self._fetch_results_as_file(query_id, iterator_function)

    def _fetch_iterator_as_pages(
        self, query_id, page_size
    ) -> Generator[dict, None, None]:
        """
        Function to return generator for SHOW/DESC queries that is only possible using page_size.
        """
        first_page_url = (
            f"{self.resource_url}/queries/{query_id}" f"/results?page[size]={page_size}"
        )
        response = self.session.get(first_page_url)
        error_handler(response)
        result_data = response.json()
        rows = [row_data.get("attributes") for row_data in result_data.get("data")]
        # yielding data for the first time call
        for row in rows:
            yield row

        while (
            result_data.get("links") is not None
            and result_data.get("links").get("next") is not None
            and result_data.get("links").get("next") != "null"
        ):
            # subsequent call for next paginated data, if any
            next_page_url = self.base_url + result_data.get("links").get("next")
            response = self.session.get(next_page_url)
            error_handler(response)
            result_data = response.json()
            if result_data.get("data"):
                rows = [
                    row_data.get("attributes") for row_data in result_data.get("data")
                ]
                for row in rows:
                    yield row

    def _fetch_results_as_pages(self, query_id, page_size) -> pd.DataFrame:
        first_page_url = (
            f"{self.resource_url}/queries/{query_id}" f"/results?page[size]={page_size}"
        )
        response = self.session.get(first_page_url)
        error_handler(response)
        result_data = response.json()
        rows = [row_data.get("attributes") for row_data in result_data.get("data")]

        all_rows = rows

        message = "Fetched {} rows"
        print(message.format(len(all_rows)), end="\r")

        while (
            result_data.get("links") is not None
            and result_data.get("links").get("next") is not None
            and result_data.get("links").get("next") != "null"
        ):
            next_page_url = self.base_url + result_data.get("links").get("next")
            response = self.session.get(next_page_url)
            error_handler(response)
            result_data = response.json()
            if result_data.get("data"):
                rows = [
                    row_data.get("attributes") for row_data in result_data.get("data")
                ]
            else:
                rows = []
            all_rows.extend(rows)
            print(message.format(len(all_rows)), end="\r")

        # Blank line resets console line start position
        print()
        return self._get_sorted_col_df(pd.DataFrame(all_rows))

    def _get_root_loc_from_url(self, url) -> str:
        # Function to parse the root location from URL & return it.
        pos = url.rfind("?")
        s = ""
        for i in range(0, pos):
            s += url[i]
        return s.split("/")[-1]

    def _local_temp_file_path(self, filename):
        # Function to check presence of file based upon system platform
        temp_dir = Path(
            "/tmp" if platform.system() == "Darwin" else tempfile.gettempdir()
        ).absolute()

        temp_file_path = os.path.join(temp_dir, filename)
        if Path(temp_file_path).exists():
            os.remove(temp_file_path)

        return temp_file_path

    def _extract_results_from_download_urls(self, download_urls) -> pd.DataFrame:
        # Function to pull out & combine results from the list of Download URLS
        query_metadata_df = pd.DataFrame()
        files = Parallel(n_jobs=-1, require="sharedmem")(
            delayed(self._write_single_gzip_file)(url) for url in download_urls
        )
        temp_records = []
        for filename in files:
            with gzip.open(filename, "rt", encoding="utf-8") as fgz:
                for line in fgz:
                    data = json.loads(line)
                    temp_records.append(data)
                    if len(temp_records) == const.QUERY_MAX_RECORD_SIZE:
                        new_df = pd.DataFrame.from_records(temp_records)
                        query_metadata_df = pd.concat(
                            [query_metadata_df, new_df], ignore_index=True
                        )
                        temp_records.clear()
        df = pd.DataFrame.from_records(temp_records)
        query_metadata_df = pd.concat([query_metadata_df, df], ignore_index=True)
        print(f"Fetched {len(query_metadata_df.index)} rows")
        return query_metadata_df

    def _write_single_gzip_file(self, url) -> str:
        """
        Function that writes content of a file and returns the filename.
        """
        r = requests.get(url, allow_redirects=True)
        name = self._get_root_loc_from_url(url)
        filename = self._local_temp_file_path(name)
        with open(filename, "wb") as f:
            f.write(r.content)
        return filename

    def _generator_function_for_download_urls(
        self, download_urls: list
    ) -> Generator[dict, None, None]:
        """
        Function to return an iterable object, that yields files one line at a time downloaded from the list of download_urls.
        """
        files = Parallel(n_jobs=-1, require="sharedmem")(
            delayed(self._write_single_gzip_file)(url) for url in download_urls
        )
        for filename in files:
            with gzip.open(filename, "rt", encoding="utf-8") as fgz:
                for line in fgz:
                    sorted_json = omix_hlpr.return_sorted_dict(json.loads(line))
                    yield sorted_json

    def _fetch_results_as_file(
        self, query_id: str, iterator_function: bool
    ) -> Union[pd.DataFrame, Generator[dict, None, None]]:
        results_file_req_url = (
            f"{self.resource_url}/queries/{query_id}/results?action=download"
        )
        response = self.session.get(results_file_req_url)
        error_handler(response)
        result_data = response.json()

        results_file_download_url = result_data.get("data", {}).get("download_url")
        if results_file_download_url in [None, "Not available"]:
            # The user is probably executing SHOW TABLES or DESCRIBE query
            if iterator_function:
                return self._fetch_iterator_as_pages(query_id, 100)
            else:
                return self._fetch_results_as_pages(query_id, 100)
        else:
            pd.set_option("display.max_columns", None)
            if iterator_function:
                return self._generator_function_for_download_urls(
                    results_file_download_url
                )
            else:
                df = self._extract_results_from_download_urls(results_file_download_url)
                return self._get_sorted_col_df(df)

    def _get_sorted_col_df(self, results_dataframe):
        """
        Function to sort a dataframe columnwise. Primarily being used before returning the
        query_metadata result dataframe.

        ``Args:``
            |  ``results_dataframe :`` dataframe containing the query_metadata results

        ``Returns:``
            |  coloumn-wise sorted dataframe where the order will be dataset_id , src_dataset_id, alphabetically ordered
            |  rest of the columns.
        """

        # checking presence of either of the dataset_id related cols in the df
        id_cols_present = set.intersection(
            set(["dataset_id", "src_dataset_id"]), set(results_dataframe.columns)
        )
        if len(id_cols_present) == 0:
            # none of the dataset id related cols are present - sorting cols alphabetically
            results_dataframe = self._get_alphabetically_sorted_col_df(
                results_dataframe
            )
        elif len(id_cols_present) == 1:
            col_data = results_dataframe.pop(id_cols_present.pop())
            results_dataframe = self._get_alphabetically_sorted_col_df(
                results_dataframe
            )
            results_dataframe.insert(0, col_data.name, col_data)
        else:
            dataset_id_data = results_dataframe.pop("dataset_id")
            src_dataset_id_data = results_dataframe.pop("src_dataset_id")
            results_dataframe = self._get_alphabetically_sorted_col_df(
                results_dataframe
            )
            results_dataframe.insert(0, src_dataset_id_data.name, src_dataset_id_data)
            results_dataframe.insert(0, dataset_id_data.name, dataset_id_data)

        return results_dataframe

    def _get_alphabetically_sorted_col_df(self, results_dataframe):
        """
        Function to alphabetically column-wise sort a dataframe.

        ``Args:``
            |  ``dataframe :`` dataframe containing the query_metadata results

        ``Returns:``
            |  coloumn-wise sorted dataframe where the order will be alphabetical.

        """
        return results_dataframe.sort_index(axis=1)

    @Track.track_decorator
    def get_schema(
        self,
        repo_key: str,
        schema_level=[],
        source="",
        data_type="",
        return_type="dataframe",
    ) -> dict:
        """
        Function to get the Schema of all the tables in an OmixAtlas.
        User need to have Data Admin at the resource level to get the schema of an OmixAtlas.
        Please contact polly@support.com if you get Access Denied error message.

        Args:
            repo_key (str): repo_id OR repo_name. This is a mandatory field.
            schema_level (list, optional): Table name for which users want to get the schema. \
            Users can get the table names by querying `SHOW TABLES IN <repo_name>` using query_metadata function.\
            The default value is all the table names for the repo.
            source (str, optional): Source for which user wants to fetch the schema. \
            The default value is all the sources in the schema.
            data_type (str, optional): Datatype for which user wants to fetch the schema. \
            The default value is all the datatypes in the schema.
            return_type (str, optional): For users who intend to query should use "dataframe" output. \
            For users, who want to perform schema management, they should get the output in "dict" format. \
            Dataframe format doesn't give the complete schema, it only shows the information \
            which aids users for writing queryies. Default value is "dataframe".

        Raises:
            paramException: When Function Parameter passed are not in the right format.
            RequestException: There is some issue in fetching the Schema.
            invalidApiResponseException: The Data returned is not in appropriate format.
        """

        try:
            schema_obj = Schema()
            return schema_obj.get_schema(
                self, repo_key, schema_level, source, data_type, return_type
            )
        except Exception as err:
            raise err

    @Track.track_decorator
    def validate_schema(self, body: dict) -> dict:
        """Validate the payload of the schema.
        If there are errors schema in schema, then table of errors are printed
        If there are no errors in the schema, success message is printed
        Payload Format
        {
            "data":{
                "type": <type_val>,
                "id": <id_val>,
                "attributes":{
                    "repo_id":<repo_id_val>,
                    "schema_type":<schema_type_val>,
                    "schema":{
                        <schema_val>
                    }
                }
            }
        }

        Args:
            body (dict): payload of the schema

        Raises:
            paramException: if payload is not in correct format

        Returns:
            dict: Dataframe having all the errors in the schema
        """
        try:
            schema_obj = Schema()
            res_df = schema_obj.validate_schema(self, body)
            return res_df
        except Exception as err:
            raise err

    @Track.track_decorator
    def insert_schema(self, repo_key, body: dict):
        """
        This function is used to insert the Schema in a newly created OmixAtlas.
        In order to insert schema the user must be a Data Admin at the resource level.<br>
        Please contact polly@support.com if you get Access Denied error message.

        Args:
            repo_key (str/int, Optional): repo_id OR repo_name of the OmixAtlas. Users can  \
            get this by running `get_all_omixatlas` function. If not passed, taken from payload.
            body (dict):  The payload should be a JSON file for a specific table as per the structure defined for \
            schema.

        Raises:
            RequestException: Some Issue in Inserting the Schema for the OmixAtlas.
        """
        try:
            schema_obj = Schema()
            schema_obj.insert_schema(self, repo_key, body)
        except Exception as err:
            raise err

    @Track.track_decorator
    def update_schema(self, repo_key, body: dict):
        """
        This function is used to update the schema of an existing OmixAtlas.
        If the user wants to edit a field or its attribute in existing schema or if they want to
        add or delete new fields or if they want add a new source or datatype then they should use
        update schema function.\
        Using update_schema, users can:<br>
            1. ADD new source or datatypes in the schema<br>
            2. ADD a new field to a source+data_type combination<br>
            3. UPDATE attributes of an existing field<br>
            However, using update_schema, users can't perform DELETE operations on any field, source or datatype.<br><br>
        A message will be displayed on the status of the operation.\
        In order to update schema the user must be a Data Admin at the resource level.<br>
        Please contact polly@support.com if you get Access Denied error message.\
        For more information, (see Examples)

        Args:
            repo_key (str/int, Optional): repo_id OR repo_name of the OmixAtlas. Users can  \
            get this by running get_all_omixatlas function. If not passed, taken from payload.
            body (dict): The payload should be a JSON file for a specific table as per the structure defined for \
            schema.

        Raises:
            RequestException: Some Issue in Updating the Schema for the OmixAtlas.
            paramException: Parameter Functions are not passed correctly.
        """
        try:
            schema_obj = Schema()
            schema_obj.update_schema(self, repo_key, body)
        except Exception as err:
            raise err

    @Track.track_decorator
    def replace_schema(self, repo_key, body: dict):
        """
        The function will completely replace existing schema with the new schema passed in the body.\
        A message will be displayed on the status of the operation.\
        Completely REPLACE the existing schema with the one provided, so it can do all the \
        ops (including deletion of fields if they are no longer present in the new incoming schema).\
        In order to replace schema the user must be a Data Admin at the resource level.<br>
        Please contact polly@support.com if you get Access Denied error message.\
        For more information, (see Examples)

        Args:
            repo_key (str/int, optional): repo_id OR repo_name of the OmixAtlas. Users can  \
            get this by running get_all_omixatlas function. If not passed, taken from payload.
            body (dict): The payload should be a JSON file for a specific table as per the structure defined for schema.

        Raises:
            RequestException: Some Issue in Replacing the Schema for the OmixAtlas.
            paramException: Parameter Functions are not passed correctly.
        """
        try:
            schema_obj = Schema()
            schema_obj.replace_schema(self, repo_key, body)
        except Exception as err:
            raise err

    @Track.track_decorator
    def download_data(self, repo_name, _id: str, internal_call=False):
        """
        To download any dataset, the following function can be used to get the signed URL of the dataset.
        The data can be downloaded by clicking on this URL.
        NOTE: This signed URL expires after 60 minutes from when it is generated.

        The repo_name OR repo_id of an OmixAtlas can be identified by calling the get_all_omixatlas() function.
        The dataset_id can be obtained by querying the metadata at the dataset level using query_metadata().

        This data can be parsed into a data frame for better accessibility using the code under the examples section.

        Args:
              repo_key (str): repo_id OR repo_name. This is a mandatory field.
              payload (dict): The payload is a JSON file which should be as per the structure defined for schema.
              Only data-admin will have the authentication to update the schema.
              internal_call (bool): True if being called internally by other functions. Default is False

        Raises:
              apiErrorException: Params are either empty or its datatype is not correct or see detail.
        """
        if not internal_call:
            # if not an internal call and is called directly, we show deprecation msg
            warnings.simplefilter("always", DeprecationWarning)
            warnings.formatwarning = (
                lambda msg, *args, **kwargs: f"DeprecationWarning: {msg}\n"
            )
            warnings.warn(
                "This method will soon be deprecated. Please use new function download_dataset for downloading"
                + " data files directly.\nFor usage: help(<omixatlas_object>.download_dataset) \n"
                + "For more details: "
                + "https://docs.elucidata.io/polly-python/OmixAtlas/Download%20Data.html#omixatlas.OmixAtlas.download_dataset"
            )
        url = f"{self.resource_url}/{repo_name}/download"
        params = {"_id": _id}
        response = self.session.get(url, params=params)
        error_handler(response)
        return response.json()

    @Track.track_decorator
    def save_to_workspace(
        self, repo_id: str, dataset_id: str, workspace_id: int, workspace_path: str
    ) -> json:
        """
        Function to download a dataset from OmixAtlas and save it to Workspaces.

        Args:
             repo_id (str): repo_id of the Omixatlas
             dataset_id (str): dataset id that needs to be saved
             workspace_id (int): workspace id in which the dataset needs to be saved
             workspace_path (str): path where the workspace resides

        Returns:
             json: Info about workspace where data is saved and of which Omixatlas
        """
        url = f"{self.resource_url}/workspace_jobs"
        params = {"action": "copy"}
        payload = {
            "data": {
                "type": "workspaces",
                "attributes": {
                    "dataset_id": dataset_id,
                    "repo_id": repo_id,
                    "workspace_id": workspace_id,
                    "workspace_path": workspace_path,
                },
            }
        }
        response = self.session.post(url, data=json.dumps(payload), params=params)
        error_handler(response)
        if response.status_code == 200:
            logging.basicConfig(level=logging.INFO)
            logging.info(f"Data Saved to workspace={workspace_id}")
        return response.json()

    @Track.track_decorator
    def format_converter(self, repo_key: str, dataset_id: str, to: str) -> None:
        """
        Function to convert a file format.
        Args:
            repo_key (str) : repo_id.
            dataset_id (str) : dataset_id.
            to (str) : output file format.
        Raises:
            InvalidParameterException : invalid value of any parameter for example like - repo_id/repo_name.
            paramException : Incompatible or empty value of any parameter
        """
        if not (repo_key and isinstance(repo_key, str)):
            raise InvalidParameterException("repo_id/repo_name")
        if not (dataset_id and isinstance(dataset_id, str)):
            raise InvalidParameterException("dataset_id")
        if not (to and isinstance(to, str)):
            raise InvalidParameterException("convert_to")
        ssl._create_default_https_context = ssl._create_unverified_context
        response_omixatlas = self._get_omixatlas(repo_key)
        data = response_omixatlas.get("data").get("attributes")
        repo_name = data.get("repo_name")
        index_name = data.get("v2_indexes", {}).get("files")
        if index_name is None:
            raise paramException(
                title="Param Error", detail="Repo entered is not an omixatlas."
            )
        elastic_url = f"{self.elastic_url}/{index_name}/_search"
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"_index": index_name}},
                        {"term": {"dataset_id.keyword": dataset_id}},
                    ]
                }
            }
        }
        data_type = helpers.get_data_type(self, elastic_url, query)
        if data_type in DATA_TYPES:
            mapped_list = DATA_TYPES[data_type][0]
            if to in mapped_list["format"]:
                supported_repo = mapped_list["supported_repo"]
                repo_found = False
                for details in supported_repo:
                    if repo_name == details["name"]:
                        header_mapping = details["header_mapping"]
                        repo_found = True
                if not repo_found:
                    raise paramException(
                        title="Param Error",
                        detail=f"Incompatible repository error: Repository:'{repo_name}' not yet \
                                 incorporated for converter function",
                    )
                helpers.file_conversion(self, repo_name, dataset_id, to, header_mapping)
            else:
                raise paramException(
                    title="Param Error",
                    detail=f"Incompatible dataformat error: data format= {to} not yet incorporated for converter function",
                )
        else:
            raise paramException(
                title="Param Error",
                detail=f"Incompatible dataype error: data_type={data_type} not yet incorporated for converter function",
            )
        logging.basicConfig(level=logging.INFO)
        logging.info("File converted successfully!")

    @Track.track_decorator
    def create(
        self,
        display_name: str,
        description: str,
        repo_name="",
        image_url="",
        components=[],
        category="private",
        data_type=None,
        org_id="",
        controls={},
    ) -> pd.DataFrame:
        """
        This function is used to create a new omixatlas.
        The arguments category, data_type and org_id can only be set during creation of Omixatlas and cannot be
        updated afterwards.

        Args:
            display_name (str): Display name of the omixatlas as shown on the GUI.
            description (str): description of the omixatlas.
            repo_name (str, optional): repo_name which is used to create index in database.
            image_url (str, optional): URL of the image which should be kept as the icon for omixatlas.
            components (list, optional): Optional Parameter.
            category (str, optional): Optional parameter(public/private/diy_poa).Immutable argument.
            By default it is private.
            data_type (str, optional): Optional Parameter(single_cell/rna_seq).Immutable argument.
            By default it is None. If category is `public` or `diy_poa` then `data_type` is mandatory.
            org_id (str, optional): Optional Parameter. Org Id is mandatory to be passed when category
            of omixatlas is `diy_poa`. Org Id can be found on admin panel.

        Returns:
            Dataframe after creation of omixatlas.

        Raises:
            ValueError: Repository creation response is in Incorrect format.
        """
        try:
            omix_hlpr.check_create_omixatlas_parameters(
                display_name,
                description,
                repo_name,
                image_url,
                components,
                category,
                data_type,
                org_id,
                controls,
            )
            payload = const.REPOSITORY_PAYLOAD
            frontend_info = {}
            frontend_info["description"] = description
            frontend_info["display_name"] = display_name
            frontend_info["icon_image_url"] = (
                image_url if image_url else const.IMAGE_URL_ENDPOINT
            )
            frontend_info["controls"] = controls

            if not repo_name:
                repo_name = omix_hlpr.create_repo_name(display_name)
            else:
                repo_name = repo_name

            payload["data"]["attributes"]["repo_name"] = repo_name
            payload["data"]["attributes"]["category"] = category
            if data_type:
                payload["data"]["attributes"]["data_type"] = data_type
            if org_id:
                payload["data"]["attributes"]["org_id"] = org_id
            payload["data"]["attributes"]["frontend_info"] = frontend_info
            payload["data"]["attributes"]["components"] = components
            indexes = payload["data"]["attributes"]["indexes"]

            for key in indexes.keys():
                indexes[key] = f"{repo_name}_{key}"

            repository_url = f"{self.resource_url}"
            resp = self.session.post(repository_url, json=payload)
            error_handler(resp)

            if resp.status_code != const.CREATED:
                raise Exception(resp.text)
            else:
                if resp.json()["data"]["id"]:
                    repo_id = resp.json()["data"]["id"]
                    print(f" OmixAtlas {repo_id} Created  ")
                    return omix_hlpr.repo_creation_response_df(resp.json())
                else:
                    ValueError("Repository creation response is in Incorrect format")
        except Exception as err:
            raise err

    @Track.track_decorator
    def update(
        self,
        repo_key: str,
        display_name="",
        description="",
        image_url="",
        workspace_id="",
        components=[],
        controls={},
    ) -> pd.DataFrame:
        """
        This function is used to update an omixatlas.

        Args:
             repo_key (str/int): repo_name/repo_id for that Omixatlas
             display_name (str, optional): Display name of the omixatlas as shown on the GUI.
             description (str, optional): Description of the omixatlas.
             image_url (str, optional): URL of the image which should be kept as the icon for omixatlas.
             workspace_id (str, optional): ID of the Workspace to be linked to the Omixatlas.
             components (list, optional): List of components to be added.
        """

        omix_hlpr.check_update_omixatlas_parameters(
            display_name,
            description,
            repo_key,
            image_url,
            components,
            workspace_id,
            controls,
        )

        if isinstance(repo_key, int):
            repo_key = omix_hlpr.make_repo_id_string(repo_key)

        if workspace_id:
            self._link_workspace_to_omixatlas(repo_key, workspace_id)

        repo_curr_data = self._get_omixatlas(repo_key)

        if "attributes" not in repo_curr_data["data"]:
            raise invalidDataException(
                detail="OmixAtlas is not created properly. Please contact admin"
            )

        attribute_curr_data = repo_curr_data["data"]["attributes"]
        if components:
            curr_components = attribute_curr_data.get("components", [])
            for item in components:
                curr_components.append(item)

        repo_curr_data["data"]["attributes"] = attribute_curr_data

        if "frontend_info" not in repo_curr_data["data"]["attributes"]:
            raise invalidDataException(
                detail="OmixAtlas is not created properly. Please contact admin"
            )

        frontendinfo_curr_data = repo_curr_data["data"]["attributes"]["frontend_info"]
        repo_curr_data["data"]["attributes"]["frontend_info"] = (
            omix_hlpr.update_frontendinfo_value(
                frontendinfo_curr_data, image_url, description, display_name, controls
            )
        )

        repository_url = f"{self.resource_url}/{repo_key}"
        resp = self.session.patch(repository_url, json=repo_curr_data)
        error_handler(resp)
        if resp.status_code != const.OK:
            raise Exception(resp.text)
        else:
            if resp.json()["data"]["id"]:
                repo_id = resp.json()["data"]["id"]
                print(f" OmixAtlas {repo_id} Updated  ")
                return omix_hlpr.repo_creation_response_df(resp.json())
            else:
                ValueError("Repository Updation response is in Incorrect format")

    def _link_workspace_to_omixatlas(self, repo_key: str, workspace_id: str):
        """
        Link a workspace ID given by the user to an OmixAtlas. Called by the update() function.
        Args:
            repo_key (str): repo_name/repo_id for that Omixatlas
            workspace_id (str): ID of the Workspace to be linked to the Omixatlas
        """
        url = f"{self.discover_url}/repositories/{repo_key}"
        get_response = self.session.get(url)
        error_handler(get_response)
        get_response = get_response.json()
        get_response["data"]["attributes"]["linked_workspace_id"] = workspace_id
        get_response["data"]["attributes"].pop("repo_name")
        patch_response = self.session.patch(url, data=json.dumps(get_response))
        error_handler(patch_response)
        if patch_response.status_code != const.OK:
            raise Exception(patch_response.text)
        else:
            if patch_response.json()["data"]["id"]:
                repo_id = patch_response.json()["data"]["id"]
                print(f" Workspace ID {workspace_id} linked with OmixAtlas {repo_id}")
            else:
                ValueError("Repository Updation response is in Incorrect format")

    # function used in delete datasets also
    def _commit_data_to_repo(self, repo_id: str):
        """
        Inform the infra to commit the data uploaded
        Not raising error in this if commit API Fails because
        even if manual commit fails, files will be picked up in
        automatic update. Users need not know about this
        Args:
            repo_id: str
        """
        try:
            schema_base_url = f"{self.discover_url}/repositories"
            url = f"{schema_base_url}/{repo_id}/files?action=commit"
            resp = self.session.post(url)
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

    @Track.track_decorator
    def add_datasets(
        self,
        repo_id: int,
        source_folder_path: dict,
        priority="low",
        validation=False,
    ) -> pd.DataFrame:
        """
        This function is used to add a new data into an OmixAtlas.
        Once user runs this function successfully, it takes 30 seconds to log the ingestion request and within 2 mins, the
        ingestion log will be shown in the data ingestion monitoring dashboard.
        In order to add datasets into Omixatlas the user must be a Data Contributor at the resource level.
        Please contact polly@support.com if you get Access Denied error message.

        Args:
            repo_id (int/str): repo_id for that Omixatlas
            source_folder_path (dict): source folder paths from data and metadata files are fetched.In this \
            dictionary, there should be two keys called "data" and "metadata" with value consisting of folders where \
            data and metadata files are stored respectively i.e. {"data":"<data_path>", "metadata":"<metadata_path>"}
            priority (str, optional): Optional parameter(low/medium/high). \
            Priority at which this data has to be ingested into the OmixAtlas. \
            The default value is "low". Acceptable values are "medium" and "high".
            validation (bool, optional): Optional parameter(True/False) Users was to activate validation. By Default False. \
            Means validation not active by default. Validation needs to be activated only when \
            validated files are being ingested.

        Raises:
            paramError: If Params are not passed in the desired format or value not valid.
            RequestException: If there is issue in data ingestion.

        Returns:
            pd.DataFrame: DataFrame showing Upload Status of Files
        """
        try:
            files_obj = Files()
            data_upload_results_df = files_obj.add_datasets(
                self, repo_id, source_folder_path, priority, validation
            )
            return data_upload_results_df
        except Exception as err:
            raise err

    @Track.track_decorator
    def update_datasets(
        self,
        repo_id: int,
        source_folder_path: dict,
        priority="low",
        file_mapping={},
        validation=False,
    ) -> pd.DataFrame:
        """
        This function is used to update a new data into an OmixAtlas.
        Once user runs this function successfully, it takes 30 seconds to log the ingestion request and within 2 mins, the
        ingestion log will be shown in the data ingestion monitoring dashboard.
        In order to update datasets the user must be a Data Contributor at the resource level.
        Please contact polly@support.com if you get Access Denied error message.

        Args:
            repo_id (int/str): repo_id for that Omixatlas
            source_folder_path (dict): source folder paths from data and metadata files are fetched.In this \
            dictionary, there should be two keys called "data" and "metadata" with value consisting of folders where \
            data and metadata files are stored respectively i.e. {"data":"<data_path>", "metadata":"<metadata_path>"}
            priority (str, optional): Optional parameter(low/medium/high).\
            Priority at which this data has to be ingested into the OmixAtlas. \
            The default value is "low". Acceptable values are "medium" and "high".
            file_mapping(dict, optional): Defaults to empty dict. The dictionary should be in the format \
            {"<dataset_file_name>":"<datset_id>"}. Full Dataset File Name should be provided in the key. \
            Example entry -> {"GSE2067_GPL96.gct": "GSE2067_GPL96", "GSE2067_GPL97.gct": "GSE2067_GPL97"}
            validation(bool, optional): Optional parameter(True/False) Users was to activate validation. By Default False. \
            Means validation not active by default. Validation needs to be activated only when \
            validated files are being ingested.

        Raises:
            paramError: If Params are not passed in the desired format or value not valid.
            RequestException: If there is issue in data ingestion.

        Returns:
            pd.DataFrame: DataFrame showing Upload Status of Files
        """
        try:
            files_obj = Files()
            data_upload_results_df = files_obj.update_datasets(
                self, repo_id, source_folder_path, priority, file_mapping, validation
            )
            return data_upload_results_df
        except Exception as err:
            raise err

    # used in delete datasets
    @lru_cache(maxsize=None)
    def _list_files_in_oa(self, repo_id: str):
        """
        Summary:
        for a given repo_id/omixatlas, this function returns all the files
        present in the omixatlas.
        refer to :
        https://elucidatainc.atlassian.net/wiki/spaces/DIS/pages/3654713403/Data+ingestion+APIs+-+technical+proposal
        for more information

        Arguments:
            repo_id -- repo id (str)

        Returns:
            list of file "data" information
        """
        files_api_endpoint = f"{self.discover_url}/repositories/{repo_id}/files"
        next_link = ""
        responses = []
        while next_link is not None:
            if next_link:
                next_endpoint = f"{self.discover_url}{next_link}"
                response = self.session.get(next_endpoint)
            else:
                query_params = {
                    "page[size]": 1000,
                    "page[after]": 0,
                    "include_metadata": "false",
                    "data": "true",
                    "version": "current",
                }
                response = self.session.get(files_api_endpoint, params=query_params)
            response.raise_for_status()
            response_json = response.json()
            responses.append(response_json.get("data"))
            next_link = response_json.get("links").get("next")
        return responses

    # TODO
    # Currently works for repositories having source -> `all` & datatype -> `all`
    # In the datalake only these examples exist for now
    # In future it will be extended for other sources and datatypes
    @Track.track_decorator
    def dataset_metadata_template(
        self, repo_key, source="all", data_type="all"
    ) -> dict:
        """
        This function is used to fetch the template of dataset level metadata in a given OmixAtlas.
        In order to ingest the dataset level metadata appropriately in the OmixAtlas, the user needs
        to ensure the metadata json file contains the keys as per the dataset level schema.

        Args:
            repo_id (str/int): repo_name/repo_id for that Omixatlas
            source (all, optional): Source/Sources present in the schema. Default value is "all"
            data_type (all, optional): Datatype/Datatypes present in the schema. Default value is "all"

        Returns:
            A dictionary with the dataset level metadata

        Raises:
            invalidApiResponseException: attribute/key error

        """
        # for dataset level metadata index is files
        schema_type = "files"

        schema_base_url = f"{self.discover_url}/repositories"

        dataset_url = f"{schema_base_url}/{repo_key}/" + f"schemas/{schema_type}"

        resp = self.session.get(dataset_url)
        error_handler(resp)
        api_resp_dict = resp.json()
        if "data" in api_resp_dict:
            if "attributes" in api_resp_dict["data"]:
                if "schema" in api_resp_dict["data"]["attributes"]:
                    resp_dict = {}
                    resp_dict = api_resp_dict["data"]["attributes"]["schema"][source][
                        data_type
                    ]
                else:
                    raise invalidApiResponseException(
                        title="schema key not present",
                        detail="`schema` key not inside attributes present in the repository schema",
                    )
            else:
                raise invalidApiResponseException(
                    title="attributes key not present",
                    detail="attributes not present in the repository schema",
                )
        else:
            raise invalidApiResponseException(
                title="data key not present",
                detail="data key not present in the repository schema",
            )

        result_dict = {}
        # deleting unnecessary keys
        for field_key, val_dict in resp_dict.items():
            is_array_val = val_dict.get("is_array", None)
            type_val = val_dict.get("type", None)
            original_name_key = val_dict.get("original_name", None)
            if is_array_val is None:
                result_dict[original_name_key] = type_val
            elif is_array_val:
                result_dict[original_name_key] = []
            else:
                result_dict[original_name_key] = type_val

        # adding `__index__` key and its default values
        result_dict["__index__"] = {
            "file_metadata": True,
            "col_metadata": True,
            "row_metadata": False,
            "data_required": False,
        }

        return result_dict

    def get_all_file_paths(
        self, repo_id: int, dataset_id: str, internal_call=False
    ) -> list:
        """Get all file paths where the file is stored corresponding to the
        repo_id and dataset_id

        Args:
            repo_id (int): repo_id of the omixatlas
            dataset_ids (str): dataset_id present in the omixatlas

        Raises:
            paramError: If Params are not passed in the desired format or value not valid.

        Returns:
            list: all the file paths corresponding to repo_id and dataset_id
            Error: If repo_id or dataset id does not exist in the system
        """
        files_obj = Files()
        file_paths = files_obj.get_all_file_paths(
            self, repo_id, dataset_id, internal_call
        )
        return file_paths

    @Track.track_decorator
    def delete_datasets(
        self, repo_id: int, dataset_ids: list, dataset_file_path_dict={}
    ):
        """
        This function is used to delete datasets from an OmixAtlas.
        Once user runs this function successfully, they should be able to see the
        deletion status on the data ingestion monitoring dashboard within ~2 mins.
        A dataframe with the status of the operation for each file(s) will be displayed after the
        function execution.

        In order to delete datasets into Omixatlas the user must be a Data Admin at the resource level.
        Please contact polly.support@elucidata.io if you get Access Denied error message.

        Note -> Because this function takes list as an input, user must not run this function in a loop.

        Args:
            repo_id (int): repo_id for that Omixatlas
            dataset_ids (list): list of dataset_ids that users want to delete. It is mandatory for \
            users to pass the dataset_id which they want to delete from the repo in this list.
            dataset_file_path_dict(dict, Optional): Optional Parameter. In case a given dataset ID \
            has multiple files associated with it, then the user has to specifically give the \
            file_path which needs to be deleted. Users can use the function get_all_file_paths \
            to get paths of all the files which correspond to same dataset_id.

        Raises:
            paramError: If Params are not passed in the desired format or value not valid.
            RequestException: If there is issue in data ingestion.

        Returns:
            None
        """
        try:
            files_obj = Files()
            files_obj.delete_datasets(
                self, repo_id, dataset_ids, dataset_file_path_dict
            )
        except Exception as err:
            raise err

    def move_data(
        self,
        source_repo_key: str,
        destination_repo_key: str,
        dataset_ids: list,
        priority="medium",
    ) -> str:
        """
        This function is used to move datasets from source atlas to destination atlas.
        This function should only be used when schema of source and destination atlas are compatible with each other.
        Else, the behaviour of data in destination atlas may not be the same or the ingestion may fail.
        Please contact polly@support.com if you get Access Denied error message.

        Args:
            source_repo_key (str/int): src repo key of the dataset ids. Only repo_id supported now,
            destination_repo_key (str/int): destination repo key where the data needs to be transferred
            dataset_ids (list): list of dataset ids to transfer
            priority (str, optional): Optional parameter(low/medium/high). Priority of ingestion. \
            Defaults to "medium".

        Returns:
            None: None
        """
        # right now source_repo_key and destination_repo_key is only supported
        # when sai makes the change in the API both repo_id and repo_name
        # will be supported
        try:
            omix_hlpr.move_data_params_check(
                source_repo_key, destination_repo_key, dataset_ids, priority
            )
            # convert repo_key if int from int to str
            source_repo_key = omix_hlpr.make_repo_id_string(source_repo_key)
            destination_repo_key = omix_hlpr.make_repo_id_string(destination_repo_key)

            src_repo_metadata = self._get_omixatlas(source_repo_key)
            data = src_repo_metadata.get("data").get("attributes", {})
            # repo_name = data.get("repo_name")
            index_name = data.get("v2_indexes", {}).get("files")
            if index_name is None:
                raise paramException(
                    title="Param Error", detail="Invalid Repo Id/ Repo Name passed."
                )
            elastic_url = f"{self.elastic_url}/{index_name}/_search"
            # dataset links to be moved from source to destination
            payload_datasets = []
            for dataset_id in dataset_ids:
                query = helpers.elastic_query(index_name, dataset_id)
                metadata = helpers.get_metadata(self, elastic_url, query)
                source_info = metadata.get("_source", "")
                src_uri = source_info.get("src_uri", "")
                if not src_uri:
                    raise invalidApiResponseException(
                        title="Invalid API Response",
                        detail=f"src_uri for {dataset_id} does not exist.",
                    )
                payload_datasets.append(src_uri)

            move_data_url = f"{self.discover_url}/repositories/ingestion-transactions"
            move_data_payload = omix_hlpr.create_move_data_payload(
                payload_datasets, source_repo_key, destination_repo_key, priority
            )
            # move data API Call
            # json.dumps used so that dict is converted into json
            response = self.session.post(
                move_data_url, data=json.dumps(move_data_payload)
            )
            error_handler(response)
            if response.status_code == http_codes.OK:
                print(const.MOVE_DATA_SUCCESS)
        except Exception as err:
            raise err

    @Track.track_decorator
    def link_report(
        self,
        repo_key: str,
        dataset_id: str,
        workspace_id,
        workspace_path: str = None,
        access_key: str = "private",
    ) -> None:
        """
        This function is used to link a file (html or pdf) present in a workspace with the specified dataset in OmixAtlas.
        On success it displays the access key URL and a success message.
        Org admins can now link a report present in a workspace with the specified datasets in an OmixAtlas.
        Once a report is linked to a dataset in OmixAtlas, it can be fetched both from front-end and polly-python.
        A message will be displayed on the status of the operation.

        Warning:
            Since this function is only responsible for attaching the report, if you initially attach the \
            report as private and later make the file public, you must re-attach the report as public.

        Args:
            repo_key (str): repo_name/repo_id of the repository to be linked
            dataset_id (str): dataset_id of the dataset to be linked
            workspace_id (str/int): workspace_id or public url for the file which is to be linked \
            If workspace id provided then workspace path is required, for public url it will attach \
            as public report.
            workspace_path (str): workspace_path for the file which is to be linked
            access_key (str): access_key(private or public) depending upon the link access type to be generated.\
            If public, then anyone with a Polly account with the link will be able to see the report.\
            If private, only individuals who have access to the workspace where reports is stored will be able to see them.

        Raises:
            InvalidParameterException: invalid parameters

        Returns:
            None
        """
        if isinstance(workspace_id, int) or (
            isinstance(workspace_id, str) and workspace_id.isdigit()
        ):
            if not workspace_path:
                raise InvalidParameterException(
                    "workspace path is required with workspace id"
                )

            try:
                report_obj = Reporting()
                report_obj.link_report(
                    self,
                    repo_key,
                    dataset_id,
                    int(workspace_id),
                    workspace_path,
                    access_key,
                )
            except Exception as err:
                raise err

        elif isinstance(workspace_id, str):
            try:
                report_obj = Reporting()
                report_obj.link_report_url(self, repo_key, dataset_id, workspace_id)
            except Exception as err:
                raise err

        else:
            raise InvalidParameterException(
                "workspace path or public url is required for linking a report"
            )

    @Track.track_decorator
    def fetch_linked_reports(self, repo_key: str, dataset_id: str) -> pd.DataFrame:
        """
        Fetch linked reports for a dataset_id in an OmixAtlas.

        Args:
            repo_key (str): repo_name/repo_id of the repository for which to fetch the report
            dataset_id (str): dataset_id of the dataset which to fetch the reports.

        Raises:
            InvalidParameterException : invalid parameters
            RequestException : api request exception
            UnauthorizedException : unauthorized to perform this action

        Returns:
            A Dataframe with the details of the linked reports - who added the report, when it was added and the link.

        """
        try:
            report_obj = Reporting()
            df = report_obj.fetch_linked_reports(self, repo_key, dataset_id)
            return df
        except Exception as err:
            raise err

    @Track.track_decorator
    def download_linked_reports(self, repo_key: str, dataset_id: str, folder_path: str):
        """Downloads Linked Reports to the repo

        Args:
            repo_key (str): repo_name/repo_id of the repository for which to fetch the report
            dataset_id (str): dataset_id of the dataset which to fetch the reports.
            folder_path (str): local folder path where the files need to be downloaded

        Returns:
            Download: Downloads the datasets in the passed folder path
        """
        try:
            report_obj = Reporting()
            report_obj.download_linked_reports(self, repo_key, dataset_id, folder_path)
        except Exception as err:
            raise err

    @Track.track_decorator
    def delete_linked_report(
        self, repo_key: str, dataset_id: str, report_id: str
    ) -> None:
        """
         Delete the link of the report in workspaces with the specified dataset in OmixAtlas.
         On success displays a success message.

        Arguments:
            repo_key (str): repo_name/repo_id of the repository which is linked.
            dataset_id (str): dataset_id of the dataset to be unlinked
            report_id (str): report id associated with the report in workspaces that is to be deleted. \
            This id can be found when invoking the fetch_linked_report() function.

        Raises:
            InvalidParameterException: Invalid parameter passed

        Returns:
            None
        """
        try:
            report_obj = Reporting()
            report_obj.delete_linked_report(self, repo_key, dataset_id, report_id)
        except Exception as err:
            raise err

    @Track.track_decorator
    def download_metadata(
        self, repo_key: str, dataset_id: str, file_path: str, metadata_key="field_name"
    ) -> None:
        """
        This function is used to download the dataset level metadata into a json file.
        The key present in the json file can be controlled using the `metadata_key` argument of the function.
        Users should use `original_name` for data ingestion.

        Args:
            repo_key (str): repo_name/repo_id of the repository where dataset belongs to.
            dataset_id (str): dataset_id of the dataset for which metadata should be downloaded.
            file_path (str): the system path where the json file should be stored.
            metadata_key (str, optional): Optional paramter. The metadata_key determines the key used in the json file.
            There are two options available `field_name` and `original_name`.
            For ingestion related use-cases, users should use `original_name` and for other purposes
            `field_name` should be preferred.
            The default value is `field_name`.

        Raises:
            InvalidParameterException: Invalid parameter passed
            InvalidPathException: Invalid file path passed
            InvalidDirectoryPathException: Invalid file path passed
        """
        if not (repo_key and isinstance(repo_key, str)):
            raise InvalidParameterException("repo_key")
        if not (dataset_id and isinstance(dataset_id, str)):
            raise InvalidParameterException("dataset_id")
        if not (file_path and isinstance(file_path, str)):
            raise InvalidParameterException("file_path")
        if not (
            (metadata_key.lower() in ["field_name", "original_name"])
            and isinstance(metadata_key, str)
        ):
            raise paramException(
                title="Param Error",
                detail="metadata_key argument should be either of the two values - [field_name, original_name]",
            )
        if not os.path.exists(file_path):
            raise InvalidPathException
        if not os.path.isdir(file_path):
            raise InvalidDirectoryPathException
        response_omixatlas = self.omixatlas_summary(repo_key)
        data = response_omixatlas.get("data")
        index_name = data.get("indexes", {}).get("files")
        if index_name is None:
            raise paramException(
                title="Param Error", detail="Repo entered is not an omixatlas."
            )
        elastic_url = f"{self.elastic_url}/{index_name}/_search"
        query = helpers.elastic_query(index_name, dataset_id)
        metadata = helpers.get_metadata(self, elastic_url, query)
        source_info = metadata.get("_source")
        file_name = f"{dataset_id}.json"
        complete_path = helpers.make_path(file_path, file_name)
        final_data = source_info
        if metadata_key == "original_name":
            # replace field names with original names
            data_type = source_info.get("data_type")
            schema_dict_tuple = self.get_schema(repo_key, return_type="dict")
            schema_dict_datasets = schema_dict_tuple.datasets
            schema_dict_val = (
                schema_dict_datasets.get("data", {})
                .get("attributes", {})
                .get("schema", {})
            )
            dataset_source = schema_dict_val.get("dataset_source")
            final_data = helpers.replace_original_name_field(
                source_info, schema_dict_val, dataset_source, data_type
            )
        with open(complete_path, "w") as outfile:
            json.dump(final_data, outfile)
        print(
            f"The dataset level metadata for dataset = {dataset_id} has been downloaded at : = {complete_path}"
        )

    @Track.track_decorator
    def download_dataset(self, repo_key: str, dataset_ids: list, folder_path=""):
        """
        This functions downloads the data for the provided dataset id list from the repo passed to
        the folder path provided.

        Arguments:
            repo_key (int/str): repo_id OR repo_name. This is a mandatory field.
            dataset_ids (list): list of dataset_ids from the repo passed that users want to download data of
            folder_path (str, optional): folder path where the datasets will be downloaded to.
            Default is the current working directory.

        Raises:
            InvalidParameterException : invalid or missing parameter
            paramException : invalid or missing folder_path provided
        """
        if not folder_path:
            folder_path = os.getcwd()

        try:
            omix_hlpr.param_check_download_dataset(
                repo_key=repo_key, dataset_ids=dataset_ids, folder_path=folder_path
            )
            repo_key = helpers.make_repo_id_string(repo_key)
            # number of jobs/workers set as 30 as that was the best performing while profiling
            # please refer ticket LIB-314 for more details/tech debt link
            # in sharedmem the memory is shared amongst the threads. Otherwise, for each thread a
            # different session is required, that needs to be authenticated.
            Parallel(n_jobs=30, require="sharedmem")(
                delayed(self._download_data_file)(repo_key, i, folder_path)
                for i in dataset_ids
            )
        except Exception as err:
            raise err

    def _download_data_file(self, repo_name: str, dataset_id: str, folder_path: str):
        try:
            download_response = self.download_data(
                repo_name, dataset_id, internal_call=True
            )
            url = (
                download_response.get("data", {})
                .get("attributes", {})
                .get("download_url")
            )
        except Exception as err:
            print(
                f"error in getting the download url for dataset_id: {dataset_id}. Download of this file will be skipped."
                + f" ERROR: {err}"
            )
            return
        try:
            """
            example URL:
            {'data': {'attributes': {'last-modified': '2022-11-22 18:25:31.000000', 'size': '39.68 KB', 'download_url':
            'https://discover-prod-datalake-v1.s3.amazonaws.com/GEO_data_lake/data/GEO_metadata/GSE7466/GCT/
            GSE7466_GPL3335_metadata.gct?X-Amz-Algorithm=.....f24f472f'}}}
            """
            filename = url.split("/")[-1].split("?")[0]
            filename_path = os.path.join(folder_path, filename)
            with requests.get(url, stream=True) as r:
                total_size_in_bytes = int(r.headers.get("content-length", 0))
                progress_bar = tqdm(
                    total=total_size_in_bytes,
                    unit="iB",
                    unit_scale=True,
                    desc=f"downloading data file:{filename}",
                    position=0,
                    leave=True,
                )
                r.raise_for_status()
                with open(filename_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        progress_bar.update(len(chunk))
                        f.write(chunk)
                progress_bar.close
        except Exception as err:
            # if any error occurs on downloading the data, then if the file is created/partially present
            # we delete that file.
            print(
                f"error in downloading the data from the url for dataset_id: {dataset_id}: {err}"
            )
            if os.path.exists(filename_path):
                os.remove(filename_path)
            return

    @Track.track_decorator
    def get_metadata(
        self, repo_key: str, dataset_id: str, table_name: str
    ) -> pd.DataFrame:
        """
        This function is used to get the sample level metadata as a dataframe.

        Args:
            repo_key(str): repo_name/repo_id of the repository.
            dataset_id(str): dataset_id of the dataset.
            table_name(str): table name for the desired metadata, 'samples','samples_singlecell' supported for now.

        Raises:
              paramException: invalid or missing parameter provided
              RequestFailureException: Request failed
        """
        omix_hlpr.check_params_for_get_metadata(repo_key, dataset_id, table_name)
        repo_key = omix_hlpr.make_repo_id_string(repo_key)
        omixatlas_data = self._get_omixatlas(repo_key)
        v2_index = (
            omixatlas_data.get("data", {}).get("attributes", {}).get("v2_indexes", "")
        )
        # getting the mapped value for table_name from the dictionary
        actual_index = TABLE_NAME_SAMPLE_LEVEL_INDEX_MAP.get(table_name, "")
        if actual_index not in v2_index:
            # this implies that this is an irrelevant index
            raise paramException(
                title="Param Error",
                detail=ERROR_MSG_GET_METADATA,
            )
        # getting the value for this index
        index = v2_index.get(actual_index, "")
        discover_url = (
            f"https://api.datalake.discover.{self.session.env}.elucidata.io/elastic/v2"
        )
        page_size = 1000  # has to be less than 10k, chose 1000 as an optimal value for fast pagination

        dataframe = self._retrieve_dataframe(discover_url, page_size, dataset_id, index)
        return dataframe

    def _retrieve_dataframe(self, discover_url, page_size, dataset_id, index):
        """
        Function that drives the process of retrieval of dataframe.
        This function can be reused in future for getting metadata for dataset and feature level,
        with argument index being specified for respective metadata.
        """
        # loop for fetching data and setting the lower limit for the page_size
        while page_size > 50:
            query = helpers.make_query_for_discover_api(page_size, dataset_id)
            first_pass_data = self._initiate_retrieval(discover_url, query, index)
            if first_pass_data:
                # first pass yields a valid result for the query
                # sending this data for completing the process
                final_dataframe = self._complete_retrieval(
                    discover_url, first_pass_data
                )
                if final_dataframe is not False:
                    # complete result fetched in a dataframe
                    return final_dataframe
            # process interrupted as query failed due to large page_size, restart the process with page_size as half
            page_size = page_size / 2
        # the page_size reduction will happen only until page_size=50, raise an exception after that
        raise RequestFailureException

    def _initiate_retrieval(self, discover_url, query, index):
        """
        Function to kickstart the retrieval of sample level metadata using the discover endpoint,
        returns the result for the first pass.
        """
        payload = json.dumps(query)
        query_url = discover_url + f"/{index}/_search?scroll=1m"
        response = self.session.post(query_url, data=payload)
        if (
            response.status_code == http_codes.GATEWAY_TIMEOUT
            or response.status_code == http_codes.PAYLOAD_TOO_LARGE
        ):
            # a possible failure due to large page_size in the query
            return False

        try:
            if response.status_code != 200:
                omix_hlpr.handle_elastic_discover_api_error(response)
        except Exception as err:
            raise err

        search_result = json.loads(response.text)
        # search_result is a dictionary conatining the details from the endpoint
        hits = search_result.get("hits", {}).get("hits")
        if not hits:
            # the hits will be an empty list if the index is incorrect for the dataset_id
            raise Exception(
                "The index provided by you is not applicable for this dataset. \
For gct files, please use samples and for h5ad files, please use samples_singlecell. \
Please ensure that the dataset_id mentioned is present in the repo_key mentioned in the function parameters. \
If any issue persists, please contact polly.support@elucidata.io"
            )
        return search_result

    def _complete_retrieval(self, discover_url, search_result):
        """
        Function to complete the retrieval process and return the dataframe.
        """
        all_hits = []  # list for the comlete data
        hits = search_result.get("hits", {}).get("hits")  # results from the first pass
        # hits will be a list containing the data
        while hits:
            # combining hits in the first pass with the paginated results, if any
            all_hits += hits
            scroll_id = search_result["_scroll_id"]
            payload = json.dumps({"scroll": "1m", "scroll_id": scroll_id})
            response = self.session.post(discover_url + "/_search/scroll", data=payload)
            if (
                response.status_code == http_codes.GATEWAY_TIMEOUT
                or response.status_code == http_codes.PAYLOAD_TOO_LARGE
            ):
                # a possible failure due to large page_size in the query
                return False
            error_handler(response)
            search_result = json.loads(response.text)
            hits = search_result.get("hits", {}).get("hits")
        return pd.DataFrame(
            data=[hit.get("_source") for hit in all_hits if "_source" in hit]
        )

    def check_omixatlas_status(self, repo_key: str) -> bool:
        """
        function to check if a repository or omixatlas is locked or not.
        if the repository/omixatlas is locked, it is blocked for any schema or ingestion related processes.
        returns True if locked and False if not locked.
        Arguments:
            repo_key(int/str): repo_id or repo_name in str or int format
        Raises:
            paramException: incorrect parameter
            requestException: request exception
        Returns:
            Boolean: true or false
        """
        try:
            omix_hlpr.parameter_check_for_repo_id(repo_id=repo_key)
        except paramException as exception:
            # the actual exception coming from parameter_check_for_repo_id states just repo_id
            # doing this to raise the same exception but different msg with repo_key
            raise paramException(
                title="Param Error",
                detail="Argument 'repo_key' is either empty or invalid. \
                        It should either be a string or an integer. Please try again.",
            ) from exception
        repo_key = omix_hlpr.make_repo_id_string(repo_key)
        repo_locked_status_messages = {
            "No_Status": f"Unable to fetch the lock status for omixatlas: {repo_key}."
            + " Please contact polly support for assistance.",
            True: f"Omixatlas {repo_key} is locked."
            + " Operations such as data ingestion and editing schema and changing properties of the omixatlas"
            + " are not permitted while the OA is locked.",
            False: f"Omixatlas {repo_key} is not locked."
            + " All operations on the omixatlas are permitted.",
        }
        try:
            response_omixatlas = self._get_omixatlas(repo_key)
            data = response_omixatlas.get("data").get("attributes")
            if "is_locked" in data:
                is_locked = data.get("is_locked")
                if is_locked in repo_locked_status_messages.keys():
                    print(repo_locked_status_messages[is_locked])
                    return is_locked
                else:
                    print(repo_locked_status_messages["No_Status"])
                    return None
            else:
                print(repo_locked_status_messages["No_Status"])
                return
        except Exception as err:
            print(
                f" Error in getting the lock status for omixatlas: {repo_key}."
                + f" ERROR: {err}"
            )
            return

    @Track.track_decorator
    def _fetch_quilt_metadata(self, repo_key: str, dataset_id: str) -> dict:
        """
        This function is used to get the quilt sample level metadata as a dataframe.
        Args:
            repo_key(str/int): repo_name/repo_id of the repository.
            dataset_id(str): dataset_id of the dataset.
        Raises:
              paramException:
              RequestFailureException:
        Returns:
            Quilt metadata in json format is returned.
        """
        omix_hlpr.check_params_for_fetch_quilt_metadata(repo_key, dataset_id)
        repo_summary = self.omixatlas_summary(repo_key)
        repo_id = repo_summary.get("data", "").get("repo_id")  # Extracting repo_id
        # getting dataset level metadata using download_metadata function
        with TempDir() as dir_path:
            self.download_metadata(repo_id, dataset_id, dir_path)
            filepath = os.path.join(dir_path, f"{dataset_id}.json")
            metadata = helpers.read_json(filepath)
        package = metadata["package"] + "/"
        file_id = helpers.remove_prefix(metadata["key"], package)
        url = self.discover_url + f"/repositories/{repo_id}/files/{file_id}"
        # get request to fetch quilt metadata
        response = self.session.get(url)
        error_handler(response)
        return response.json().get("data", "").get("attributes", "").get("metadata")


if __name__ == "__main__":
    client = OmixAtlas()
