import pytest
import os
import gzip
import json
from polly_services.dataset import sanitize_user_defined_id
from polly_services.dataset import is_supported_format, UnsupportedFormat
from polly_services.dataset import extract_extension_from_s3_uri
from polly_services.dataset import infer_file_type
from polly_services.dataset import S3ClientManager, S3SessionDetails
from polly_services.dataset import extract_file_extension
from polly_services.dataset import VersionBase, Dataset, DatasetVersion
from polly_services.dataset import SupplementaryFile

from polly.session import PollySession

from unittest.mock import patch, MagicMock
from cmapPy.pandasGEXpress.GCToo import GCToo


@pytest.fixture(scope="module", autouse=True)
def setup_polly_auth():
    from polly.auth import Polly

    Polly.auth("DUMMY_TOKEN")


def test_sanitize_user_defined_id_valid_string():
    assert (
        sanitize_user_defined_id("valid_string_123") == "valid_string_123"
    ), "Should not change valid string"


def test_sanitize_user_defined_id_special_characters():
    assert (
        sanitize_user_defined_id("user!@#id$%^&*()") == "user___id_______"
    ), "Should replace special characters with underscores"


def test_sanitize_user_defined_id_empty_string():
    with pytest.raises(ValueError, match="Empty string cannot be sanitized"):
        sanitize_user_defined_id("")


@pytest.fixture
def mock_s3_client_manager(monkeypatch):
    mock_manager = MagicMock()
    monkeypatch.setattr("polly.data_management.S3ClientManager", mock_manager)
    return mock_manager


@pytest.fixture
def s3_credentials():
    return {
        "access_key": "fake_access_key",
        "secret_key": "fake_secret_key",
        "token": "fake_token",
        "expiry_time": "2023-01-01T00:00:00Z",
    }


@patch("polly.data_management.S3ClientManager._generate_temp_s3_tokens")
@patch("boto3.Session.client")
def test_get_client_returns_s3_client(
    mock_boto3_client, mock_generate_temp_s3_tokens, s3_credentials
):
    mock_generate_temp_s3_tokens.return_value = (
        s3_credentials,
        "fake_bucket",
        "fake_prefix",
        "read",
    )
    s3_client_manager = S3ClientManager(omixatlas_id="test_omixatlas_id")
    client = s3_client_manager.get_client()

    assert mock_boto3_client.called, "boto3 client should be created"
    assert isinstance(client, MagicMock), "get_client should return a boto3 client"


@patch("polly.data_management.S3ClientManager._generate_temp_s3_tokens")
def test_get_upload_path_returns_bucket_and_prefix(
    mock_generate_temp_s3_tokens, s3_credentials
):
    expected_bucket = "fake_bucket"
    expected_prefix = "fake_prefix"
    mock_generate_temp_s3_tokens.return_value = (
        s3_credentials,
        expected_bucket,
        expected_prefix,
        "read",
    )
    s3_client_manager = S3ClientManager(omixatlas_id="test_omixatlas_id")
    bucket, prefix = s3_client_manager.get_upload_path()

    assert (
        bucket == expected_bucket
    ), "get_upload_path should return the correct bucket name"
    assert prefix == expected_prefix, "get_upload_path should return the correct prefix"


@patch("polly.data_management.S3ClientManager._generate_temp_s3_tokens")
def test_get_access_level_returns_correct_access(
    mock_generate_temp_s3_tokens, s3_credentials
):
    expected_access_level = "read"
    mock_generate_temp_s3_tokens.return_value = (
        s3_credentials,
        "fake_bucket",
        "fake_prefix",
        expected_access_level,
    )
    s3_client_manager = S3ClientManager(omixatlas_id="test_omixatlas_id")
    access_level = s3_client_manager.get_access_level()

    assert (
        access_level == expected_access_level
    ), "get_access_level should return the correct access level"


