import json
import os
import urllib
from polly import helpers
from cloudpathlib import S3Client
from polly.errors import error_handler
from urllib.parse import quote
from polly.errors import paramException, AccessDeniedError
from tqdm import tqdm
import requests


def verify_workspace_path(cloud_path: str, credentials: dict) -> tuple:
    """
    Function to verify if the workspace path is valid.
    """
    access_key_id = credentials["AccessKeyId"]
    secret_access_key = credentials["SecretAccessKey"]
    session_token = credentials["SessionToken"]
    client = S3Client(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        aws_session_token=session_token,
    )
    source_path = client.CloudPath(cloud_path)
    if source_path.exists():
        return source_path, True
    else:
        return source_path, False


def check_is_file(
    polly_session, sts_url: str, workspace_id: int, workspace_path: str
) -> bool:
    """
    Function to check if the workspace_path is a valid file path existing in the workspace.
    """
    creds = polly_session.session.get(sts_url)
    error_handler(creds)
    credentials = helpers.get_sts_creds(creds.json())
    if polly_session.session.env == "polly":
        env_string = "prod"
    elif polly_session.session.env == "testpolly":
        env_string = "test"
    else:
        env_string = "devenv"
    bucket = f"mithoo-{env_string}-project-data-v1"
    s3_path = f"{bucket}/{workspace_id}/"
    s3_path = f"s3://{helpers.make_path(s3_path, workspace_path)}"
    tuple_output = verify_workspace_path(s3_path, credentials)
    source_path = tuple_output[0]
    status = tuple_output[1]
    if status is True:
        isFile = source_path.is_file()
        return isFile
    return status


def verify_workspace_details(
    polly_session, workspace_id, workspace_path, sts_url
) -> None:
    """
    Function to check and verify workspace permissions and workspace path.
    """
    access_workspace = helpers.workspaces_permission_check(polly_session, workspace_id)
    if not access_workspace:
        raise AccessDeniedError(
            detail=f"Access denied to workspace-id - {workspace_id}"
        )
    is_file = check_is_file(polly_session, sts_url, workspace_id, workspace_path)
    if not is_file:
        raise paramException(
            title="Param Error",
            detail="The given workspace path does not represent a file. Please try again.",
        )


