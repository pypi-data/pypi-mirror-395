from polly.auth import Polly
from polly.errors import (
    ResourceNotFoundError,
    BadRequestError,
    UnauthorizedException,
    InvalidParameterException,
    QueryFailedException,
)
from polly import helpers
from polly import constants as const
from polly.tracking import Track

import requests
import json
import os
from requests import Response
import time


def get_error_message(response: Response):
    """Helper function to extract error message from response"""
    if "errors" in response.json():
        errors = response.json()["errors"]
        if isinstance(errors, list) and errors:
            return errors[0].get("detail", "Unknown error")
        return errors or "Unknown error"
    return "Unknown error"


def handle_success_and_error_response(response: Response):
    error_message = "Unknown error"

    if response.status_code in [200, 201]:
        return response.json()

    if response.status_code == 204:
        return None

    if response.status_code == 401:
        raise UnauthorizedException()

    error_message = get_error_message(response)

    if response.status_code == 400:
        raise BadRequestError(detail=error_message)
    elif response.status_code == 404:
        raise ResourceNotFoundError(detail=error_message)
    elif response.status_code == 409:
        raise Exception(f"Conflict: {error_message}")

    if int(response.status_code) >= 500:
        raise Exception(f"Server error: {error_message}")

    response.raise_for_status()


def _get_latest_version_kg(session, polly_kg_neo4j_endpoint, kg_id):
    """Get the latest version of the knowledge graph with the specified kg_id.

    Args:
        session: The authenticated session to make requests.
        polly_kg_neo4j_endpoint: The endpoint for the Polly Knowledge Graph API.
        kg_id (str): The ID of the knowledge graph.

    Returns:
        tuple: A tuple containing the kg_id and version_id of the latest version.

    Raises:
        ResourceNotFoundError: If no knowledge graph with the specified kg_id is found.
    """
    response = session.get(f"{polly_kg_neo4j_endpoint}/kg/{kg_id}")
    handle_success_and_error_response(response)
    data = response.json().get("data", {})
    if not data:
        raise ResourceNotFoundError(
            detail=f"No knowledge graph with ID '{kg_id}' found."
        )
    latest_version = data.get("attributes", {})
    return (
        kg_id,
        latest_version.get("version_id"),
    )


def _get_default_kg(session, polly_kg_neo4j_endpoint):
    kg_url = f"{polly_kg_neo4j_endpoint}/kg"
    response = session.get(kg_url)
    handle_success_and_error_response(response)
    data = response.json().get("data", [])
    if not data:
        raise ResourceNotFoundError(detail="No knowledge graphs found.")
    if len(data) > 1:
        kg_ids = {kg.get("kg_id") for kg in data}
        if len(kg_ids) == 1:
            return _get_latest_version_kg(
                session, polly_kg_neo4j_endpoint, kg_ids.pop()
            )
        else:
            raise BadRequestError(
                detail="Multiple knowledge graphs found for the given org. Please specify a kg_id and version_id."
            )
    default_kg = data[0]
    latest_kg_response = session.get(
        f"{polly_kg_neo4j_endpoint}/kg/{default_kg.get('kg_id')}"
    )
    handle_success_and_error_response(latest_kg_response)
    latest_kg = latest_kg_response.json().get("data", {}).get("attributes", {})

    return (
        latest_kg.get("kg_id"),
        latest_kg.get("version_id"),
    )


def _validate_kg_version_exists(session, polly_kg_neo4j_endpoint, kg_id, version_id):
    """Validate if the specified kg_id and version_id exist in the Polly Knowledge Graph.

    Args:
        session: The authenticated session to make requests.
        polly_kg_neo4j_endpoint: The endpoint for the Polly Knowledge Graph API.
        kg_id (str): The ID of the knowledge graph.
        version_id (str): The version ID of the knowledge graph.

    Returns:
        tuple: A tuple containing the kg_id and version_id if they exist.

    Raises:
        ResourceNotFoundError: If the specified kg_id or version_id does not exist.
    """
    response = session.get(
        f"{polly_kg_neo4j_endpoint}/kg/{kg_id}/versions/{version_id}"
    )
    handle_success_and_error_response(response)
    data = response.json().get("data", [])
    if not data:
        raise ResourceNotFoundError(
            detail=f"No knowledge graphs with ID '{kg_id}' and version '{version_id}' found."
        )
    return kg_id, version_id


