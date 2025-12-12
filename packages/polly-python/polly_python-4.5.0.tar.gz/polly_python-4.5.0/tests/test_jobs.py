import pandas as pd
from pytest import fixture
from unittest.mock import MagicMock
import os
import json
import random
import pytest
import requests
import polly
from polly.auth import Polly
from polly import jobs
from polly.errors import (
    InvalidJobFunctionParameterException,
    InvalidParameterException,
    error_handler,
)
import test_constants as test_const

key = "POLLY_API_KEY"
token = os.getenv(key)

test_key = "TEST_POLLY_API_KEY"
testpolly_token = os.getenv(test_key)

dev_key = "DEV_POLLY_API_KEY"
devpolly_token = os.getenv(dev_key)


def test_obj_initialised():
    Polly.auth(token)
    assert jobs.jobs() is not None
    assert jobs.jobs(token) is not None
    assert Polly.get_session(token) is not None


@fixture
def get_job_submission_json_file(mocker):
    base_polly_py_test_url = test_const.POLLY_PY_TEST_FILES_URL
    parent_dir = os.getcwd()
    test_dir = "tests"
    test_path = os.path.join(parent_dir, test_dir)
    if not os.path.isdir(test_path):
        os.makedirs(test_path)

    test_jobs_json_file_remote_path = f"{base_polly_py_test_url}/test_job.json"
    test_jobs_json = requests.get(test_jobs_json_file_remote_path)
    error_handler(test_jobs_json)
    test_job_json_filename = "test_job.json"
    test_job_json_file_path_local = os.path.join(test_path, test_job_json_filename)
    with open(test_job_json_file_path_local, "w") as file_1:
        file_1_content = test_jobs_json.text
        file_1.write(file_1_content)
    return test_job_json_file_path_local


@fixture
def get_jobData_with_secret_env_keys(mocker, get_job_submission_json_file):
    workspace_id = 12345
    with open(get_job_submission_json_file, "r") as jobfile:
        jobData = json.load(jobfile)
    secret_env = {
        "POLLY_REFRESH_TOKEN": "refresh_token",
        "POLLY_WORKSPACE_ID": workspace_id,
        "POLLY_USER": "test_user@test.io",
        "POLLY_SUB": "dummysub",
        "POLLY_EXP": 1234567,
        "POLLY_AUD": "dummyaud",
    }
    jobData["secret_env"] = secret_env
    return jobData


def test_submit_job(
    mocker, get_job_submission_json_file, get_jobData_with_secret_env_keys
):
    # valid_input_json_file = "/Users/shilpanair/workspace/dev_test_files/jobs_work/test_job.json"
    valid_input_json_file = get_job_submission_json_file
    valid_workspace_id = 12345
    # internally called fuction _submit_job_to_polly returns a response object - creating a mock of the response object
    mocker.patch(
        polly.jobs.__name__ + ".jobs._add_secret_env_keys_to_jobData",
        return_value=get_jobData_with_secret_env_keys,
    )
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "data": {"project_id": 12345, "job_id": "19cbda998c4c492faeef0b14cbc55274"}
    }
    # patching the mock response object when _submit_job_to_polly is called
    mocker.patch(
        polly.jobs.__name__ + ".jobs._submit_job_to_polly",
        return_value=mock_response,
    )
    # calling the function under test
    Polly.auth(testpolly_token, env="testpolly")
    jobs_obj = jobs.jobs()
    output = jobs_obj.submit_job(valid_workspace_id, valid_input_json_file)
    assert type(output) is pd.DataFrame
    assert output.iloc[0]["Workspace ID"] == 12345

    if os.path.exists(valid_input_json_file):
        os.remove(valid_input_json_file)

    # test for expected parameter exceptions
    invalid_workspace_id_type = {"worspace_id": "12345"}
    invalid_file_path_type = ["/dummy/path/dummy_input.json"]
    with pytest.raises(
        InvalidParameterException,
        match=r"Empty or Invalid Parameters = project id/workspace id",
    ):
        jobs_obj.submit_job(invalid_workspace_id_type, valid_input_json_file)

    with pytest.raises(
        TypeError,
        match=r"path should be string, bytes, os.PathLike or integer, not list",
    ):
        jobs_obj.submit_job(valid_workspace_id, invalid_file_path_type)


