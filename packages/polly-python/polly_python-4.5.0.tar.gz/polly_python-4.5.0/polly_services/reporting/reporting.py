import os
from polly_interfaces.IReporting import IReporting
import json
import urllib.parse
import pandas as pd
from polly import helpers
from datetime import datetime
from urllib.parse import urlparse
from polly_services import polly_services_hlpr
from polly_services.reporting import reporting_hlpr
from polly.errors import (
    InvalidParameterException,
    error_handler,
    InvalidDirectoryPath,
)


class Reporting(IReporting):
    def __init__(self):
        pass

    def link_report(
        self,
        polly_session,
        repo_key: str,
        dataset_id: str,
        workspace_id: int,
        workspace_path: str,
        access_key: str,
    ):
        """
        This function is used to link a file (html or pdf) present in a workspace with the specified dataset in OmixAtlas.
        On success it displays the access key URL and a success message.
        Org admins can now link a report present in a workspace with the specified datasets in an OmixAtlas.
        Once a report is linked to a dataset in OmixAtlas, it can be fetched both from front-end and polly-python.
        A message will be displayed on the status of the operation.

        Args:
            repo_key (str): repo_name/repo_id of the repository to be linked
            dataset_id (str): dataset_id of the dataset to be linked
            workspace_id (str): workspace_id for the file which is to be linked
            workspace_path (str): workspace_path for the file which is to be linked
            access_key (str): access_key(private or public) depending upon the link access type to be generated.\
            If public, then anyone with a Polly account with the link will be able to see the report.\
            If private, only individuals who have access to the workspace where reports is stored will be able to see them.

        Raises:
            InvalidParameterException: invalid parameters

        Returns:
            None
        """
        if not (repo_key and isinstance(repo_key, str)):
            raise InvalidParameterException("repo_key")
        if not (dataset_id and isinstance(dataset_id, str)):
            raise InvalidParameterException("dataset_id")
        if not (workspace_id and isinstance(workspace_id, int)):
            raise InvalidParameterException("workspace_id")
        if not (workspace_id and isinstance(workspace_path, str)):
            raise InvalidParameterException("workspace_path")
        if not (
            access_key
            and isinstance(access_key, str)
            and access_key.lower() in ["private", "public"]
        ):
            raise InvalidParameterException("access_key")
        sts_url = f"{polly_session.base_url}/projects/{workspace_id}/credentials/files"
        access_url = f"https://{polly_session.session.env}.elucidata.io/manage"
        reporting_hlpr.verify_workspace_details(
            polly_session, workspace_id, workspace_path, sts_url
        )

        # get omixatlas details
        response_omixatlas = polly_services_hlpr.omixatlas_summary(
            polly_session, repo_key
        )
        data = response_omixatlas.get("data")
        repo_id = data.get("repo_id")

        # check existing access of file
        shared_id = reporting_hlpr.get_shared_id(
            polly_session, workspace_id, workspace_path
        )
        if shared_id is None:
            existing_access = "private"
        else:
            existing_access = "public"

        # if access key differ from existing access then change file access
        if access_key != existing_access:
            report_id = reporting_hlpr.get_report_id(
                polly_session, workspace_id, workspace_path
            )
            changed_file_link = reporting_hlpr.change_file_access(
                polly_session,
                access_key,
                workspace_id,
                workspace_path,
                access_url,
                report_id,
            )

        # add report as private report
        if access_key == "private":
            absolute_path = helpers.make_path(workspace_id, workspace_path)

            url = f"{polly_session.base_url}/v1/omixatlases/{repo_id}/reports"
            payload = {
                "data": {
                    "type": "dataset-reports",
                    "attributes": {
                        "dataset_id": f"{dataset_id}",
                        "absolute_path": f"{absolute_path}",
                    },
                }
            }

            response = polly_session.session.post(url, data=json.dumps(payload))
            error_handler(response)
            report_id = reporting_hlpr.get_report_id(
                polly_session, workspace_id, workspace_path
            )

            file_link = reporting_hlpr.make_private_link(
                workspace_id, workspace_path, access_url, report_id
            )

            print(
                f"File Successfully linked to dataset id = {dataset_id}. The URL for the {access_key} access is '{file_link}'"
            )

        # add report as public file
        elif access_key == existing_access == "public":
            file_link = f"{access_url}/shared/file/?id={shared_id}"
            self.link_report_url(polly_session, repo_key, dataset_id, file_link)

        else:
            file_link = changed_file_link
            self.link_report_url(polly_session, repo_key, dataset_id, changed_file_link)

    def link_report_url(
        self, polly_session, repo_key: str, dataset_id: str, url_to_be_linked: str
    ):
        """
        This function is used to link a URL with the specified dataset in OmixAtlas.
        A message will be displayed on the status of the operation.

        Args:
            repo_key (str): repo_name/repo_id of the repository to be linked
            dataset_id (str): dataset_id of the dataset to be linked
            url_to_be_linked (str): The url which is to be linked

        Raises:
            InvalidParameterException: invalid parameters

        Returns:
            None
        """
        if not (repo_key and isinstance(repo_key, str)):
            raise InvalidParameterException("repo_key")
        if not (dataset_id and isinstance(dataset_id, str)):
            raise InvalidParameterException("dataset_id")
        if not (url_to_be_linked and isinstance(url_to_be_linked, str)):
            raise InvalidParameterException("url")
        parsed_url = urlparse(url_to_be_linked)
        response_omixatlas = polly_services_hlpr.omixatlas_summary(
            polly_session, repo_key
        )
        data = response_omixatlas.get("data")
        repo_id = data.get("repo_id")
        # check for components in a url for a basic validation of url
        """
        Format of the parsed string with a sample URL - http://www.cwi.nl:80/%7Eguido/Python.html
        ParseResult(scheme='http', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html',
        params='', query='', fragment='')
        """
        if all([parsed_url.scheme, parsed_url.netloc, parsed_url.path]):
            report_url = f"{polly_session.base_url}/v1/omixatlases/{repo_id}/reports"
            payload = {
                "data": {
                    "type": "dataset-reports",
                    "attributes": {
                        "dataset_id": f"{dataset_id}",
                        "absolute_path": f"{url_to_be_linked}",
                    },
                }
            }
            response = polly_session.session.post(report_url, data=json.dumps(payload))
            error_handler(response)
            print(
                f"Dataset - {dataset_id} has been successfully linked with URL {url_to_be_linked} "
            )
        else:
            raise InvalidParameterException("url")

    def fetch_linked_reports(self, polly_session, repo_key: str, dataset_id: str):
        if not (repo_key and isinstance(repo_key, str)):
            raise InvalidParameterException("repo_key")
        if not (dataset_id and isinstance(dataset_id, str)):
            raise InvalidParameterException("dataset_id")
        response_omixatlas = polly_services_hlpr.omixatlas_summary(
            polly_session, repo_key
        )
        data = response_omixatlas.get("data")
        repo_id = data.get("repo_id")
        params = {"dataset_id": f"{dataset_id}"}
        url = f"{polly_session.base_url}/v1/omixatlases/{repo_id}/reports"
        response = polly_session.session.get(url, params=params)
        error_handler(response)
        report_list = response.json().get("data").get("attributes").get("reports")
        access_url = f"https://{polly_session.session.env}.elucidata.io/manage"
        if len(report_list) == 0:
            print("No Reports found, linked with the given details.")
        else:
            columns = ["Added_by", "Added_time", "URL", "Report_id"]
            all_details = []
            for items in report_list:
                details_list = []
                added_by = items.get("added_by")
                # convertime time fetched in miliseconds to datetime
                added_on = items.get("added_on") / 1000.0
                added_time = datetime.fromtimestamp(added_on).strftime(
                    "%d/%m/%Y %H:%M:%S"
                )
                if "url" in items:
                    """
                    Contents of dict items
                    {
                        "added_by": "circleci@elucidata.io",
                        "added_on": 1669722856247,
                        "report_id": "c048a786-988d-4ff0-96c4-56f06211c9b5",
                        "url": "https://github.com/ElucidataInc/PublicAssets"
                    }
                    """
                    # case where url is linked to the dataset
                    url = items.get("url")
                    report_id = items.get("report_id")
                    details_list.append(added_by)
                    details_list.append(added_time)
                    details_list.append(url)
                    details_list.append(report_id)
                    all_details.append(details_list)
                else:
                    """
                    Contents of dict items
                    {
                        "report_id": str(uuid.uuid4()),
                        "workspace_id": "1456",
                        "file_name": "myreport.html",
                        "absolute_path": "1456/myreport.html",
                        "added_by": "circleci@elucidata.io",
                        "added_on": 1669722856247
                    }
                    """
                    # case where a workspace file is linked to a dataset
                    absolute_path = items.get("absolute_path")
                    workspace_id, workspace_path = reporting_hlpr.split_workspace_path(
                        absolute_path
                    )
                    try:
                        sts_url = f"{polly_session.base_url}/projects/{workspace_id}/credentials/files"
                        status = reporting_hlpr.check_is_file(
                            polly_session, sts_url, workspace_id, workspace_path
                        )
                    except Exception:
                        print(
                            f"Not enough permissions for the workspace_id : {workspace_id}. Please contact Polly Support."
                        )
                        continue
                    if not status:
                        # the file does not exist in the workspace, hence skipping this file path
                        print(
                            f"The workspace path '{workspace_path}' is invalid. Please contact Polly Support."
                        )
                        continue
                    shared_id = reporting_hlpr.get_shared_id(
                        polly_session, workspace_id, workspace_path
                    )
                    # file_url will be private or public based on shared_id
                    report_id = reporting_hlpr.get_report_id(
                        polly_session, workspace_id, workspace_path
                    )
                    file_url = reporting_hlpr.return_workspace_file_url(
                        shared_id, access_url, workspace_id, workspace_path, report_id
                    )
                    report_id = items.get("report_id")
                    details_list.append(added_by)
                    details_list.append(added_time)
                    details_list.append(file_url)
                    details_list.append(report_id)
                    all_details.append(details_list)
            if len(all_details) == 0:
                print("No Reports to be displayed.")
            else:
                df = pd.DataFrame(all_details, columns=columns)
                pd.set_option("display.max_colwidth", None)
                return df

    def _extract_file_ids(self, urls_list):
        file_id_list = []
        for url in urls_list:
            parsed_url = urllib.parse.urlparse(url)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            file_id = query_params.get("id")
            if file_id:
                file_id_list.append(file_id[0])
            else:
                print(f"ID not found in the file URL: {url}")
        return file_id_list

    def download_linked_reports(
        self, polly_session, repo_key: str, dataset_id: str, local_folder_path: str
    ):
        """Download linked reports to the local path

        Args:
            polly_session : polly_session variable
            repo_key (str): repo_key for the omixatlas
            dataset_id (str): dataset_id for the repo
            local_folder_path (str): _description_
        """
        # sanity check of variables
        if not (repo_key and isinstance(repo_key, str)):
            raise InvalidParameterException("repo_key")
        if not (dataset_id and isinstance(dataset_id, str)):
            raise InvalidParameterException("dataset_id")

        isExists = os.path.isdir(local_folder_path)
        if not isExists:
            raise InvalidDirectoryPath(local_folder_path)

        # get the resultant dataframe from fetch_linked_reports function
        df = self.fetch_linked_reports(polly_session, repo_key, dataset_id)

        if df is None:
            print("No reports to download")
            return

        urls_list = []
        # iterate on the DF and get the report_ids
        for _, row in df.iterrows():
            # print(row)
            urls_list.append(row["URL"])

        files_signed_urls_list = []

        file_id_list = self._extract_file_ids(urls_list)

        # call the API on the report_id to get list of all signed urls
        for file_id in file_id_list:
            params = {"action": "file_download"}
            url = f"{polly_session.base_url}/shared-files/{file_id}"

            response = polly_session.session.get(url, params=params)
            error_handler(response)
            response_json = response.json()

            # structure of response
            """
                {
                    "data":{
                        "type":"file",
                        "id":"15374/renamed - another.xlsx",
                        "attributes":{
                            "s3_key":"15374/renamed - another.xlsx",
                            "last_modified":"2024-04-11 04:28:35.000000",
                            "size":"8.94 KB",
                            "file_name":""
                        },
                        "links":{
                            "self":"/projects/15374/files/renamed%20-%20another.xlsx",
                            "signed_url": "<signed_url>"
                        }
                    }
                }
            """
            signed_url_val = response_json.get("data").get("links").get("signed_url")
            files_signed_urls_list.append(signed_url_val)

        try:
            # iterate over signed urls and download it in the provided local file path
            reporting_hlpr.download_from_s3_signedUrls(
                files_signed_urls_list, local_folder_path
            )
        except Exception as err:
            raise err

    def delete_linked_report(
        self, polly_session, repo_key: str, dataset_id: str, report_id: str
    ):
        if not (repo_key and isinstance(repo_key, str)):
            raise InvalidParameterException("repo_key")
        if not (dataset_id and isinstance(dataset_id, str)):
            raise InvalidParameterException("dataset_id")
        if not (report_id and isinstance(report_id, str)):
            raise InvalidParameterException("report_id")
        # getting repo_id from the repo_key entered
        response_omixatlas = polly_services_hlpr.omixatlas_summary(
            polly_session, repo_key
        )
        data = response_omixatlas.get("data")
        repo_id = data.get("repo_id")
        params = {"dataset_id": f"{dataset_id}", "report_id": f"{report_id}"}
        url = f"{polly_session.base_url}/v1/omixatlases/{repo_id}/reports"
        response = polly_session.session.delete(url, params=params)
        error_handler(response)
        print(f"Linked file with report_id = '{report_id}' deleted.")