@patch("polly.data_management.PollySession.post")
def test_generate_temp_s3_tokens_returns_credentials(mock_post, s3_credentials):
    expected_bucket = "fake_bucket"
    expected_prefix = "fake_prefix"
    expected_access_level = "read"
    mock_post.return_value.json.return_value = {
        "data": {
            "attributes": {
                "bucket_name": expected_bucket,
                "prefix": expected_prefix,
                "access_level": expected_access_level,
                "tokens": {
                    "AccessKeyId": s3_credentials["access_key"],
                    "SecretAccessKey": s3_credentials["secret_key"],
                    "SessionToken": s3_credentials["token"],
                    "Expiration": s3_credentials["expiry_time"],
                },
            }
        }
    }
    mock_post.return_value.raise_for_status = MagicMock()

    s3_client_manager = S3ClientManager(omixatlas_id="test_omixatlas_id")
    (
        credentials,
        bucket,
        prefix,
        access_level,
    ) = s3_client_manager._generate_temp_s3_tokens()

    assert credentials["access_key"] == s3_credentials["access_key"]
    assert credentials["secret_key"] == s3_credentials["secret_key"]
    assert credentials["token"] == s3_credentials["token"]
    assert credentials["expiry_time"] == s3_credentials["expiry_time"]
    assert bucket == expected_bucket
    assert prefix == expected_prefix
    assert access_level == expected_access_level


@patch("polly.data_management.S3ClientManager._generate_temp_s3_tokens")
@patch("botocore.session.Session.set_credentials")
def test_get_autorefresh_session_returns_session_details(
    mock_set_credentials, mock_generate_temp_s3_tokens, s3_credentials
):
    mock_generate_temp_s3_tokens.return_value = (
        s3_credentials,
        "fake_bucket",
        "fake_prefix",
        "read",
    )

    s3_client_manager = S3ClientManager(omixatlas_id="test_omixatlas_id")
    session_details = s3_client_manager._get_autorefresh_session()

    assert isinstance(
        session_details, S3SessionDetails
    ), "_get_autorefresh_session should return an _S3SessionDetails instance"
    assert (
        session_details.bucket == "fake_bucket"
    ), "The bucket name should be set correctly in the session details"
    assert (
        session_details.prefix == "fake_prefix"
    ), "The prefix should be set correctly in the session details"
    assert (
        session_details.access == "read"
    ), "The access level should be set correctly in the session details"


@patch("polly.data_management.infer_file_type")
def test_is_supported_format_with_supported_extension(mock_infer_file_type):
    mock_infer_file_type.return_value = ("csv", ".csv")
    assert (
        is_supported_format("data.csv") is True
    ), "Should return True for supported file format"


@patch("polly.data_management.infer_file_type")
def test_is_supported_format_with_unsupported_extension(mock_infer_file_type):
    mock_infer_file_type.side_effect = UnsupportedFormat("Unsupported file format")
    assert (
        is_supported_format("data.xyz") is False
    ), "Should return False for unsupported file format"


def test_infer_file_type_supported_extension():
    assert infer_file_type("example.gct") == (
        "gct",
        ".gct",
    ), "Should return ('gct', '.gct') for .gct files"
    assert infer_file_type("example.csv") == (
        "csv",
        ".csv",
    ), "Should return ('csv', '.csv') for .csv files"


def test_infer_file_type_unsupported_extension():
    with pytest.raises(UnsupportedFormat, match="Couldn't infer file type"):
        infer_file_type("example.xyz")


def test_extract_extension_from_s3_uri_with_extension():
    assert (
        extract_extension_from_s3_uri("s3://mybucket/myfile.txt") == ".txt"
    ), "Should return '.txt' for myfile.txt"


def test_extract_extension_from_s3_uri_without_extension():
    assert (
        extract_extension_from_s3_uri("s3://mybucket/myfile") == ""
    ), "Should return an empty string for myfile with no extension"


def test_extract_extension_from_s3_uri_with_query_parameters():
    assert (
        extract_extension_from_s3_uri("s3://mybucket/myfile.txt?versionId=someversion")
        == ".txt"
    ), "Should return '.txt' for myfile.txt with query parameters"