# @pytest.mark.skip(reason="no way of currently testing this")
def test_submit_job_invalid_json(
    mocker, get_job_submission_json_file, get_jobData_with_secret_env_keys, capsys
):
    # valid_input_json_file = "/Users/shilpanair/workspace/dev_test_files/jobs_work/test_job.json"
    valid_input_json_file = get_job_submission_json_file
    valid_workspace_id = 12345
    # internally called fuction _submit_job_to_polly returns a response object - creating a mock of the response object
    # patching the mock response object when _submit_job_to_polly is called

    mocker.patch(
        polly.jobs.__name__ + ".jobs._add_secret_env_keys_to_jobData",
        return_value=get_jobData_with_secret_env_keys,
    )

    mocker.patch(
        polly.jobs.__name__ + ".jobs._submit_job_to_polly",
        side_effect=Exception(
            "Either cpu and memory or machineType should be specified', "
            + "'Server could not understand the request due to invalid syntax"
        ),
    )
    # calling the function under test
    Polly.auth(testpolly_token, env="testpolly")
    jobs_obj = jobs.jobs()
    with pytest.raises(
        Exception,
        match=r"Either cpu and memory or machineType should be specified*",
    ):
        jobs_obj.submit_job(valid_workspace_id, valid_input_json_file)
        captured = capsys.readouterr()
        assert "Not able to submit job" in captured.out


# @pytest.mark.skip(reason="no way of currently testing this")
def test_submit_job_invalid_workspace_id(
    mocker, get_job_submission_json_file, get_jobData_with_secret_env_keys, capsys
):
    Polly.auth(testpolly_token, env="testpolly")
    jobs_obj = jobs.jobs()
    valid_input_json_file = get_job_submission_json_file
    invalid_workspace_id_1 = "abcdwef"
    invalid_workspace_id_2 = "00000000"

    mocker.patch(
        polly.jobs.__name__ + ".jobs._add_secret_env_keys_to_jobData",
        return_value=get_jobData_with_secret_env_keys,
    )

    # case 1: where the project_id/workspace_id is not of valid type (should be numeric)
    Polly.auth(testpolly_token, env="testpolly")
    jobs_obj = jobs.jobs()

    mocker.patch(
        polly.jobs.__name__ + ".jobs._submit_job_to_polly",
        side_effect=Exception("Bad Request', 'Project ID - abcdwef should be numeric"),
    )
    # calling the function under test
    with pytest.raises(
        Exception,
        match=r"Project ID - abcdwef should be numeric*",
    ):
        jobs_obj.submit_job(invalid_workspace_id_1, valid_input_json_file)
        captured = capsys.readouterr()
        assert "Not able to submit job" in captured.out
    # case 2: where the project_id/workspace_id is not present
    mocker.patch(
        polly.jobs.__name__ + ".jobs._submit_job_to_polly",
        side_effect=Exception(
            "Project Ownership', 'Error occurred in getting the Project ownership"
        ),
    )
    with pytest.raises(
        Exception,
        match=r"Error occurred in getting the Project ownership*",
    ):
        jobs_obj.submit_job(invalid_workspace_id_2, valid_input_json_file)
        captured = capsys.readouterr()
        assert "Not able to submit job" in captured.out


# test successfullcancellation of job
def test_cancel_job(mocker, get_jobData_with_secret_env_keys, capsys):
    valid_workspace_id = 12345
    valid_job_id = f"{random.randrange(16**32):032x}"
    Polly.auth(testpolly_token, env="testpolly")
    jobs_obj = jobs.jobs()
    # internally called fuction _submit_job_to_polly returns a response object - creating a mock of the response object
    mocker.patch(
        polly.jobs.__name__ + ".jobs._add_secret_env_keys_to_jobData",
        return_value=get_jobData_with_secret_env_keys,
    )
    mocker.patch(
        polly.jobs.__name__ + ".jobs._parameter_check_for_jobs",
        return_value=None,
    )
    response = mocker.patch.object(jobs_obj.session, "delete")
    response.return_value.status_code = 204

    jobs_obj.cancel_job(valid_workspace_id, valid_job_id)
    captured = capsys.readouterr()

    expected_output = "Cancelled job ID " + valid_job_id + " successfully!"
    assert expected_output in captured.out


# test invalid workspace in  cancellation of job
def test_cancel_job_invalid_workspace(mocker, get_jobData_with_secret_env_keys, capsys):
    Polly.auth(testpolly_token, env="testpolly")
    jobs_obj = jobs.jobs()
    invalid_job_id = "1234"
    valid_workspace_id = 12345
    mocker.patch(
        polly.jobs.__name__ + ".jobs._check_job_id",
        side_effect=InvalidJobFunctionParameterException(
            "The specified  job_id could not be found. Inspect and try again."
        ),
    )
    mocker.patch(
        polly.jobs.__name__ + ".jobs._add_secret_env_keys_to_jobData",
        return_value=get_jobData_with_secret_env_keys,
    )
    with pytest.raises(
        InvalidJobFunctionParameterException,
        match=r"The specified The specified  job_id could not be found."
        + " Inspect and try again. could not be found. Inspect and try again.",
    ):
        jobs_obj.cancel_job(valid_workspace_id, invalid_job_id)


