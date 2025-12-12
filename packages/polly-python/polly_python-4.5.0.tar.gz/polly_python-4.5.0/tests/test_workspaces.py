from polly import workspaces
import pytest
import os
from polly.errors import (
    InvalidParameterException,
    InvalidPathException,
    InvalidWorkspaceDetails,
)
import polly
import test_constants as test_const

key = "POLLY_API_KEY"
token = os.getenv(key)
response_json = test_const.WORKSPACE_RESPONSE_JSON


def test_obj_initialised():
    assert workspaces.Workspaces(token) is not None


@pytest.fixture()
def mock_workspaces_permission_check_fixture(mocker):
    mocker.patch(
        polly.helpers.__name__ + ".workspaces_permission_check",
        return_value=True,
    )
    return mocker


def test_fetch_my_workspaces(mocker):
    mocked_response = test_const.FETCH_WORKSPACES_MOCKED_RESPONSE
    obj = workspaces.Workspaces(token)
    mocker.patch(
        polly.workspaces.__name__ + ".Workspaces._fetch_workspaces_iteratively",
        return_value=mocked_response,
    )
    assert dict(obj.fetch_my_workspaces()) is not None


# def test_create_copy_incorrect_token():
#     incorrect_token = "incorrect_token"
#     with pytest.raises(HTTPError):
#         workspaces.Workspaces(incorrect_token)


def test_create_copy(mocker):
    response_post_request = test_const.WORKSPACE_CREATE_COPY_POST_REQUEST_RESPONSE
    response_sample = test_const.WORKSPACE_CREATE_COPY_GET_REQUEST_RESPONSE
    obj = workspaces.Workspaces(token)
    invalid_source_id = "12"
    valid_source_id = 12
    invalid_source_path = ["source_path"]
    valid_source_path = "source_path"
    valid_destination_id = 13
    invalid_destination_id = "13"
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.create_copy(invalid_source_id, valid_source_path, valid_destination_id)
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.create_copy(valid_source_id, invalid_source_path, valid_destination_id)
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.create_copy(valid_source_id, valid_source_path, invalid_destination_id)
    mocker.patch(
        polly.helpers.__name__ + ".get_sts_creds",
        return_value=True,
    )
    mocker.patch(
        polly.helpers.__name__ + ".get_workspace_payload",
        return_value=response_json,
    )
    response = mocker.patch.object(obj.session, "get")
    response.return_value.status_code = 200
    response.return_value.json.return_value = response_sample
    response_post = mocker.patch.object(obj.session, "post")
    response_post.return_value.status_code = 200
    response_post.return_value.json.return_value = response_post_request
    result = obj.create_copy(valid_source_id, valid_source_path, valid_destination_id)
    assert result is None


def test_upload_to_workspaces_incorrect_path():
    workspace_id = 12
    workspace_path = "workspace_path"
    local_path = "local_path"
    obj = workspaces.Workspaces(token)
    with pytest.raises(
        InvalidPathException, match=r"does not represent a file or a directory"
    ):
        obj.upload_to_workspaces(workspace_id, workspace_path, local_path)


def test_upload_to_workspaces(mocker, mock_workspaces_permission_check_fixture):
    obj = workspaces.Workspaces(token)
    invalid_workspace_id = "12"
    valid_workspace_id = 12
    invalid_workspace_path = ["workspace_path"]
    valid_workspace_path = "workspace_path"
    invalid_local_path = ["local_path"]
    valid_local_path = "local_path"
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.upload_to_workspaces(
            invalid_workspace_id, valid_workspace_path, valid_local_path
        )
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.upload_to_workspaces(
            valid_workspace_id, invalid_workspace_path, valid_local_path
        )
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.upload_to_workspaces(
            valid_workspace_id, valid_workspace_path, invalid_local_path
        )
    mocker.patch(
        "os.path.exists",
        return_value=True,
    )
    mocker = mock_workspaces_permission_check_fixture
    mocker.patch(
        polly.helpers.__name__ + ".get_sts_creds",
        return_value=True,
    )
    mocker.patch(
        polly.helpers.__name__ + ".upload_to_S3",
        return_value=True,
    )
    response = mocker.patch.object(obj.session, "get")
    response.return_value.status_code = 200
    response.return_value.json.return_value = response_json
    result = obj.upload_to_workspaces(
        valid_workspace_id, valid_workspace_path, valid_local_path
    )
    assert result is None


# def test_download_from_workspaces_incorrect_token():
#     incorrect_token = "incorrect_token"
#     with pytest.raises(HTTPError):
#         workspaces.Workspaces(incorrect_token)


def test_download_from_workspaces(mocker, mock_workspaces_permission_check_fixture):
    obj = workspaces.Workspaces(token)
    invalid_workspace_id = "12"
    valid_workspace_id = 12
    valid_workspace_path = "path"
    invalid_workspace_path = ["workspace_path"]
    valid_workspace_path = "workspace_path"
    local_path = "./"
    mocker = mock_workspaces_permission_check_fixture
    mocker.patch(
        polly.helpers.__name__ + ".get_sts_creds",
        return_value=True,
    )
    mocker.patch(
        polly.helpers.__name__ + ".download_from_S3",
        return_value=True,
    )
    response = mocker.patch.object(obj.session, "get")
    response.return_value.status_code = 200
    response.return_value.json.return_value = response_json
    result = obj.download_from_workspaces(
        valid_workspace_id, valid_workspace_path, local_path
    )
    assert result is None
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.download_from_workspaces(
            invalid_workspace_id, valid_workspace_path, local_path
        )
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.download_from_workspaces(
            valid_workspace_id, invalid_workspace_path, local_path
        )

    exclude_path_result = obj.download_from_workspaces(
        valid_workspace_id, valid_workspace_path, local_path, copy_workspace_path=False
    )
    assert exclude_path_result is None
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.download_from_workspaces(
            invalid_workspace_id,
            valid_workspace_path,
            local_path,
            copy_workspace_path=False,
        )
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.download_from_workspaces(
            valid_workspace_id,
            invalid_workspace_path,
            local_path,
            copy_workspace_path=False,
        )


def test_sync_data(mocker, mock_workspaces_permission_check_fixture):
    obj = workspaces.Workspaces(token)
    invalid_workspace_id = "12"
    valid_workspace_id = 12
    valid_workspace_path = "polly://path"
    invalid_workspace_path = ["workspace_path"]
    local_path = "folder/"
    mocker = mock_workspaces_permission_check_fixture
    mocker.patch(
        polly.helpers.__name__ + ".get_sts_creds",
        return_value=True,
    )
    mocker.patch(
        polly.helpers.__name__ + ".upload_to_S3",
        return_value=True,
    )
    mocker.patch(
        polly.helpers.__name__ + ".download_from_S3",
        return_value=True,
    )
    mocker.patch(
        "os.path.isdir",
        return_value=True,
    )
    response = mocker.patch.object(obj.session, "get")
    response.return_value.status_code = 200
    response.return_value.json.return_value = response_json
    result = obj.sync_data(valid_workspace_id, valid_workspace_path, local_path)
    assert result is None
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.sync_data(invalid_workspace_id, valid_workspace_path, local_path)
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.sync_data(valid_workspace_id, invalid_workspace_path, local_path)
    with pytest.raises(
        InvalidWorkspaceDetails,
        match=r".* path should start with 'polly://'. .*",
    ):
        obj.sync_data(valid_workspace_id, local_path, local_path)