def test_extract_extension_from_s3_uri_with_multi_part_extension():
    assert (
        extract_extension_from_s3_uri("s3://mybucket/myfile.json.gz") == ".json.gz"
    ), "Should return '.json.gz' for an S3 URI with a multi-part extension"


def test_extract_file_extension_valid_path():
    assert (
        extract_file_extension("example.csv") == ".csv"
    ), "Should return '.csv' for a valid file path with extension"


def test_extract_file_extension_directory_path():
    with pytest.raises(
        ValueError, match="The file path is either an empty string or a directory path"
    ):
        extract_file_extension("/path/to/directory/")


def test_extract_file_extension_no_extension():
    with pytest.raises(
        ValueError, match="The file path does not contain a file extension"
    ):
        extract_file_extension("example")


def test_extract_file_extension_with_multi_part_extension():
    assert (
        extract_file_extension("example.json.gz") == ".json.gz"
    ), "Should return '.json.gz' for a file path with a multi-part extension"


@pytest.fixture
def mock_version(monkeypatch, mock_s3_client_manager):
    version_instance = VersionBase(
        dataset_id="test_dataset",
        omixatlas_id="test_omixatlas_id",
        data_type="test_data_type",
        version_id="test_version",
        study_id="test_study",
        metadata_location="s3://test_bucket/metadata.json.gz?versionId=someversionid",
        data_location="s3://test_bucket/data.csv?versionId=someversionid",
        data_format="csv",
        created_at=1234567890,
    )
    version_instance._s3_client_manager = mock_s3_client_manager
    return version_instance


@patch("polly_services.dataset.read_bytes")
def test_version_metadata_returns_correct_metadata(mock_read_bytes, mock_version):
    expected_metadata = {"description": "This is test metadata."}
    mock_read_bytes.return_value = gzip.compress(
        json.dumps(expected_metadata).encode("utf-8")
    )

    metadata = mock_version.metadata()

    assert (
        metadata == expected_metadata
    ), "metadata method should return the correct metadata dictionary"


@pytest.fixture
def mock_version_with_format(monkeypatch, mock_s3_client_manager):
    version_instance = VersionBase(
        dataset_id="test_dataset",
        omixatlas_id="test_omixatlas_id",
        data_type="test_data_type",
        version_id="test_version",
        study_id="test_study",
        metadata_location="s3://test_bucket/metadata.json.gz",
        data_location="s3://test_bucket/data.csv",
        created_at=1234567890,
    )
    version_instance._s3_client_manager = mock_s3_client_manager
    return version_instance


@patch("cmapPy.pandasGEXpress.parse.parse")
@patch("polly_services.dataset.copy_file")
def test_version_load_gct(
    mock_copy_file, mock_parse, mock_version_with_format, monkeypatch
):
    from pandas import DataFrame

    mock_version_with_format.data_format = "gct"
    mock_df = DataFrame()
    mock_gctoo_instance = GCToo(data_df=mock_df)
    mock_parse.return_value = mock_gctoo_instance

    result = mock_version_with_format.load()

    assert isinstance(result, GCToo), "load should return a GCToo object for GCT files"


@patch("polly.data_management.copy_file")
def test_version_load_unsupported_format(mock_copy_file, mock_version_with_format):
    mock_version_with_format.data_format = "unsupported_format"

    with pytest.raises(ValueError):
        mock_version_with_format.load()


@patch("polly_services.dataset.copy_file")
def test_version_download_to_file_path(mock_copy_file, mock_version):
    mock_copy_file.return_value = None  # Simulate successful copy
    file_path = "/path/to/local/data.csv"
    result = mock_version.download(file_path)

    mock_copy_file.assert_called_once_with(
        mock_version.data_location,
        file_path,
        s3_client=mock_version._s3_client_manager.get_client(),
    )
    assert (
        result == file_path
    ), "download should return the file path where the data was downloaded"


