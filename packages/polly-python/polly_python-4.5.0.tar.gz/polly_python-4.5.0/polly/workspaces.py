from polly.auth import Polly
from polly.errors import (
    InvalidParameterException,
    error_handler,
    InvalidPathException,
    AccessDeniedError,
    InvalidWorkspaceDetails,
    InvalidDirectoryPath,
)
from polly import helpers
from polly import constants as const
import logging
import pandas as pd
import json
import os
from polly.help import example
from polly.tracking import Track
from datetime import datetime
import math


class Workspaces:
    """
    This class contains functions to interact with workspaces on Polly. Users can create a workspace, fetch list\
 of workspaces, upload data to workspace and download data from workspace. To get started, users need to \
initialize a object that can use all function and methods of Workspaces class.

    Args:
        token (str): Authentication token from polly

    Usage:
        from polly.workspaces import Workspaces

        workspaces = Workspaces(token)
    """

    example = classmethod(example)

    def __init__(self, token=None, env="", default_env="polly") -> None:
        # check if COMPUTE_ENV_VARIABLE present or not
        # if COMPUTE_ENV_VARIABLE, give priority
        env = helpers.get_platform_value_from_env(
            const.COMPUTE_ENV_VARIABLE, default_env, env
        )
        self.session = Polly.get_session(token, env=env)
        self.base_url = f"https://apis.{self.session.env}.elucidata.io/mithoo"
        self.base_url_auth = f"https://apis.{self.session.env}.elucidata.io/auth"
        self.resource_url = f"{self.base_url}/workspaces"
        self.resource_url_search = f"{self.base_url}/_search"
        if self.session.env == "polly":
            self.env_string = "prod"
        elif self.session.env == "testpolly":
            self.env_string = "test"
        else:
            self.env_string = "devenv"

    @Track.track_decorator
    def create_workspace(self, name: str, description=None):
        """
        This function create workspace on Polly.
        Returns a Dictionary object like this
                        ``{
                        'id': 9999,
                        'name': 'rrrrr',
                        'active': True,
                        'description': 'for docu',
                        'created_time': '2022-03-16 11:08:47.127260',
                        'last_modified': '2022-03-16 11:08:47.127260',
                        'creator': 1127,
                        'project_property': {
                            'type': 'workspaces',
                            'labels': ''
                        },
                        'organisation': 1
                        }``

        Args:
              name (str): name of the workspace
              description (str, optional): general information about workspace


        """
        url = self.resource_url
        payload = {
            "data": {
                "type": "workspaces",
                "attributes": {
                    "name": name,
                    "description": description,
                    "project_property": {"type": "workspaces", "labels": ""},
                },
            }
        }
        response = self.session.post(url, data=json.dumps(payload))
        error_handler(response)
        attributes = response.json()["data"]["attributes"]
        logging.basicConfig(level=logging.INFO)
        logging.info("Workspace Created !")
        return attributes

    @Track.track_decorator
    def fetch_my_workspaces(self):
        """
        This function fetch workspaces from Polly.

        Args:
              None: None

        Returns:
              Table: A table with workspace specific attributes
        """
        all_details = self._fetch_workspaces_iteratively()
        pd.set_option("display.max_columns", 20)
        dataframe = pd.DataFrame.from_dict(
            pd.json_normalize(all_details), orient="columns"
        )
        dataframe.rename(
            columns={"id": "Workspace_id", "name": "Workspace_name"}, inplace=True
        )
        df = dataframe.sort_values(by="last_modified", ascending=False)
        df = df.reset_index()
        df.drop("index", axis=1, inplace=True)
        return df

    def _fetch_workspaces_iteratively(self):
        """
        Fetch all workspaces iteratively by making api calls until links is None.
        """
        url = self.resource_url_search
        all_details = []
        from_index = 0
        size = 20
        while True:
            payload = {
                "from": from_index,
                "size": size,
                "sort": [{"created_date": {"order": "desc"}}],
                "query": {
                    "nested": {
                        "path": "permissions",
                        "query": {"match": {"permissions.user_id": "{user_id}"}},
                    }
                },
            }
            response = self.session.post(url, data=json.dumps(payload))
            error_handler(response)
            data = response.json()["hits"]["hits"]
            total_hits = response.json()["hits"]["total"]["value"]
            for workspace_details in data:
                modified_workspace_details = self._modify_data(workspace_details)
                all_details.append(modified_workspace_details)
            from_index += size
            if from_index >= total_hits:
                break
        return all_details

    def _modify_data(self, data):
        """
        Removing less informative fields and making information user friendly
        """
        data_dict = data.get("_source")
        # Extracting necessary fields
        modified_data = {
            "id": data_dict.get("id"),
            "name": data_dict.get("name", ""),
            "status": "active" if data_dict.get("status") == 1 else "archived",
            "description": data_dict.get("description", ""),
            "last_modified": datetime.fromtimestamp(
                data_dict.get("modified_date", 0)
            ).strftime("%Y-%m-%d %H:%M:%S"),
            "tag_names": data_dict.get("tags", []),
            "favourite": False,
            "watch": False,
        }

        # Extract permissions
        permissions = data_dict.get("permissions")
        if permissions:
            modified_data["watch"] = permissions[0].get("watch", False)
            modified_data["favourite"] = permissions[0].get("is_bookmarked", False)

        return modified_data

    @Track.track_decorator
    def list_contents(self, workspace_id: str):
        """
        This function fetches contents of a workspace from Polly.

        Args:
            workspace_id : workspace id for the target workspace.

        Returns:
            Table: it will return a table with attributes.
        """
        url = f"{self.resource_url}/{workspace_id}/_search"
        from_index = 0
        fixed_size = 20
        details_list = []
        response_columns = ["file_name", "size", "last_modified"]
        while True:
            payload = {
                "from": from_index,
                "size": fixed_size,
                "query": {
                    "bool": {
                        "should": [
                            {
                                "bool": {
                                    "must": [
                                        {
                                            "term": {
                                                "_index": {"value": "{document_index}"}
                                            }
                                        },
                                        {
                                            "term": {
                                                "workspace_id": {"value": workspace_id}
                                            }
                                        },
                                        {
                                            "term": {
                                                "parent_id": {"value": workspace_id}
                                            }
                                        },
                                    ]
                                }
                            },
                            {
                                "bool": {
                                    "must": [
                                        {
                                            "term": {
                                                "_index": {"value": "{workspace_index}"}
                                            }
                                        },
                                        {
                                            "nested": {
                                                "path": "permissions",
                                                "query": {
                                                    "match": {
                                                        "permissions.user_id": {
                                                            "query": "{user_id}"
                                                        }
                                                    }
                                                },
                                            }
                                        },
                                    ]
                                }
                            },
                        ]
                    }
                },
            }
            response = self.session.post(url, data=json.dumps(payload))
            error_handler(response)
            total_hits = response.json()["hits"]["total"]["value"]
            data = response.json()["hits"]["hits"]
            columns = ["entity_name", "size", "modified_date"]
            for i in data:
                file_name = i.get("_source").get(columns[0])
                size = i.get("_source").get(
                    columns[1], "-"
                )  # If size is not present, set to "-"

                # Convert size
                if size != "-":
                    size = self.convert_size(size)

                last_modified = i.get("_source").get(columns[2])
                if last_modified is None:
                    last_modified = "-"
                else:
                    dt_object = datetime.fromtimestamp(last_modified)
                    formatted_date = dt_object.strftime("%Y-%m-%d %H:%M:%S")
                    last_modified = formatted_date

                details_list.append([file_name, size, last_modified])

            from_index += fixed_size
            if from_index >= total_hits:
                break
        df = pd.DataFrame(details_list, columns=response_columns)
        return df

    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    @Track.track_decorator
    def create_copy(
        self, source_id: int, source_path: str, destination_id: int, destination_path=""
    ) -> None:
        """
        Function to create a copy of files/folders existing in a workspace into another workspace.

        Args:
              source_id (int): workspace id of the source workspace where the file/folder exists
              source_path (str): file/folder path on the source workspace to be copied
              destination_id (int): workspace id of the destination workspace where the file/folder is to be copied
              destination_path (str, optional): optional parameter to specify the destination path

        Raises:
              InvalidParameterException: when the parameter like source id is invalid
              InvalidPathException: when the source path is invalid
        """
        if not (source_id and isinstance(source_id, int)):
            raise InvalidParameterException("source_id")
        if not (destination_id and isinstance(destination_id, int)):
            raise InvalidParameterException("destination_id")
        if not (source_path and isinstance(source_path, str)):
            raise InvalidParameterException("source_path")
        url = f"{self.base_url}/projects/{destination_id}/files/{destination_path}"
        source_key = f"{source_id}/{source_path}"
        params = {"source": "workspace", "source_workspace_id": source_id}
        sts_url = f"{self.base_url}/projects/{source_id}/credentials/files"
        creds = self.session.get(sts_url)
        error_handler(creds)
        credentials = helpers.get_sts_creds(creds.json())
        bucket = f"mithoo-{self.env_string}-project-data-v1"
        s3_path = f"{bucket}/{source_id}/"
        s3_path = f"s3://{helpers.make_path(s3_path, source_path)}"
        payload = helpers.get_workspace_payload(
            s3_path, credentials, source_key, source_path
        )
        response = self.session.post(url, data=json.dumps(payload), params=params)
        error_handler(response)
        message = response.json()["data"][0].get("attributes", {}).get("body")
        print(message)
        links = response.json().get("included")[0].get("links")
        url = f"{self.base_url}{links.get('self')}"
        while True:
            response = self.session.get(url)
            if response.json().get("errors"):
                error_handler(response)
            status = response.json()["primary_data"].get("status")
            if status != "INITIATED":
                break
        print("Copy Operation Successful!")

    @Track.track_decorator
    def upload_to_workspaces(
        self, workspace_id: int, workspace_path: str, local_path: str
    ) -> None:
        """
        Function to upload files/folders to workspaces.

        Args:
              workspace_id (int): id of the workspace where file need to uploaded
              workspace_path (str): path where the file/folder is to be uploaded. \
              The workspace path should be prefixed with "polly://". Creates the folder if provided folder path doesn't exist.
              local_path (str): uploaded file/folder path

        Raises:
              InvalidParameterException: when the parameter like workspace id is invalid
              InvalidPathException: when the file to path is invalid

        """
        if not (workspace_id and isinstance(workspace_id, int)):
            raise InvalidParameterException("workspace_id")
        if not (local_path and isinstance(local_path, str)):
            raise InvalidParameterException("local_path")
        if not (workspace_path and isinstance(workspace_path, str)):
            raise InvalidParameterException("workspace_path")
        isExists = os.path.exists(local_path)
        if not isExists:
            raise InvalidPathException
        # check for access rights for the workspace_id
        workspace_path = workspace_path.strip()
        access_workspace = helpers.workspaces_permission_check(self, workspace_id)
        if not access_workspace:
            raise AccessDeniedError(
                detail=f"Access denied to workspace-id - {workspace_id}"
            )
        if workspace_path.startswith("polly://"):
            workspace_path = workspace_path.split("polly://")[1]

        # If local_path is a file, append its name to workspace_path
        if os.path.isfile(local_path):
            file_name = os.path.basename(local_path)
            if not workspace_path.endswith(file_name):
                workspace_path = os.path.join(workspace_path, file_name)

        s3_path, credentials = self._s3_util(workspace_id, workspace_path)
        helpers.upload_to_S3(s3_path, local_path, credentials)
        logging.basicConfig(level=logging.INFO)
        logging.info(f"Upload successful on workspace-id={workspace_id}.")

    @Track.track_decorator
    def download_from_workspaces(
        self,
        workspace_id: int,
        workspace_path: str,
        local_path: str,
        copy_workspace_path: bool = True,
    ) -> None:
        """
        Function to download files/folders from workspaces.
        A message will be displayed on the status of the operation.

        Args:
              workspace_id (int): Id of the workspace where file needs to uploaded
              workspace_path (str): Downloaded file on workspace. The workspace path should be prefixed with "polly://"
              copy_workspace_path (bool): Flag indicating whether the workspace path needs to copied in the working directory

        Returns:
              None

        Raises:
              InvalidPathException: Invalid file path provided
              OperationFailedException: Failed download
              InvalidParameterException: Invalid parameter passed
        """
        if not (workspace_id and isinstance(workspace_id, int)):
            raise InvalidParameterException("workspace_id")
        if not (workspace_path and isinstance(workspace_path, str)):
            raise InvalidParameterException("workspace_path")
        # check for access rights for the workspace_id
        access_workspace = helpers.workspaces_permission_check(self, workspace_id)
        if not access_workspace:
            raise AccessDeniedError(
                detail=f"Access denied to workspace-id - {workspace_id}"
            )
        isExists = os.path.isdir(local_path)
        if not isExists:
            raise InvalidDirectoryPath(local_path)
        if workspace_path.startswith("polly://"):
            workspace_path = workspace_path.split("polly://")[1]
        s3_path, credentials = self._s3_util(workspace_id, workspace_path)
        helpers.download_from_S3(
            s3_path, workspace_path, credentials, local_path, copy_workspace_path
        )
        logging.basicConfig(level=logging.INFO)
        logging.info(f"Download successful to path={local_path}")

    def sync_data(self, workspace_id: int, source_path: str, destination_path: str):
        """
        Function to sync directory to or from workspaces and local.

        Args:
              workspace_id (int): id of the workspace which is used for sync
              source_path (str): path for the directory that is to be used for sync. \
              Can be local path or a workspace path. The workspace path should be prefixed with "polly://".
              destination_path (str): path for the directory that is to be used for sync. \
              Can be local path or a workspace path. \
              The workspace path should be prefixed with "polly://".Creates the folder if provided folder path doesn't exist.

        Raises:
              InvalidParameterException: when the parameter like workspace id is invalid
              InvalidDirectoryPath: when the folder to path is invalid
              InvalidWorkspaceDetails: when the workspace path is not prefixed with "polly://"
        """
        if not (workspace_id and isinstance(workspace_id, int)):
            raise InvalidParameterException("workspace_id")
        if not (source_path and isinstance(source_path, str)):
            raise InvalidParameterException("local_path")
        if not (destination_path and isinstance(destination_path, str)):
            raise InvalidParameterException("workspace_path")
        if source_path.startswith("polly://"):
            self._sync_local(workspace_id, source_path, destination_path)
        elif destination_path.startswith("polly://"):
            self._sync_s3(workspace_id, source_path, destination_path)
        else:
            raise InvalidWorkspaceDetails()

    def _sync_s3(self, workspace_id, source_path, destination_path):
        """
        Function to sync s3 directory with the local directory
        """
        isExists = os.path.isdir(source_path)
        if not isExists:
            raise InvalidDirectoryPath(source_path)
        workspace_path = destination_path.split("polly://")[1]
        s3_path, credentials = self._s3_util(workspace_id, workspace_path)
        helpers.upload_to_S3(s3_path, source_path, credentials)
        logging.basicConfig(level=logging.INFO)
        logging.info(f"Sync successful on workspace-id={workspace_id}.")

    def _sync_local(self, workspace_id, workspace_path, local_path):
        """
        Function to sync local directory with the s3 path
        """
        isExists = os.path.isdir(local_path)
        if not isExists:
            raise InvalidDirectoryPath(local_path)

        workspace_path = workspace_path.split("polly://")[1]
        s3_path, credentials = self._s3_util(workspace_id, workspace_path)
        helpers.download_from_S3(s3_path, workspace_path, credentials, local_path)
        logging.basicConfig(level=logging.INFO)
        logging.info(f"Sync successful on workspace-id={workspace_id}.")

    def _s3_util(self, workspace_id, workspace_path):
        """
        Function to return s3 client credentials and s3_path
        """
        sts_url = f"{self.base_url}/projects/{workspace_id}/credentials/files"
        creds = self.session.get(sts_url)
        error_handler(creds)
        credentials = helpers.get_sts_creds(creds.json())
        bucket = f"mithoo-{self.env_string}-project-data-v1"
        s3_path = f"{bucket}/{workspace_id}/"
        s3_path = f"s3://{helpers.make_path(s3_path, workspace_path)}"
        return s3_path, credentials
