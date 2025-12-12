import os
from polly.auth import Polly
from polly import pipelines
from test_constants import (
    MOCKED_LIST_RESPONSE,
    MOCKED_PIPELINE_GET_RESPONSE,
    MOCKED_RESPONSE_DICT,
)

key = "POLLY_API_KEY"
token = os.getenv(key)

test_key = "TEST_POLLY_API_KEY"
testpolly_token = os.getenv(test_key)

dev_key = "DEV_POLLY_API_KEY"
devpolly_token = os.getenv(dev_key)

pipeline_id = "19266b29-c1c3-4b7c-86aa-e065f555944b"  # sample pipeline_id
batch_id = "7e9d309c-76b1-4312-9013-5eff50a09034"  # sample batch_id
run_id = "f0d5348d-0196-4d9e-bd43-aab87202c882"  # sample run_id


def test_obj_initialised():
    Polly.auth(devpolly_token, env="devpolly")
    assert pipelines.Pipelines() is not None
    assert pipelines.Pipelines(token) is not None
    assert Polly.get_session(token) is not None


def test_list_pipelines(mocker):
    Polly.auth(devpolly_token, env="devpolly")
    obj = pipelines.Pipelines()
    response = mocker.patch.object(obj.session, "get")
    response.return_value.status_code = 200
    response.return_value.json.return_value = MOCKED_LIST_RESPONSE
    assert type(obj.list_pipelines()) is list


def test_get_pipeline(mocker):
    Polly.auth(devpolly_token, env="devpolly")
    obj = pipelines.Pipelines()
    response = mocker.patch.object(obj.session, "get")
    response.return_value.status_code = 200
    response.return_value.json.return_value = MOCKED_PIPELINE_GET_RESPONSE
    assert type(obj.get_pipeline(pipeline_id=pipeline_id)) is dict


def test_create_batch(mocker):
    Polly.auth(devpolly_token, env="devpolly")
    obj = pipelines.Pipelines()
    response = mocker.patch.object(obj.session, "post")
    response.return_value.status_code = 200
    response.return_value.json.return_value = MOCKED_RESPONSE_DICT
    assert type(obj.create_batch(pipeline_id=pipeline_id)) is dict


def test_submit_run(mocker):
    Polly.auth(devpolly_token, env="devpolly")
    obj = pipelines.Pipelines()
    parameters = {"a": 12, "b": 13}
    config = {"infra": {"cpu": 1, "memory": 2, "storage": 120}}
    response = mocker.patch.object(obj.session, "post")
    response.return_value.status_code = 200
    response.return_value.json.return_value = MOCKED_LIST_RESPONSE
    assert (
        type(obj.submit_run(batch_id=batch_id, parameters=parameters, config=config))
        is dict
    )


def test_list_batches(mocker):
    Polly.auth(devpolly_token, env="devpolly")
    obj = pipelines.Pipelines()
    response = mocker.patch.object(obj.session, "get")
    response.return_value.status_code = 200
    response.return_value.json.return_value = MOCKED_LIST_RESPONSE
    assert type(obj.list_batches()) is list


def test_get_batch(mocker):
    Polly.auth(devpolly_token, env="devpolly")
    obj = pipelines.Pipelines()
    response = mocker.patch.object(obj.session, "get")
    response.return_value.status_code = 200
    response.return_value.json.return_value = MOCKED_RESPONSE_DICT
    assert type(obj.get_batch(batch_id=batch_id)) is dict


def test_list_runs(mocker):
    Polly.auth(devpolly_token, env="devpolly")
    obj = pipelines.Pipelines()
    response = mocker.patch.object(obj.session, "get")
    response.return_value.status_code = 200
    response.return_value.json.return_value = MOCKED_LIST_RESPONSE
    assert type(obj.list_runs(batch_id=batch_id)) is list


def test_get_run(mocker):
    Polly.auth(devpolly_token, env="devpolly")
    obj = pipelines.Pipelines()
    response = mocker.patch.object(obj.session, "get")
    response.return_value.status_code = 200
    response.return_value.json.return_value = MOCKED_RESPONSE_DICT
    assert type(obj.get_run(run_id=run_id)) is dict


def test_cancel_run(mocker):
    Polly.auth(devpolly_token, env="devpolly")
    obj = pipelines.Pipelines()
    response = mocker.patch.object(obj.session, "post")
    response.return_value.status_code = 200
    response.return_value.json.return_value = MOCKED_RESPONSE_DICT
    assert type(obj.cancel_run(run_id=run_id)) is dict
