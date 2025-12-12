# from polly import polly_kg
from polly.polly_kg import PollyKG
import pytest

import os
from polly.errors import (
    InvalidParameterException,
    QueryFailedException,
)

key = "POLLY_API_KEY"
token = os.getenv(key)

test_key = "TEST_POLLY_API_KEY"
testpolly_token = os.getenv(test_key)


def test_obj_initialised_with_kg_and_version(mocker):
    mocker.patch(
        "polly.polly_kg._validate_kg_version_exists", return_value=("kg-xyz", "v9")
    )
    obj = PollyKG(token, kg_id="kg-xyz", version_id="v9")
    assert obj.kg_id == "kg-xyz"
    assert obj.version_id == "v9"


def test_run_query_success(mocker):
    mocker.patch(
        "polly.polly_kg._validate_kg_version_exists", return_value=("kg-xyz", "v9")
    )
    obj = PollyKG(token=token, kg_id="kg-xyz", version_id="v9")
    mock_post = mocker.patch.object(obj.session, "post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "data": {"attributes": {"query_id": "test-query-id"}}
    }

    mock_status = mocker.patch.object(obj.session, "get")
    mock_status.return_value.status_code = 200
    mock_status.return_value.json.return_value = {
        "data": {
            "attributes": {
                "status": "COMPLETED",
                "metadata": {"results": {"url": "https://s3-bucket/test.json"}},
            }
        }
    }

    mock_requests_get = mocker.patch("polly.polly_kg.requests.get")
    mock_requests_get.return_value.json.return_value = {"result": "success"}

    result = obj.run_query("MATCH (n) RETURN count(n);")
    assert result["result"] == "success"


def test_run_query_invalid_input(mocker):
    mocker.patch("polly.polly_kg._get_default_kg", return_value=("kg1", "v1"))
    obj = PollyKG(token=token)
    with pytest.raises(InvalidParameterException):
        obj.run_query("")


def test_run_query_failed_execution(mocker):
    mocker.patch("polly.polly_kg._get_default_kg", return_value=("kg1", "v1"))

    obj = PollyKG(token=token)

    mocker.patch.object(
        obj.session,
        "post",
        return_value=mocker.Mock(
            status_code=200,
            json=lambda: {"data": {"attributes": {"query_id": "q1"}}},
        ),
    )

    mocker.patch.object(
        obj.session,
        "get",
        return_value=mocker.Mock(
            status_code=200,
            json=lambda: {
                "data": {
                    "attributes": {
                        "status": "FAILED",
                        "metadata": {"error": "Query timed out"},
                    }
                }
            },
        ),
    )

    with pytest.raises(QueryFailedException, match="Query timed out"):
        obj.run_query("MATCH (n) RETURN count(n);")


def test_get_query_status_completed(mocker, capsys):
    mocker.patch("polly.polly_kg._get_default_kg", return_value=("kg1", "v1"))

    obj = PollyKG(token=token)

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"attributes": {"status": "COMPLETED"}}}

    mocker.patch.object(obj.session, "get", return_value=mock_response)
    status = obj.get_query_status("test-id")
    assert status["status"] == "COMPLETED"


def test_get_query_status_invalid_input(mocker):
    mocker.patch("polly.polly_kg._get_default_kg", return_value=("kg1", "v1"))

    mocker.patch(
        "polly.polly_kg._validate_kg_version_exists", return_value=("kg1", "v1")
    )
    obj = PollyKG(token=token)
    with pytest.raises(InvalidParameterException):
        obj.get_query_status("")


def test_download_query_results_success(mocker, tmp_path):
    mocker.patch("polly.polly_kg._get_default_kg", return_value=("kg1", "v1"))
    obj = PollyKG(token=token)
    query_id = "query-download-id"

    mock_status_response = {
        "data": {
            "attributes": {
                "status": "COMPLETED",
                "metadata": {"results": {"url": "https://mock-bucket.com/output.json"}},
            }
        }
    }

    mocker.patch.object(
        obj.session,
        "get",
        return_value=mocker.Mock(
            status_code=200,
            json=lambda: mock_status_response,
        ),
    )

    def create_mock_response():
        mock_resp = mocker.MagicMock()
        mock_resp.raise_for_status.return_value = None

        def mock_iter_content(chunk_size=None):
            return iter([b'{"data": "mocked"}'])

        mock_resp.iter_content = mock_iter_content
        mock_resp.__enter__.return_value = mock_resp
        mock_resp.__exit__.return_value = None
        return mock_resp

    mock_response = create_mock_response()
    mocker.patch("polly.polly_kg.requests.get", return_value=mock_response)
    mocker.patch("polly.polly_kg.os.makedirs")
    mock_file = mocker.mock_open()
    mocker.patch("builtins.open", mock_file)
    result = obj.download_query_results(query_id)
    assert result == "./results/query-download-id.json"
    mock_file.assert_called_once()
    file_handle = mock_file.return_value.__enter__.return_value
    file_handle.write.assert_called_with(b'{"data": "mocked"}')