@patch("polly_services.dataset.copy_file")
def test_version_download_to_directory_path(mock_copy_file, mock_version):
    directory_path = "/path/to/local/"
    expected_file_path = os.path.join(directory_path, mock_version.dataset_id + ".csv")
    result = mock_version.download(directory_path)

    mock_copy_file.assert_called_once_with(
        mock_version.data_location,
        expected_file_path,
        s3_client=mock_version._s3_client_manager.get_client(),
    )
    assert (
        result == expected_file_path
    ), "download should return the correct file path within the directory"


@patch("polly_services.dataset.copy_file")
def test_version_download_uses_correct_extension(mock_copy_file, mock_version):
    mock_copy_file.return_value = None  # Simulate successful copy
    mock_version.data_format = "json+gzip"
    directory_path = "/path/to/local/"
    expected_file_path = os.path.join(
        directory_path, mock_version.dataset_id + ".json.gz"
    )
    result = mock_version.download(directory_path)

    assert (
        result == expected_file_path
    ), "download should use correct file extension based on the data_format attribute"


@pytest.fixture
def mock_polly_session(monkeypatch):
    mock_session = MagicMock()
    monkeypatch.setattr("polly.data_management.PollySession", mock_session)
    return mock_session


@pytest.fixture
def catalog(mock_polly_session, mock_s3_client_manager):
    from polly.data_management import Catalog

    return Catalog(omixatlas_id="test_omixatlas_id")


@patch("polly.data_management.copy_file")
def test_create_dataset_success(
    mock_copy_file, catalog, mock_polly_session, mock_s3_client_manager
):
    # Arrange
    dataset_id = "test_dataset_id"
    data_type = "test_data_type"
    data = "path/to/data.csv"
    metadata_location = "s3://test_bucket/metadata.json.gz?versionId=someversionid"
    data_location = "s3://test_bucket/test_prefix/data.csv"
    mock_s3_client_manager.return_value.get_client.return_value = MagicMock()
    mock_s3_client_manager.return_value.get_upload_path.return_value = (
        "test_bucket",
        "test_prefix",
    )
    mock_copy_file.return_value = "s3://test_bucket/test_prefix/data.csv"
    mock_polly_session.post.return_value.json.return_value = {
        "data": {
            "attributes": {
                "dataset_id": dataset_id,
                "data_type": data_type,
                "metadata_location": metadata_location,
                "data_location": data_location,
                "data_format": "csv",
            }
        }
    }
    catalog._get_session = lambda: mock_polly_session

    # Act
    dataset = catalog.create_dataset(
        dataset_id, data_type, data, metadata={"dummy": 123}
    )

    # Assert
    mock_s3_client_manager.return_value.get_client.assert_called_once()
    mock_polly_session.post.assert_called_once()
    assert isinstance(
        dataset, Dataset
    ), "create_dataset should return a Dataset instance"
    assert dataset.dataset_id == dataset_id, "Dataset ID should be set correctly"
    assert dataset.data_type == data_type, "Data type should be set correctly"
    assert dataset.metadata_location == metadata_location
    assert dataset.data_location == data_location