class PollyKG:
    """The PollyKG class provides an interface to interact with the Polly Knowledge Graph (KG) API.\
     It enables users to execute and manage Cypher queries, retrieve node and relationship data,\
     and analyze graph structures efficiently. This class simplifies access to the KG engine, allowing seamless\
     querying and data exploration. It is designed for users who need to extract insights from complex graph-based datasets.

    Args:
        token (str): Authentication token from polly

    Usage:
        from polly.polly_kg import PollyKG

        kg = PollyKG(token)
    """

    def __init__(
        self,
        token=None,
        env="",
        default_env="polly",
        kg_id=None,
        version_id=None,
    ) -> None:
        # Initialize a PollyKG instance.

        # Args:
        #     token (str, optional): Authentication token. Defaults to None.
        #     env (str, optional): Environment override. Defaults to "".
        #     default_env (str, optional): Default environment if not specified. Defaults to "polly".

        env = helpers.get_platform_value_from_env(
            const.COMPUTE_ENV_VARIABLE, default_env, env
        )
        self.session = Polly.get_session(token, env=env)
        self.polly_kg_endpoint = (
            f"https://sarovar.{self.session.env}.elucidata.io/polly_kg"
        )
        self.polly_kg_neo4j_endpoint = (
            f"https://apis.{self.session.env}.elucidata.io/polly-kg"
        )

        if kg_id is None and version_id is not None:
            raise InvalidParameterException("kg_id")

        if kg_id is None and version_id is None:
            self.kg_id, self.version_id = _get_default_kg(
                self.session, self.polly_kg_neo4j_endpoint
            )
        if kg_id is not None and version_id is not None:
            self.kg_id, self.version_id = _validate_kg_version_exists(
                self.session, self.polly_kg_neo4j_endpoint, kg_id, version_id
            )

        if kg_id is not None and version_id is None:
            self.kg_id, self.version_id = _get_latest_version_kg(
                self.session, self.polly_kg_neo4j_endpoint, kg_id
            )

    def __repr__(self):
        return f"PollyKG(kg_id={self.kg_id}, version_id={self.version_id})"

    @Track.track_decorator
    def run_query(self, query: str, query_type: str = "CYPHER") -> dict:
        """
        Execute a graph query on the specified KG version.

        This function submits the query to Polly KG, tracks its status, and waits
        until it completes. Once complete, it returns the result.

        Args:
            query (str): The query string to be executed.
            query_type (str): The query language type. Accepts "CYPHER".

        Returns:
            dict: Query result in parsed JSON format.

        Raises:
            InvalidParameterException: If query is empty.
            QueryFailedException: If query execution fails.
        """
        if not query or query == "":
            raise InvalidParameterException("query")
        query_url = f"{self.polly_kg_neo4j_endpoint}/kg/{self.kg_id}/versions/{self.version_id}/queries/"
        is_async = True
        if query_type == "NLQ":
            is_async = False  # NLQ queries are always synchronous
        payload = {
            "data": {
                "type": "kg_query",
                "attributes": {
                    "query_string": query,
                    "query_type": query_type,
                    "is_async": is_async,
                },
            }
        }
        try:
            query_response = self.session.post(query_url, data=json.dumps(payload))

            handle_success_and_error_response(query_response)

            data = query_response.json().get("data")
            query_id = data.get("attributes", {}).get("query_id")
            print(f"Query submitted successfully. Query ID: {query_id}. ")

            download_url = f"{query_url}{query_id}/results?download=true"

            status_response = self.session.get(download_url)

            status = (
                status_response.json()
                .get("data", {})
                .get("attributes", {})
                .get("status")
            )

            while status in ("IN_PROGRESS", "QUEUED"):
                time.sleep(5)  # Wait for 5 seconds before checking the status again
                status_response = self.session.get(download_url)
                status = (
                    status_response.json()
                    .get("data", {})
                    .get("attributes", {})
                    .get("status")
                )

            if status == "COMPLETED":
                result_s3_signed_url = (
                    status_response.json()
                    .get("data", {})
                    .get("attributes", {})
                    .get("metadata", {})
                    .get("results", {})
                    .get("url")
                )
                result_json = requests.get(result_s3_signed_url)
                return result_json.json()
            elif status == "FAILED":
                metadata = (
                    status_response.json()
                    .get("data", {})
                    .get("attributes", {})
                    .get("metadata", {})
                )
                # Try new format first: metadata.results.error and metadata.results.details
                results = metadata.get("results", {})
                if results and ("error" in results or "details" in results):
                    error_type = results.get("error", "Unknown error")
                    error_details = results.get("details", "")
                    error_message = (
                        f"{error_type}: {error_details}"
                        if error_details
                        else error_type
                    )
                else:
                    # Fallback to old format: metadata.error
                    error_message = metadata.get(
                        "error", "Query failed without a specific error message."
                    )

                print(f"Query failed. Query ID: {query_id}. Error: {error_message}")
                raise QueryFailedException(error_message)
        except Exception as e:
            print(e)
            raise e

    @Track.track_decorator
    def submit_query(self, query: str, query_type: str = "CYPHER") -> dict:
        """
        Submit a graph query on the specified KG version.

        This function submits the query to Polly KG and returns the Query ID.

        Args:
            query (str): The query string to be executed.
            query_type (str): The query language type. Accepts "CYPHER".

        Returns:
            query_id (str): Unique Identifier for the query submitted.

        Raises:
            InvalidParameterException: If query is empty.
            QueryFailedException: If query execution fails.
        """
        if not query or query == "":
            raise InvalidParameterException("query")
        query_url = f"{self.polly_kg_neo4j_endpoint}/kg/{self.kg_id}/versions/{self.version_id}/queries/"
        is_async = True
        if query_type == "NLQ":
            is_async = False  # NLQ queries are always synchronous
        payload = {
            "data": {
                "type": "kg_query",
                "attributes": {
                    "query_string": query,
                    "query_type": query_type,
                    "is_async": is_async,
                },
            }
        }
        try:
            query_response = self.session.post(query_url, data=json.dumps(payload))

            handle_success_and_error_response(query_response)

            data = query_response.json().get("data")
            return data.get("attributes", {}).get("query_id")
        except Exception as e:
            print(e)
            raise e

    @Track.track_decorator
    def get_query_status(self, query_id: str) -> dict:
        """
        Fetch the status of a  submitted query.

        Args:
            query_id (str): Unique ID of the submitted query.

        Returns:
            dict: A dictionary containing current status of the query (e.g., "IN_PROGRESS", "COMPLETED").

        Raises:
            InvalidParameterException: If query_id is not provided.
        """
        if not query_id or query_id == "":
            raise InvalidParameterException("query_id")
        query_url = f"{self.polly_kg_neo4j_endpoint}/kg/{self.kg_id}/versions/{self.version_id}/queries/{query_id}"
        try:
            response = self.session.get(query_url)
            handle_success_and_error_response(response)
            data = response.json().get("data", {})
            return {"status": data.get("attributes", {}).get("status")}
        except Exception as e:
            print(e)
            raise e

    @Track.track_decorator
    def get_query_results(self, query_id: str) -> None:
        """Get the results of a query by its ID.

        Args:
            query_id (str): The ID of the query whose results you want to get.

        Returns:
            dict: Query result in parsed JSON format.

        Raises:
            InvalidParameterException: If the query_id is empty or None.
            QueryFailedException: If query execution failed.
            RequestFailureException: If the request fails due to an unexpected error.

        """
        if not query_id or query_id == "":
            raise InvalidParameterException("query_id")
        base_url = f"{self.polly_kg_neo4j_endpoint}/kg/{self.kg_id}/versions/{self.version_id}/queries"
        query_url = f"{base_url}/{query_id}/results?download=true"
        try:
            response = self.session.get(query_url)
            handle_success_and_error_response(response)
            data = response.json().get("data", {})

            status = data.get("attributes", {}).get("status")
            if status == "FAILED":
                metadata = data.get("attributes", {}).get("metadata", {})
                # Try new format first: metadata.results.error and metadata.results.details
                results = metadata.get("results", {})
                if results and ("error" in results or "details" in results):
                    error_type = results.get("error", "Unknown error")
                    error_details = results.get("details", "")
                    error_message = (
                        f"{error_type}: {error_details}"
                        if error_details
                        else error_type
                    )
                else:
                    # Fallback to old format: metadata.error
                    error_message = metadata.get(
                        "error", "Query failed without a specific error message."
                    )

                print(f"Query failed. Query ID: {query_id}. Error: {error_message}")
                raise QueryFailedException(error_message)
            result_s3_signed_url = (
                data.get("attributes", {})
                .get("metadata", {})
                .get("results", {})
                .get("url")
            )
            if not result_s3_signed_url:
                raise ResourceNotFoundError("Query results not found.")

            result_json = requests.get(result_s3_signed_url)
            return result_json.json()
        except Exception as e:
            print(e)
            raise

    @Track.track_decorator
    def download_query_results(self, query_id: str, folder: str = "./results") -> None:
        """Download the results of a query by its ID.
            If the download directory does not exist, it will be created.
            The results will be saved in a ./results directory/query_id.json with the filename as query_id.json.

        Args:
            query_id (str): The ID of the query whose results you want to download.
            folder (str): The directory where the results should be saved.

        Returns:
            str: Path to the downloaded results.

        Raises:
            InvalidParameterException: If the query_id is empty or None.
            QueryFailedException: If query execution failed.
            RequestFailureException: If the request fails due to an unexpected error.

        """
        if not query_id or query_id == "":
            raise InvalidParameterException("query_id")
        base_url = f"{self.polly_kg_neo4j_endpoint}/kg/{self.kg_id}/versions/{self.version_id}/queries"
        query_url = f"{base_url}/{query_id}/results?download=true"
        try:
            response = self.session.get(query_url)
            handle_success_and_error_response(response)
            data = response.json().get("data", {})

            status = data.get("attributes", {}).get("status")
            if status == "FAILED":
                metadata = data.get("attributes", {}).get("metadata", {})
                # Try new format first: metadata.results.error and metadata.results.details
                results = metadata.get("results", {})
                if results and ("error" in results or "details" in results):
                    error_type = results.get("error", "Unknown error")
                    error_details = results.get("details", "")
                    error_message = (
                        f"{error_type}: {error_details}"
                        if error_details
                        else error_type
                    )
                else:
                    # Fallback to old format: metadata.error
                    error_message = metadata.get(
                        "error", "Query failed without a specific error message."
                    )

                print(f"Query failed. Query ID: {query_id}. Error: {error_message}")
                raise QueryFailedException(error_message)
            result_s3_signed_url = (
                data.get("attributes", {})
                .get("metadata", {})
                .get("results", {})
                .get("url")
            )
            if not result_s3_signed_url:
                raise ResourceNotFoundError("Query results not found.")

            with requests.get(result_s3_signed_url, stream=True) as r:
                r.raise_for_status()
                os.makedirs(folder, exist_ok=True)
                file_path = os.path.join(folder, f"{query_id}.json")
                with open(file_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1048576):
                        if chunk:
                            f.write(chunk)
            print(f"Results downloaded successfully to {file_path}")
            return file_path
        except Exception as e:
            print(e)
            raise

    def get_summary(self) -> dict:
        """Retrieve a summary of the Polly Knowledge Graph.

        Returns:
            dict: A dictionary containing summary information about the graph,
                 such as node counts, edge counts, and other metadata.

        Raises:
            ResourceNotFoundError: Raised when the specified graph summary does not exist.
            AccessDeniedError: Raised when the user does not have permission to access the graph summary.
            RequestFailureException: Raised when the request fails due to an unexpected error.
        """
        try:
            response = self.session.get(
                f"{self.polly_kg_neo4j_endpoint}/kg/{self.kg_id}/versions/{self.version_id}/summary"
            )
            return handle_success_and_error_response(response)
        except Exception as e:
            print(e)

    def get_schema(self) -> dict:
        """Retrieve the schema of the Polly Knowledge Graph.

        Returns:
            dict: A dictionary containing schema information about the graph,
                 such as node types, relationship types, and other metadata with descriptions.

        Raises:
            ResourceNotFoundError: Raised when the specified graph schema does not exist.
            AccessDeniedError: Raised when the user does not have permission to access the graph schema.
            RequestFailureException: Raised when the request fails due to an unexpected error.
        """
        try:

            # Always include description parameter
            params = {"description": "true", "custom_attribute": "true"}

            response = self.session.get(
                f"{self.polly_kg_neo4j_endpoint}/kg/{self.kg_id}/versions/{self.version_id}/schema",
                params=params,
            )
            schema_response = handle_success_and_error_response(response)

            # Transform new format to old format
            if schema_response and "data" in schema_response:
                transformed = self._transform_schema_to_legacy_format(
                    schema_response, self.kg_id, self.version_id
                )
                return transformed

            return schema_response
        except Exception as e:
            print(e)
            raise

    def _transform_schema_to_legacy_format(
        self, new_schema: dict, kg_id: str, version_id: str
    ) -> dict:
        """Transform new schema format to legacy format for backward compatibility.

        Args:
            new_schema (dict): The new schema format from the API
            kg_id (str): The knowledge graph ID
            version_id (str): The version ID

        Returns:
            dict: Schema in legacy format
        """
        data = new_schema.get("data", {})
        attributes = data.get("attributes", {})
        schema = attributes.get("schema", {})

        # Extract basic information
        node_types = schema.get("node_types", [])
        edge_types = schema.get("edge_types", [])
        nodes = schema.get("nodes", {})
        edges = schema.get("edges", {})

        # Transform nodes to legacy format
        transformed_nodes = {}
        for node_name, node_data in nodes.items():
            properties_dict = node_data.get("properties", {})
            node_description = node_data.get("description", "")

            # Convert properties from dict to array format
            properties_array = []

            for prop_name, prop_details in properties_dict.items():
                prop_type = prop_details.get("type", "String")
                prop_description = prop_details.get("description", "")

                # Build property object with name, type, and description
                prop_obj = {
                    "name": prop_name,
                    "type": prop_type,
                    "description": prop_description,
                }
                properties_array.append(prop_obj)

            transformed_nodes[node_name] = {
                "properties": properties_array,
            }

            # Add description if available
            if node_description:
                transformed_nodes[node_name]["description"] = node_description

        # Transform edges to legacy format
        transformed_edges = {}
        for edge_name, edge_data in edges.items():
            properties_dict = edge_data.get("properties", {})
            edge_description = edge_data.get("description", "")
            connections = edge_data.get("connections", [])

            # Convert properties from dict to array format
            properties_array = []
            for prop_name, prop_details in properties_dict.items():
                prop_type = prop_details.get("type", "String")
                prop_description = prop_details.get("description", "")

                # Build property object with name, type, and description
                prop_obj = {
                    "name": prop_name,
                    "type": prop_type,
                    "description": prop_description,
                }
                properties_array.append(prop_obj)

            # Transform connections from new format (in/out) to old format (from/to)
            # In new format: "out" is the target node, "in" is the source node
            # In old format: "from" is the source node (in), "to" is the target node (out)
            connections_array = []
            for conn in connections:
                connections_array.append(
                    {"from": conn.get("in"), "to": conn.get("out")}
                )

            transformed_edges[edge_name] = {
                "properties": properties_array,
                "connections": connections_array,
            }

            # Add description if available
            if edge_description:
                transformed_edges[edge_name]["description"] = edge_description

        # Build legacy format response
        from datetime import datetime

        legacy_format = {
            "data": {
                "type": "kg_schema",
                "attributes": {
                    "metadata": {
                        "name": "schema",
                        "kg_id": str(kg_id),
                        "kg_version": str(version_id),
                        "last_updated": datetime.utcnow().strftime(
                            "%Y-%m-%dT%H:%M:%SZ"
                        ),
                        "computed_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    },
                    "node_types": node_types,
                    "edge_types": edge_types,
                    "nodes": transformed_nodes,
                    "edges": transformed_edges,
                },
            }
        }

        return legacy_format

    @Track.track_decorator
    def get_all_kgs(
        self,
        include_unpublished: bool = False,
        include_instances: bool = False,
        include_terminated: bool = False,
    ) -> list:
        """Retrieve all available Knowledge Graphs.

        This function fetches a list of all available Knowledge Graphs (KGs)
        that the user has access to, including their metadata such as kg_id,
        kg_name, kg_description, version_id, created_at timestamp, and
        published status.

        Args:
            include_unpublished (bool, optional): Include unpublished knowledge graphs.
                Defaults to False.
            include_instances (bool, optional): Include instance information for each KG.
                When True, each KG will include an 'instances' array with details about
                available instances (instance_id, instance_type, CPU/RAM, etc.).
                Defaults to False.
            include_terminated (bool, optional): Include terminated instances in the response.
                Only applies when include_instances is True. Defaults to False.

        Returns:
            list: A list of dictionaries, where each dictionary contains:
                - kg_id (str): Unique identifier for the knowledge graph
                - kg_name (str): Name of the knowledge graph
                - kg_description (str): Description of the knowledge graph
                - version_id (int): Current version ID
                - created_at (int): Creation timestamp (Unix epoch in milliseconds)
                - published (bool): Whether the KG is published
                - instances (list, optional): Available when include_instances=True.
                  Each instance contains:
                    - instance_id (str): Unique identifier for the instance
                    - instance_type (str): Type/size of instance (e.g., "t3.medium")
                    - is_terminated (bool): Whether the instance is terminated
                    - default_instance (bool): Whether this is the default instance
                    - org_id (int): Organization ID
                    - created_at (int): Instance creation timestamp

        Raises:
            ResourceNotFoundError: Raised when no knowledge graphs are found.
            AccessDeniedError: Raised when the user does not have permission to access the KGs.
            RequestFailureException: Raised when the request fails due to an unexpected error.

        Example:
            >>> kg = PollyKG()
            >>> # Get only published KGs
            >>> kgs = kg.get_all_kgs()
            >>> for kg_info in kgs:
            ...     print(f"{kg_info['kg_name']} (ID: {kg_info['kg_id']})")
            base kg v3 (ID: 14_base_kg_v3)

            >>> # Get all KGs including unpublished ones with instance details
            >>> kgs_with_instances = kg.get_all_kgs(
            ...     include_unpublished=True,
            ...     include_instances=True,
            ...     include_terminated=True
            ... )
            >>> for kg_info in kgs_with_instances:
            ...     print(f"{kg_info['kg_name']} - {len(kg_info.get('instances', []))} instances")
        """
        try:
            kg_url = f"{self.polly_kg_neo4j_endpoint}/kg"

            # Build query parameters
            params = {}
            if include_unpublished:
                params["include_unpublished"] = "true"
            if include_instances:
                params["include_instances"] = "true"
            if include_terminated:
                params["include_terminated"] = "true"

            response = self.session.get(kg_url, params=params)
            handle_success_and_error_response(response)

            data = response.json().get("data", [])

            if not data:
                raise ResourceNotFoundError(detail="No knowledge graphs found.")

            return data

        except Exception as e:
            print(e)
            raise
