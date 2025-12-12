from unittest.mock import patch
from cryptography.fernet import Fernet
from polly.validation import Validation
from polly import constants as const
from polly.validation_hlpr import (
    warning_validation_scope_not_defined,
    warning_validation_config_incorrectly_defined,
)


# Utility function for mocking API responses
def mock_encryption_key():
    return Fernet.generate_key().decode("utf-8")


@patch("polly.helpers.get_platform_value_from_env", return_value="polly")
@patch("polly.auth.Polly.get_session")
def test_validation_init(mock_get_session, mock_get_platform_value_from_env):
    token = "fake_token"
    env = "dev"
    validation_obj = Validation(token, env)

    mock_get_platform_value_from_env.assert_called_with(
        const.COMPUTE_ENV_VARIABLE, "polly", "dev"
    )
    mock_get_session.assert_called_with(token, env="polly")
    assert validation_obj.session is not None, "Session initialization failed."


@patch(
    "polly.validation_hlpr.get_indexing_configs", return_value={"indexing": "configs"}
)
@patch(
    "polly.validation_hlpr.get_dataset_level_validation_config",
    return_value={"validate": True},
)
@patch(
    "polly.validation_hlpr.get_sample_level_validation_configs",
    return_value={"validate": False},
)
def test_get_ingestion_configs(
    mock_sample_config, mock_dataset_config, mock_indexing_config
):
    validation_obj = Validation()

    # Call the method
    configs = validation_obj.get_ingestion_configs(
        indexing_configs=True, validation_configs=True
    )

    # Check that the returned configs have the right structure
    assert "indexing" in configs, "Indexing configs not found."
    assert "validation_check" in configs, "Validation configs section not found."
    assert (
        configs["validation_check"]["dataset"]["validate"] is True
    ), "Dataset validation config incorrect."
    assert (
        configs["validation_check"]["sample"]["validate"] is False
    ), "Sample validation config incorrect."


@patch(
    "polly.validation_hlpr.get_indexing_configs", return_value={"indexing": "configs"}
)
def test_get_ingestion_configs_indexing_only(mock_indexing_config):
    validation_obj = Validation()

    configs = validation_obj.get_ingestion_configs(
        indexing_configs=True, validation_configs=False
    )

    # Assert only indexing configs are present
    assert "indexing" in configs, "Indexing configs not returned as expected."
    assert (
        "validation_check" not in configs
    ), "Validation configs should not be present."


@patch("polly.helpers.parameter_check_for_repo_id")
@patch("polly.validation_hlpr.data_metadata_parameter_check")
@patch("polly.validation_hlpr.schema_config_check")
def test_check_validate_dataset_params(
    mock_schema_check, mock_metadata_check, mock_repo_id_check
):
    validation_obj = Validation()

    repo_id = "repo123"
    source_folder_path = {"data": "/path/to/data"}
    schema_config = {"config_key": "config_value"}

    validation_obj._check_validate_dataset_params(
        repo_id, source_folder_path, schema_config
    )

    mock_repo_id_check.assert_called_with(repo_id)
    mock_metadata_check.assert_called_with(source_folder_path)
    mock_schema_check.assert_called_with(schema_config)


@patch("polly.helpers.parameter_check_for_repo_id")
@patch("polly.validation_hlpr.data_metadata_parameter_check")
def test_check_validate_dataset_params_no_schema(
    mock_metadata_check, mock_repo_id_check
):
    validation_obj = Validation()

    repo_id = "repo123"
    source_folder_path = {"data": "/path/to/data"}
    schema_config = {}

    validation_obj._check_validate_dataset_params(
        repo_id, source_folder_path, schema_config
    )

    mock_repo_id_check.assert_called_with(repo_id)
    mock_metadata_check.assert_called_with(source_folder_path)
    mock_metadata_check.assert_called_once()

    # Check if schema_config was NOT passed to mock_repo_id_check
    for call in mock_repo_id_check.call_args_list:
        assert (
            schema_config not in call.args
        ), "Schema config check should not have been called."


def test_warning_validation_scope_not_defined():
    with patch("warnings.warn") as mock_warn:
        warning_validation_scope_not_defined("file.json")
        mock_warn.assert_called(), "Warning for undefined validation scope not called."


def test_warning_validation_config_incorrectly_defined():
    with patch("warnings.warn") as mock_warn:
        warning_validation_config_incorrectly_defined("file.json")
        mock_warn.assert_called(), "Warning for incorrectly defined validation config not called."