@pytest.mark.parametrize(
    "data, metadata, data_format, expected_data_location, expected_metadata_location",
    [
        (
            "path/to/new_data.csv",
            {"new": "metadata"},
            "csv",
            "s3://test_bucket/test_prefix/new_data.csv",
            "s3://test_bucket/metadata.json.gz?versionId=someversionid",
        ),
        (
            None,
            {"updated": "metadata"},
            None,
            "s3://test_bucket/test_prefix/data.csv",
            "s3://test_bucket/metadata.json.gz?versionId=someversionid",
        ),
    ],
)
@patch("polly.data_management.copy_file")
def test_update_dataset_success(
    mock_copy_file,
    catalog,
    mock_polly_session,
    mock_s3_client_manager,
    data,
    metadata,
    data_format,
    expected_data_location,
    expected_metadata_location,
):
    # Arrange
    dataset_id = "test_dataset_id"
    data_type = "test_data_type"
    mock_s3_client_manager.return_value.get_client.return_value = MagicMock()
    mock_s3_client_manager.return_value.get_upload_path.return_value = (
        "test_bucket",
        "test_prefix",
    )
    mock_copy_file.return_value = expected_data_location
    mock_polly_session.patch.return_value.json.return_value = {
        "data": {
            "id": dataset_id,
            "attributes": {
                "dataset_id": dataset_id,
                "data_type": data_type,
                "metadata_location": expected_metadata_location,
                "data_location": expected_data_location,
                "data_format": data_format or "csv",
            },
        }
    }
    catalog._get_session = lambda: mock_polly_session

    # Act
    dataset = catalog.update_dataset(
        dataset_id, data_type=data_type, data=data, metadata=metadata
    )

    # Assert
    if data:
        mock_copy_file.assert_called_once()
    mock_polly_session.patch.assert_called_once()
    assert isinstance(
        dataset, Dataset
    ), "update_dataset should return a Dataset instance"
    assert dataset.dataset_id == dataset_id, "Dataset ID should be set correctly"
    assert dataset.data_type == data_type, "Data type should be set correctly"
    assert dataset.metadata_location == expected_metadata_location
    assert dataset.data_location == expected_data_location


def test_create_dataset_invalid_dataset_id(catalog):
    # Arrange
    invalid_dataset_id = ""
    data_type = "test_data_type"
    data = "path/to/data.csv"
    metadata = {"description": "test metadata"}

    # Act & Assert
    with pytest.raises(ValueError, match="Empty string cannot be used as dataset_id"):
        catalog.create_dataset(invalid_dataset_id, data_type, data, metadata)


def test_create_dataset_unsupported_data_format(
    catalog, mock_polly_session, mock_s3_client_manager
):
    # Arrange
    dataset_id = "test_dataset_id"
    data_type = "test_data_type"
    data = "path/to/data.xyz"  # Unsupported file format
    metadata = {"description": "test metadata"}
    mock_s3_client_manager.return_value.get_client.return_value = MagicMock()
    mock_s3_client_manager.return_value.get_upload_path.return_value = (
        "test_bucket",
        "test_prefix",
    )

    # Act & Assert
    with pytest.raises(ValueError):
        catalog.create_dataset(dataset_id, data_type, data, metadata)


def test_create_dataset_missing_parameters(catalog):
    dataset_id = "test_dataset_id"
    data_type = "test_data_type"
    metadata = {"description": "test metadata"}

    with pytest.raises(
        TypeError, match="missing 1 required positional argument: 'data'"
    ):
        catalog.create_dataset(dataset_id, data_type, metadata=metadata)


def test_get_dataset_success(catalog, mock_polly_session):
    # Arrange
    dataset_id = "test_dataset_id"
    expected_response = {
        "data": {
            "id": dataset_id,
            "attributes": {
                "dataset_id": dataset_id,
                "data_type": "test_data_type",
                "metadata_location": "s3://test_bucket/metadata.json.gz",
                "data_location": "s3://test_bucket/data.csv",
                "data_format": "csv",
                "last_modified_at": 1234567890,
            },
        }
    }
    mock_polly_session.get.return_value.json.return_value = expected_response
    mock_polly_session.get.return_value.status_code = 200
    catalog._get_session = lambda: mock_polly_session

    # Act
    dataset = catalog.get_dataset(dataset_id)

    # Assert
    mock_polly_session.get.assert_called_once_with(
        f"{catalog._get_session().discover_url}/repositories/{catalog.omixatlas_id}/datasets/{dataset_id}"
    )
    assert isinstance(dataset, Dataset)
    assert dataset.dataset_id == dataset_id
    assert dataset.data_type == expected_response["data"]["attributes"]["data_type"]
    assert (
        dataset.metadata_location
        == expected_response["data"]["attributes"]["metadata_location"]
    )
    assert (
        dataset.data_location
        == expected_response["data"]["attributes"]["data_location"]
    )
    assert dataset.data_format == expected_response["data"]["attributes"]["data_format"]
    assert (
        dataset.last_modified_at
        == expected_response["data"]["attributes"]["last_modified_at"]
    )