def test_download_query_results_invalid_input(mocker):
    mocker.patch("polly.polly_kg._get_default_kg", return_value=("kg1", "v1"))
    obj = PollyKG(token=token)
    with pytest.raises(InvalidParameterException):
        obj.download_query_results("")


def test_download_query_results_failed_status(mocker):
    mocker.patch("polly.polly_kg._get_default_kg", return_value=("kg1", "v1"))

    obj = PollyKG(token=token)
    query_id = "failed-query"

    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json = lambda: {
        "data": {
            "attributes": {
                "status": "FAILED",
                "metadata": {"error": "Execution error"},
            }
        }
    }

    mocker.patch.object(obj.session, "get", return_value=mock_response)

    with pytest.raises(QueryFailedException, match="Execution error"):
        obj.download_query_results(query_id)


def test_get_summary_success(mocker):
    mocker.patch("polly.polly_kg._get_default_kg", return_value=("kg1", "v1"))

    obj = PollyKG(token=token)
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"summary": {"nodes": 10}}

    mocker.patch.object(obj.session, "get", return_value=mock_response)
    result = obj.get_summary()

    assert result["summary"]["nodes"] == 10


def test_get_schema_success(mocker):
    mocker.patch("polly.polly_kg._get_default_kg", return_value=("kg1", "v1"))

    obj = PollyKG(token=token)
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"schema": {"labels": ["Disease", "Drug"]}}

    mocker.patch.object(obj.session, "get", return_value=mock_response)
    result = obj.get_schema()

    assert "Disease" in result["schema"]["labels"]


def test_get_all_kgs_success(mocker):
    mocker.patch("polly.polly_kg._get_default_kg", return_value=("kg1", "v1"))

    obj = PollyKG(token=token)
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": [
            {
                "kg_id": "14_base_kg_v3",
                "kg_name": "base kg v3",
                "kg_description": "Base KG v",
                "version_id": 1,
                "created_at": 1756115807076,
                "published": True,
            },
            {
                "kg_id": "15_test_kg",
                "kg_name": "test kg",
                "kg_description": "Test KG",
                "version_id": 2,
                "created_at": 1756115900000,
                "published": False,
            },
        ]
    }

    mocker.patch.object(obj.session, "get", return_value=mock_response)
    result = obj.get_all_kgs()

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["kg_id"] == "14_base_kg_v3"
    assert result[0]["kg_name"] == "base kg v3"
    assert result[0]["version_id"] == 1
    assert result[0]["published"] is True
    assert result[1]["kg_id"] == "15_test_kg"
    assert result[1]["published"] is False


def test_get_all_kgs_with_parameters(mocker):
    mocker.patch("polly.polly_kg._get_default_kg", return_value=("kg1", "v1"))

    obj = PollyKG(token=token)
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": [
            {
                "kg_id": "14_base_kg_v3",
                "kg_name": "base kg v3",
                "kg_description": "Base KG v",
                "version_id": 1,
                "created_at": 1756115807076,
                "published": True,
                "instances": [
                    {
                        "instance_id": "inst_123",
                        "instance_type": "t3.medium",
                        "is_terminated": False,
                        "default_instance": True,
                        "org_id": 1,
                        "created_at": 1756115807076,
                    }
                ],
            },
            {
                "kg_id": "15_test_kg",
                "kg_name": "test kg",
                "kg_description": "Test KG",
                "version_id": 2,
                "created_at": 1756115900000,
                "published": False,
                "instances": [
                    {
                        "instance_id": "inst_456",
                        "instance_type": "t3.large",
                        "is_terminated": True,
                        "default_instance": False,
                        "org_id": 1,
                        "created_at": 1756115900000,
                    }
                ],
            },
        ]
    }

    mock_get = mocker.patch.object(obj.session, "get", return_value=mock_response)
    result = obj.get_all_kgs(
        include_unpublished=True, include_instances=True, include_terminated=True
    )

    # Verify the API was called with correct parameters
    mock_get.assert_called_once()
    call_kwargs = mock_get.call_args.kwargs
    assert "params" in call_kwargs
    assert call_kwargs["params"] == {
        "include_unpublished": "true",
        "include_instances": "true",
        "include_terminated": "true",
    }

    # Verify the response structure
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["kg_id"] == "14_base_kg_v3"
    assert result[0]["published"] is True
    assert "instances" in result[0]
    assert len(result[0]["instances"]) == 1
    assert result[0]["instances"][0]["instance_id"] == "inst_123"
    assert result[0]["instances"][0]["instance_type"] == "t3.medium"
    assert result[0]["instances"][0]["is_terminated"] is False

    assert result[1]["kg_id"] == "15_test_kg"
    assert result[1]["published"] is False
    assert "instances" in result[1]
    assert len(result[1]["instances"]) == 1
    assert result[1]["instances"][0]["instance_id"] == "inst_456"
    assert result[1]["instances"][0]["is_terminated"] is True