# test cancel of an already cancelled job
def test_cancel_cancelled_job(mocker, get_jobData_with_secret_env_keys, capsys):
    Polly.auth(testpolly_token, env="testpolly")
    jobs_obj = jobs.jobs()
    invalid_job_id = "1234"
    valid_workspace_id = 12345
    mocker.patch(
        polly.jobs.__name__ + ".jobs._add_secret_env_keys_to_jobData",
        return_value=get_jobData_with_secret_env_keys,
    )
    mocker.patch(
        polly.jobs.__name__ + ".jobs._parameter_check_for_jobs",
        return_value=None,
    )

    response = mocker.patch.object(jobs_obj.session, "delete")
    response.return_value.status_code = 400
    response.return_value.text = (
        '{"errors": [{"status": "400", "code": "bad_req",'
        + '"title": "Bad Request", "detail": "Cannot cancel a job in CANCELLED state"}]}'
    )

    jobs_obj.cancel_job(valid_workspace_id, invalid_job_id)
    captured = capsys.readouterr()
    assert (
        "Failed to cancel the job.: Cannot cancel a job in CANCELLED state"
        in captured.out
    )


def test_job_status(mocker, get_jobData_with_secret_env_keys):
    valid_workspace_id = 12345
    valid_job_id = f"{random.randrange(16**32):032x}"
    Polly.auth(testpolly_token, env="testpolly")
    jobs_obj = jobs.jobs()
    # internally called fuction _submit_job_to_polly returns a response object - creating a mock of the response object
    mocker.patch(
        polly.jobs.__name__ + ".jobs._add_secret_env_keys_to_jobData",
        return_value=get_jobData_with_secret_env_keys,
    )
    mocker.patch(
        polly.jobs.__name__ + ".jobs._parameter_check_for_jobs",
        return_value=None,
    )
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": [
            {
                "type": "jobs",
                "id": valid_job_id,
                "attributes": {
                    "job_name": "This is a job for testing bust mode",
                    "started_ts": 1666346315947,
                    "creator_id": 1663209871,
                    "log_ids": ["random_log_id"],
                    "project_id": valid_workspace_id,
                    "config_json": {
                        "cpu": "1",
                        "memory": "1Gi",
                        "image": "ubuntu",
                        "tag": "latest",
                        "machineType": "null",
                        "cloud_provider": "aws",
                        "timelimit": 12,
                        "command": [
                            "/bin/bash",
                            "-c",
                            "TERM=xterm free -h; echo '\nnumber of vCPU';nproc;sleep 30",
                        ],
                    },
                    "job_id": "valid_job_id",
                    "ended_ts": 1666346361960,
                    "session_info": [
                        {
                            "log_id": "14832-20c139ae6925438ba670fdac6175b4c4-776133615_compute-test_main",
                            "ended_ts": 1666346361960,
                            "state": "Success",
                            "started_ts": 1666346315947,
                        }
                    ],
                    "created_ts": 1666346311500,
                    "state": "Success",
                },
            }
        ]
    }
    # patching the mock response object when _submit_job_to_polly is called
    mocker.patch(
        polly.jobs.__name__ + ".jobs._get_data_for_job_id",
        return_value=mock_response,
    )
    Polly.auth(testpolly_token, env="testpolly")
    jobs_obj = jobs.jobs()
    output = jobs_obj.job_status(valid_workspace_id, valid_job_id)
    assert type(output) is pd.DataFrame
    assert output.iloc[0]["Job State"] == "Success"


def test_job_status_invalid_job_id(mocker, get_jobData_with_secret_env_keys):
    valid_workspace_id = 12345
    Polly.auth(testpolly_token, env="testpolly")
    jobs_obj = jobs.jobs()
    # internally called fuction _submit_job_to_polly returns a response object - creating a mock of the response object
    mocker.patch(
        polly.jobs.__name__ + ".jobs._add_secret_env_keys_to_jobData",
        return_value=get_jobData_with_secret_env_keys,
    )
    invalid_job_id = "1234"
    valid_workspace_id = 12345
    mocker.patch(
        polly.jobs.__name__ + ".jobs._check_job_id",
        side_effect=InvalidJobFunctionParameterException(
            "The specified  job_id could not be found. Inspect and try again."
        ),
    )
    with pytest.raises(
        InvalidJobFunctionParameterException,
        match=r"The specified The specified  job_id could not be found."
        + " Inspect and try again. could not be found. Inspect and try again.",
    ):
        jobs_obj.job_status(valid_workspace_id, invalid_job_id)