def test_get_version_success(catalog, mock_polly_session):
    # Arrange
    dataset_id = "test_dataset_id"
    version_id = "test_version_id"
    expected_response = {
        "data": {
            "id": version_id,
            "attributes": {
                "version_id": version_id,
                "dataset_id": dataset_id,
                "data_type": "test_data_type",
                "metadata_location": "s3://test_bucket/metadata.json.gz",
                "data_location": "s3://test_bucket/data.csv",
                "data_format": "csv",
                "created_at": 1234567890,
            },
        }
    }
    mock_polly_session.get.return_value.json.return_value = expected_response
    mock_polly_session.get.return_value.status_code = 200
    catalog._get_session = lambda: mock_polly_session

    # Act
    version = catalog.get_version(dataset_id, version_id)

    # Assert
    mock_polly_session.get.assert_called_once_with(
        f"{catalog._get_session().discover_url}/repositories/"
        f"{catalog.omixatlas_id}/datasets/{dataset_id}/versions/{version_id}"
    )
    assert isinstance(version, DatasetVersion)
    assert version.version_id == version_id
    assert version.dataset_id == dataset_id
    assert version.data_type == expected_response["data"]["attributes"]["data_type"]
    assert (
        version.metadata_location
        == expected_response["data"]["attributes"]["metadata_location"]
    )
    assert (
        version.data_location
        == expected_response["data"]["attributes"]["data_location"]
    )
    assert version.data_format == expected_response["data"]["attributes"]["data_format"]
    assert version.created_at == expected_response["data"]["attributes"]["created_at"]


def test_list_datasets_in_study_success(catalog, mock_polly_session):
    # Arrange
    study_id = "test_study_id"
    expected_dataset_ids = ["dataset1", "dataset2"]
    expected_response = {
        "relationships": {
            "datasets": {"data": [{"id": "dataset1"}, {"id": "dataset2"}]}
        }
    }
    mock_polly_session.get.return_value.json.return_value = expected_response
    catalog._get_session = lambda: mock_polly_session

    # Act
    dataset_ids = catalog.list_datasets_in_study(study_id)

    # Assert
    mock_polly_session.get.assert_called_once_with(
        f"{catalog._get_session().discover_url}/repositories/{catalog.omixatlas_id}/studies/{study_id}"
    )
    assert dataset_ids == expected_dataset_ids


def test_list_studies_success(catalog, mock_polly_session):
    # Arrange
    expected_study_ids = ["study1", "study2"]
    expected_response = {"data": [{"id": "study1"}, {"id": "study2"}]}
    mock_polly_session.get.return_value.json.return_value = expected_response
    catalog._get_session = lambda: mock_polly_session

    # Act
    study_ids = catalog.list_studies()

    # Assert
    mock_polly_session.get.assert_called_once_with(
        f"{catalog._get_session().discover_url}/repositories/{catalog.omixatlas_id}/studies"
    )
    assert study_ids == expected_study_ids


def test_list_datasets_success(catalog, mock_polly_session):
    # Arrange
    expected_datasets = [
        {"id": "dataset1", "attributes": {"data_type": "type1"}},
        {"id": "dataset2", "attributes": {"data_type": "type2"}},
    ]
    expected_response = {"data": expected_datasets}
    mock_polly_session.get.return_value.json.return_value = expected_response
    catalog._get_session = lambda: mock_polly_session

    # Act
    datasets = catalog.list_datasets()

    # Assert
    assert all(isinstance(dataset, Dataset) for dataset in datasets)
    assert [dataset.dataset_id for dataset in datasets] == [
        "dataset1",
        "dataset2",
    ]