def get_report_id(polly_session, workspace_id: int, workspace_path: str) -> str:
    """
    Function to return report-id of the given workspace path.
    """
    s3_key = helpers.make_path(workspace_id, workspace_path)
    workspace_endpoint_url = (
        f"https://apis.{polly_session.session.env}.elucidata.io/mithoo/_search"
    )
    payload = {
        "from": 0,
        "size": 20,
        "query": {
            "bool": {
                "should": [
                    {
                        "bool": {
                            "must": [
                                {"term": {"_index": {"value": "{document_index}"}}},
                                {
                                    "term": {
                                        "workspace_id": {"value": f"{workspace_id}"}
                                    }
                                },
                                {"term": {"s3_key": {"value": f"{s3_key}"}}},
                            ]
                        }
                    },
                    {
                        "bool": {
                            "must": [
                                {"term": {"_index": {"value": "{workspace_index}"}}},
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
    response = polly_session.session.post(
        workspace_endpoint_url, data=json.dumps(payload)
    )
    error_handler(response)
    response_data = response.json()
    hits = response_data.get("hits", {}).get("hits")
    if not (hits and isinstance(hits, list)):
        raise paramException(
            title="Param Error",
            detail="Incorrect workspace path / workspace_id provided. Please try again.",
        )
    # getting the first and only element of the list that contains data
    data = hits[0]
    report_id = data.get("_source", {}).get("report_id")
    return report_id


def make_private_link(
    workspace_id: int, workspace_path: str, constant_url: str, report_id: str
) -> str:
    """
    Function to construct and return a private link for a file in workspace.
    """
    # encoding the workspace_path for any special character that might pe present in the file_name,
    # example: 18891/report@name.html
    parsed_path = urllib.parse.quote(workspace_path)
    file_element = {"path": f"/projects/{workspace_id}/files/{parsed_path}"}
    if report_id:
        return f"{constant_url}/restricted/file?id={workspace_id}&{urllib.parse.urlencode(file_element)}&report_id={report_id}"
    else:
        return f"{constant_url}/restricted/file?id={workspace_id}&{urllib.parse.urlencode(file_element)}"


def change_file_access(
    polly_session,
    access_key: str,
    workspace_id: int,
    workspace_path: str,
    access_url: str,
    report_id: str,
) -> str:
    """
    Function to change the file access as per the access_key and returns the final access url
    """
    final_url = ""
    # encoding workspace path in case of special characters
    parsed_workspace_path = urllib.parse.quote(workspace_path)
    if access_key == "private":
        params = {"action": "share", "access_type": "private"}
        url = f"{polly_session.base_url}/projects/{workspace_id}/files/{parsed_workspace_path}"
        # API call to change the file access to private
        response = polly_session.session.get(url, params=params)
        error_handler(response)
        final_url = make_private_link(
            workspace_id, workspace_path, access_url, report_id
        )
    else:
        params = {"action": "share", "access_type": "global"}
        url = f"{polly_session.base_url}/projects/{workspace_id}/files/{parsed_workspace_path}"
        # API call to change the file access to public
        response = polly_session.session.get(url, params=params)
        error_handler(response)
        shared_id = response.json().get("data").get("shared_id")
        final_url = f"{access_url}/shared/file/?id={shared_id}"
    return final_url


def get_shared_id(polly_session, workspace_id, workspace_path):
    """
    Returns the shared_id of the file in workspace in case of global access to file, None in case of private access
    """
    # encoding the workspace_path for any special character that might pe present in the file_name,
    # example: 18891/report@name.html
    parsed_path = quote(workspace_path)
    url = f"https://apis.{polly_session.session.env}.elucidata.io/mithoo/projects/{workspace_id}/files/{parsed_path}"
    params = {"action": "file_download"}
    response = polly_session.session.get(url, params=params)
    error_handler(response)
    shared_id = response.json().get("data").get("shared_id")
    return shared_id


def return_workspace_file_url(
    shared_id,
    access_url: str,
    workspace_id: str,
    workspace_path: str,
    report_id: str,
) -> str:
    if shared_id is None:
        # return private url
        file_url = make_private_link(
            workspace_id, workspace_path, access_url, report_id
        )
    else:
        # return public url
        file_url = f"{access_url}/shared/file/?id={shared_id}"
    return file_url


def split_workspace_path(absolute_path: str) -> tuple:
    """
    Function to separate workspace_id and workspace_path from s3 path
    """
    contents = absolute_path.split("/")
    workspace_id = contents[0]
    workspace_path = contents[1]
    for item in range(2, len(contents)):
        workspace_path = helpers.make_path(workspace_path, contents[item])
    return workspace_id, workspace_path


def download_from_s3_signedUrls(urls: str, local_folder: str):
    """
    Downloads files from a list of AWS signed URLs to a local folder.

    Args:
        urls: A list of strings containing the AWS signed URLs.
        local_folder: The path to the local folder where files will be downloaded.
    """
    # Create directory if it doesn't exist
    os.makedirs(local_folder, exist_ok=True)

    for url in urls:
        parsed_url = urllib.parse.urlparse(url)
        path = parsed_url.path
        filename = os.path.basename(path)
        # print(filename)
        print(f"Starting report download {filename}")
        local_path = os.path.join(local_folder, filename)

        try:
            response = requests.get(url, stream=True)
            error_handler(response)

            # tqdm implement
            with open(local_path, "wb") as f:
                chunk_size = 4096
                total_size = int(response.headers.get("Content-Length", 0))

                # Create a progress bar with total size (if available)
                pbar = tqdm(
                    total=total_size, unit="B", unit_scale=True, unit_divisor=4096
                )

                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:  # Filter out keep-alive new chunks
                        f.write(chunk)
                        pbar.update(
                            len(chunk)
                        )  # Update progress bar with downloaded chunk size

                pbar.close()  # Close the progress bar after download
                print()

        except requests.exceptions.RequestException as e:
            print(f"Error downloading {filename} from s3: {e}")