def test_list_versions_success(catalog, mock_polly_session):
    # Arrange
    dataset_id = "test_dataset_id"
    expected_versions = [
        {"id": "version1", "attributes": {"version_id": "version1"}},
        {"id": "version2", "attributes": {"version_id": "version2"}},
    ]
    expected_response = {"data": expected_versions}
    mock_polly_session.get.return_value.json.return_value = expected_response
    catalog._get_session = lambda: mock_polly_session

    # Act
    versions = catalog.list_versions(dataset_id)

    # Assert
    assert all(isinstance(version, DatasetVersion) for version in versions)
    assert [version.version_id for version in versions] == [
        "version1",
        "version2",
    ]


def test_delete_dataset_success(catalog, mock_polly_session):
    # Arrange
    dataset_id = "test_dataset_id"
    mock_polly_session.delete.return_value.status_code = 204
    catalog._get_session = lambda: mock_polly_session

    # Act
    catalog.delete_dataset(dataset_id)

    # Assert
    mock_polly_session.delete.assert_called_once_with(
        f"{catalog._get_session().discover_url}/repositories/{catalog.omixatlas_id}/datasets/{dataset_id}?params=%7B%7D"
    )


def test_set_parent_study_success(catalog, mock_polly_session):
    # Arrange
    dataset_id = "test_dataset_id"
    study_id = "test_study_id"
    mock_polly_session.patch.return_value.status_code = 204
    catalog._get_session = lambda: mock_polly_session

    # Act
    catalog.set_parent_study(dataset_id, study_id)

    # Assert
    mock_polly_session.patch.assert_called_once_with(
        f"{catalog._get_session().discover_url}/repositories/{catalog.omixatlas_id}/datasets/{dataset_id}",
        json={
            "data": {
                "type": "datasets",
                "id": dataset_id,
                "attributes": {"study_id": study_id},
            },
            "meta": {"ingestion_params": None},
        },
    )


def test_catalog_reflects_changes_in_default_session():
    """
    Test that changes to Polly.default_session are reflected in an existing Catalog instance.
    """
    from polly.data_management import Catalog
    from polly.auth import Polly

    Polly.default_session = MagicMock(spec=PollySession)

    catalog = Catalog(omixatlas_id="12345")

    assert catalog._get_session() is Polly.default_session

    Polly.default_session = MagicMock(spec=PollySession)

    assert (
        catalog._get_session() is Polly.default_session
    ), "Catalog instance should reflect changes in Polly.default_session"


def test_s3_client_manager_reflects_changes_in_default_session():
    """
    Test that changes to Polly.default_session are reflected in an existing S3ClientManager instance.
    """
    from polly.data_management import S3ClientManager
    from polly.auth import Polly

    s3_client_manager = S3ClientManager(omixatlas_id="test_omixatlas_id")

    Polly.default_session = MagicMock(spec=PollySession)

    assert s3_client_manager.get_polly_session() is Polly.default_session

    # Change Polly.default_session to a new mock session
    Polly.default_session = MagicMock(spec=PollySession)

    # The existing S3ClientManager instance should now reflect the new default session
    assert (
        s3_client_manager.get_polly_session() is Polly.default_session
    ), "S3ClientManager instance should reflect changes in Polly.default_session"


@pytest.mark.parametrize(
    "tag, derived_from",
    [
        (None, "s3://test_bucket/main.gct"),
        ("test_tag", "s3://test_bucket/main.gct"),
        (None, None),
        ("test_tag", None),
    ],
)
@patch("polly.data_management.copy_file")
def test_attach_file_success(
    mock_copy_file,
    catalog,
    mock_polly_session,
    mock_s3_client_manager,
    tag,
    derived_from,
):
    # Arrange
    dataset_id = "test_dataset_id"
    path = "path/to/file.txt"
    file_name = "file.txt"
    file_format = "txt"
    source_version_id = "abcd"
    file_location = "s3://test_bucket/test_prefix/file.txt"

    mock_s3_client_manager.return_value.get_client.return_value = MagicMock()
    mock_s3_client_manager.return_value.get_upload_path.return_value = (
        "test_bucket",
        "test_prefix",
    )
    mock_copy_file.return_value = "s3://test_bucket/test_prefix/file.txt"
    mock_polly_session.post.return_value.json.return_value = {
        "data": {
            "attributes": {
                "file_name": file_name,
                "file_format": file_format,
                "file_location": file_location,
                "tag": tag,
                "derived_from": derived_from,
            }
        }
    }
    catalog._get_session = lambda: mock_polly_session

    # Act
    file = catalog.attach_file(
        dataset_id, path, tag=tag, source_version_id=source_version_id
    )

    # Assert
    mock_s3_client_manager.return_value.get_client.assert_called_once()
    mock_polly_session.post.assert_called_once()
    assert isinstance(
        file, SupplementaryFile
    ), "attach_file should return a SupplementaryFile instance"
    assert file.file_name == file_name, "File name should be set correctly"
    assert file.file_format == file_format, "File format should be set correctly"
    assert file.file_location == file_location, "File location should be set correctly"
    assert file.tag == tag, "Tag should be set correctly"
    assert file.derived_from == derived_from


def test_list_files_success(catalog, mock_polly_session):
    # Arrange
    dataset_id = "test_dataset_id"
    mock_polly_session.get.return_value.json.return_value = {
        "data": [
            {
                "type": "file",
                "id": "1",
                "attributes": {
                    "file_name": "file1.txt",
                    "file_format": "txt",
                    "file_location": "s3://test_bucket/test_prefix/file1.txt",
                },
            },
            {
                "type": "file",
                "id": "2",
                "attributes": {
                    "file_name": "file2.txt",
                    "file_format": "txt",
                    "file_location": "s3://test_bucket/test_prefix/file2.txt",
                },
            },
        ]
    }
    catalog._get_session = lambda: mock_polly_session

    # Act
    files = catalog.list_files(dataset_id)

    # Assert
    mock_polly_session.get.assert_called_once()
    assert len(files) == 2, "list_files should return a list of 2 files"
    assert isinstance(
        files[0], SupplementaryFile
    ), "list_files should return a list of SupplementaryFile instances"


def test_get_file_success(catalog, mock_polly_session):
    # Arrange
    dataset_id = "test_dataset_id"
    file_name = "file.txt"
    mock_polly_session.get.return_value.json.return_value = {
        "data": {
            "type": "file",
            "id": "1",
            "attributes": {
                "file_name": file_name,
                "file_format": "txt",
                "file_location": "s3://test_bucket/test_prefix/file.txt",
            },
        }
    }
    catalog._get_session = lambda: mock_polly_session

    # Act
    file = catalog.get_file(dataset_id, file_name)

    # Assert
    mock_polly_session.get.assert_called_once()
    assert isinstance(
        file, SupplementaryFile
    ), "get_file should return a SupplementaryFile instance"
    assert file.file_name == file_name, "File name should be set correctly"


def test_delete_file_success(catalog, mock_polly_session):
    # Arrange
    dataset_id = "test_dataset_id"
    file_name = "file.txt"
    catalog._get_session = lambda: mock_polly_session

    # Act
    catalog.delete_file(dataset_id, file_name)

    # Assert
    mock_polly_session.delete.assert_called_once()


@patch("polly_services.dataset.copy_file")
def test_file_download_success(
    mock_copy_file, catalog, mock_polly_session, mock_s3_client_manager
):
    # Arrange
    mock_copy_file.return_value = None  # Simulate successful copy
    dataset_id = "test_dataset_id"
    file_name = "file.txt"
    file_path = "./"
    mock_polly_session.get.return_value.json.return_value = {
        "data": {
            "type": "file",
            "id": "1",
            "attributes": {
                "file_name": file_name,
                "file_format": "txt",
                "file_location": "s3://test_bucket/test_prefix/file.txt",
            },
        }
    }
    catalog._get_session = lambda: mock_polly_session

    file = catalog.get_file(dataset_id, file_name)
    file._s3_client_manager = mock_s3_client_manager

    # Act
    download_path = file.download(file_path)

    # Assert
    mock_copy_file.assert_called_once()
    assert (
        download_path == file_path + file_name
    ), "Download path should be set correctly"
