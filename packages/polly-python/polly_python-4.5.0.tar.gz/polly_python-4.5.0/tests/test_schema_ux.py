from typing import Dict
from polly.auth import Polly
from polly import omixatlas
import pandas as pd
import os
import pytest
import requests
import json
from polly.errors import error_handler
import test_constants as test_const
import polly_services
from polly.errors import paramException

key = "TEST_POLLY_API_KEY"
token = os.getenv(key)


def test_obj_initialization():
    assert Polly.get_session(token, env="testpolly") is not None
    assert omixatlas.OmixAtlas(token, env="testpolly") is not None


def test_get_schema_with_repo_id_and_both_dataset_and_sample_schema_param():
    # ingestion_test_1
    repo_id = "1654268055800"
    schema_type_dict = {"dataset": "files", "sample": "gct_metadata"}
    schema_obj = omixatlas.OmixAtlas(token, env="testpolly")
    source = ""
    data_type = ""
    schema = polly_services.schema.schema_hlpr.get_schema_from_api(
        schema_obj, repo_id, schema_type_dict, source, data_type
    )
    assert isinstance(schema, Dict)
    assert schema["dataset"] is not None
    assert schema["sample"] is not None


def test_get_schema_with_repo_id_and_sample_schema_param():
    # ingestion_test_1
    repo_id = "1654268055800"
    schema_type_dict = {"sample": "gct_metadata"}
    schema_obj = omixatlas.OmixAtlas(token, env="testpolly")
    source = ""
    data_type = ""
    schema = polly_services.schema.schema_hlpr.get_schema_from_api(
        schema_obj, repo_id, schema_type_dict, source, data_type
    )
    assert isinstance(schema, Dict)
    assert schema["sample"] is not None


def test_get_schema_full_payload():
    # ingestion_test_1
    repo_id = "1654268055800"
    schema_type_dict = {"dataset": "files", "sample": "gct_metadata"}
    schema_obj = omixatlas.OmixAtlas(token, env="testpolly")
    schema = polly_services.schema.schema_hlpr.get_full_schema_payload_from_api(
        schema_obj, repo_id, schema_type_dict
    )

    assert isinstance(schema, Dict)
    # directly payload of API is returned
    assert schema["dataset"] is not None
    assert schema["sample"] is not None


def test_get_schema_with_repo_id_and_dataset_schema_param():
    # ingestion_test_1
    repo_id = "1654268055800"
    schema_type_dict = {"dataset": "files"}
    schema_obj = omixatlas.OmixAtlas(token, env="testpolly")
    source = ""
    data_type = ""
    schema = polly_services.schema.schema_hlpr.get_schema_from_api(
        schema_obj, repo_id, schema_type_dict, source, data_type
    )
    assert isinstance(schema, Dict)
    assert schema["dataset"] is not None


def test_get_schema_type_dataset_schema_level_single_cell_bool_false_as_params():
    schema_level = ["dataset", "sample"]
    data_type = "others"
    # schema_obj = omixatlas.OmixAtlas(token, env="testpolly")
    schema_type = polly_services.schema.schema_hlpr.get_schema_type(
        schema_level, data_type
    )
    assert isinstance(schema_type, Dict)
    assert schema_type["dataset"] is not None
    assert schema_type["sample"] is not None
    assert schema_type["sample"] == "gct_metadata"


def test_get_schema_type_dataset_schema_level_single_cell_bool_true_as_params():
    schema_level = ["dataset", "sample"]
    data_type = "single_cell"
    # schema_obj = omixatlas.OmixAtlas(token, env="testpolly")
    schema_type = polly_services.schema.schema_hlpr.get_schema_type(
        schema_level, data_type
    )
    assert isinstance(schema_type, Dict)
    assert schema_type["dataset"] is not None
    assert schema_type["sample"] is not None
    assert schema_type["sample"] == "h5ad_metadata"


def test_get_schema_type_dataset_as_params():
    schema_level = ["dataset"]
    data_type = "single_cell"
    # schema_obj = omixatlas.OmixAtlas(token, env="testpolly")
    schema_type = polly_services.schema.schema_hlpr.get_schema_type(
        schema_level, data_type
    )
    assert isinstance(schema_type, Dict)
    assert schema_type["dataset"] is not None


def test_get_schema_type_schema_level_single_cell_bool_true_as_params():
    schema_level = ["sample"]
    data_type = "single_cell"
    # schema_obj = omixatlas.OmixAtlas(token, env="testpolly")
    schema_type = polly_services.schema.schema_hlpr.get_schema_type(
        schema_level, data_type
    )
    assert isinstance(schema_type, Dict)
    assert schema_type["sample"] is not None
    assert schema_type["sample"] == "h5ad_metadata"


def test_get_schema_type_schema_level_single_cell_bool_false_as_params():
    schema_level = ["sample"]
    data_type = "others"
    # schema_obj = omixatlas.OmixAtlas(token, env="testpolly")
    schema_type = polly_services.schema.schema_hlpr.get_schema_type(
        schema_level, data_type
    )
    assert isinstance(schema_type, Dict)
    assert schema_type["sample"] is not None
    assert schema_type["sample"] == "gct_metadata"


@pytest.fixture()
def get_ingestion_test_1_schema_fixture():
    base_polly_py_test_url = test_const.POLLY_PY_TEST_FILES_URL
    parent_dir = os.getcwd()
    test_dir = "tests"
    test_path = os.path.join(parent_dir, test_dir)
    if not os.path.isdir(test_path):
        os.makedirs(test_path)

    ingestion_test_1_schema_file = (
        f"{base_polly_py_test_url}/ingestion_test_1_schema.json"
    )
    ingestion_test_1_schema = requests.get(ingestion_test_1_schema_file)
    error_handler(ingestion_test_1_schema)
    ingestion_test_1_schema_file_name = "ingestion_test_1_schema.json"
    with open(
        os.path.join(test_path, ingestion_test_1_schema_file_name), "w"
    ) as file_1:
        file_1_content = ingestion_test_1_schema.text
        file_1.write(file_1_content)

    with open(
        f"{test_path}/{ingestion_test_1_schema_file_name}", "r+"
    ) as ingestion_test_1_schema:
        body = json.load(ingestion_test_1_schema)

    return body


@pytest.fixture
def get_ingestion_test_1_schema_fixture_summary():
    base_polly_py_test_url = test_const.POLLY_PY_TEST_FILES_URL
    parent_dir = os.getcwd()
    test_dir = "tests"
    test_path = os.path.join(parent_dir, test_dir)
    if not os.path.isdir(test_path):
        os.makedirs(test_path)

    ingestion_test_1_schema_file = (
        f"{base_polly_py_test_url}/ingestion_test_1_schema_summary.json"
    )
    ingestion_test_1_schema = requests.get(ingestion_test_1_schema_file)
    error_handler(ingestion_test_1_schema)
    ingestion_test_1_schema_file_name = "ingestion_test_1_schema_summary.json"
    with open(
        os.path.join(test_path, ingestion_test_1_schema_file_name), "w"
    ) as file_1:
        file_1_content = ingestion_test_1_schema.text
        file_1.write(file_1_content)

    with open(
        f"{test_path}/{ingestion_test_1_schema_file_name}", "r+"
    ) as ingestion_test_1_schema:
        body = json.load(ingestion_test_1_schema)

    print("----body------")
    print(body)
    return body


@pytest.fixture
def get_full_schema_payload_from_api_fixture(
    mocker, get_ingestion_test_1_schema_fixture
):
    Polly.auth(token, env="testpolly")
    nobj = omixatlas.OmixAtlas()
    # ingestion_test_1
    repo_id = test_const.INGESTION_TEST_1_REPO_ID
    fake_json = get_ingestion_test_1_schema_fixture
    response = mocker.patch.object(nobj.session, "get")
    response.return_value.status_code = 200
    response.return_value.json.return_value = fake_json
    schema_type_dict = {
        "datasets": "files",
        "samples": "gct_metadata",
        "features": "gct_row_metadata",
    }
    result = polly_services.schema.schema_hlpr.get_full_schema_payload_from_api(
        nobj, repo_id, schema_type_dict
    )
    return result


@pytest.fixture
def get_full_schema_payload_from_api_fixture_valid_level_names(
    mocker, get_ingestion_test_1_schema_fixture
):
    Polly.auth(token, env="testpolly")
    nobj = omixatlas.OmixAtlas()
    # ingestion_test_1
    repo_id = test_const.INGESTION_TEST_1_REPO_ID
    fake_json = get_ingestion_test_1_schema_fixture
    response = mocker.patch.object(nobj.session, "get")
    response.return_value.status_code = 200
    response.return_value.json.return_value = fake_json
    schema_type_dict = {
        "dataset": "files",
        "sample": "gct_metadata",
    }
    result = polly_services.schema.schema_hlpr.get_full_schema_payload_from_api(
        nobj, repo_id, schema_type_dict
    )
    return result


def test_get_schema_full_payload_dict_when_return_type_dict(
    mocker, get_full_schema_payload_from_api_fixture
):
    # ingestion_test_1
    mocker.patch(
        polly_services.schema.schema_hlpr.__name__
        + ".get_full_schema_payload_from_api",
        return_value=get_full_schema_payload_from_api_fixture,
    )

    repo_key_1 = "1654268055800"
    omix_obj_test = omixatlas.OmixAtlas(token, env="testpolly")
    resp = omix_obj_test.get_schema(
        repo_key_1, ["dataset"], source="all", data_type="all", return_type="dict"
    )

    assert isinstance(resp.datasets, Dict)


@pytest.fixture
def get_schema_from_api_fixture(mocker, get_ingestion_test_1_schema_fixture_summary):
    Polly.auth(token, env="testpolly")
    nobj = omixatlas.OmixAtlas()
    # ingestion_test_1
    repo_id = test_const.INGESTION_TEST_1_REPO_ID
    fake_json = get_ingestion_test_1_schema_fixture_summary
    print("---fake json----")
    print(fake_json)
    response = mocker.patch.object(nobj.session, "get")
    response.return_value.status_code = 200
    response.return_value.json.return_value = fake_json
    schema_type_dict = {
        "datasets": "files",
        "samples": "gct_metadata",
        "features": "gct_row_metadata",
    }
    source = "all"
    data_type = "all"
    result = polly_services.schema.schema_hlpr.get_schema_from_api(
        nobj, repo_id, schema_type_dict, source, data_type
    )
    return result


@pytest.fixture
def get_schema_from_api_fixture_level_names(
    mocker, get_ingestion_test_1_schema_fixture_summary
):
    Polly.auth(token, env="testpolly")
    nobj = omixatlas.OmixAtlas()
    # ingestion_test_1
    repo_id = test_const.INGESTION_TEST_1_REPO_ID
    fake_json = get_ingestion_test_1_schema_fixture_summary
    print("---fake json----")
    print(fake_json)
    response = mocker.patch.object(nobj.session, "get")
    response.return_value.status_code = 200
    response.return_value.json.return_value = fake_json
    schema_type_dict = {
        "dataset": "files",
        "sample": "gct_metadata",
    }
    source = "all"
    data_type = "all"
    result = polly_services.schema.schema_hlpr.get_schema_from_api(
        nobj, repo_id, schema_type_dict, source, data_type
    )
    return result


def test_get_schema_default_return_type(
    mocker, get_schema_from_api_fixture_level_names
):
    # default return type is dataframe
    # ingestion_test_1

    mocker.patch(
        polly_services.schema.schema_hlpr.__name__ + ".get_schema_from_api",
        return_value=get_schema_from_api_fixture_level_names,
    )

    repo_key_1 = "1654268055800"
    omix_obj_test = omixatlas.OmixAtlas(token, env="testpolly")
    resp = omix_obj_test.get_schema(
        repo_key_1, ["dataset"], source="all", data_type="all"
    )
    assert isinstance(resp.dataset, pd.DataFrame)


def test_get_schema_with_valid_table_names(mocker, get_schema_from_api_fixture):
    # default return type is dataframe

    mocker.patch(
        polly_services.schema.schema_hlpr.__name__ + ".get_schema_from_api",
        return_value=get_schema_from_api_fixture,
    )

    omix_obj_test = omixatlas.OmixAtlas(token, env="testpolly")
    # ingestion_test_1
    repo_key_1 = "1654268055800"
    resp = omix_obj_test.get_schema(
        repo_key_1, ["datasets", "samples"], source="all", data_type="all"
    )
    assert isinstance(resp.datasets, pd.DataFrame)
    assert isinstance(resp.samples, pd.DataFrame)


def test_get_schema_with_valid_schema_level_values(
    mocker, get_schema_from_api_fixture_level_names
):
    # dataset, sample are valid schema lvl values
    # ingestion_test_1

    mocker.patch(
        polly_services.schema.schema_hlpr.__name__ + ".get_schema_from_api",
        return_value=get_schema_from_api_fixture_level_names,
    )

    repo_key_1 = "1654268055800"
    omix_obj_test = omixatlas.OmixAtlas(token, env="testpolly")
    resp = omix_obj_test.get_schema(
        repo_key_1, ["sample"], source="all", data_type="all"
    )
    assert isinstance(resp.sample, pd.DataFrame)


def test_get_schema_schema_level_param_empty_by_default_all_values(
    mocker, get_schema_from_api_fixture
):
    # neither valid table name or schema level value passed
    # should take all the table names
    # ingestion_test_1

    mocker.patch(
        polly_services.schema.schema_hlpr.__name__ + ".get_schema_from_api",
        return_value=get_schema_from_api_fixture,
    )

    repo_key_1 = "1654268055800"
    omix_obj_test = omixatlas.OmixAtlas(token, env="testpolly")
    resp = omix_obj_test.get_schema(repo_key_1, [], source="all", data_type="all")
    # will take all the table names present for this repo
    # for this repo 3 table names are there
    # datasets, samples, features
    # all three should be present in the schema
    assert resp.datasets is not None
    assert isinstance(resp.datasets, pd.DataFrame)

    assert resp.samples is not None
    assert isinstance(resp.samples, pd.DataFrame)


"""def test_get_schema_with_valid_schema_level_value_and_incorrect_data_type_value():
    # valid schema level sample with "single cell" as data_type
    # as data_type is only `all` -> there is no single_cell datatype in the schema
    # it should return error
    repo_key_2 = "sc_data_lake"
    omix_obj_test = omixatlas.OmixAtlas(token, env="testpolly")
    with pytest.raises(
        RequestException,
        match=r".*Datatype passed in the query param does not existfor this source: all. You can try these instead ['all']*",
    ):
        omix_obj_test.get_schema(
            repo_key_2, ["sample"], source="all", data_type="single_cell"
        )"""


def test_get_schema_with_valid_schema_table_value_return_type_dict(
    mocker, get_full_schema_payload_from_api_fixture
):
    # valid schema table value and return type dict
    # it should return dict in response

    mocker.patch(
        polly_services.schema.schema_hlpr.__name__
        + ".get_full_schema_payload_from_api",
        return_value=get_full_schema_payload_from_api_fixture,
    )

    omix_obj_test = omixatlas.OmixAtlas(token, env="testpolly")
    # ingestion_test_1
    repo_key_1 = "1654268055800"
    resp = omix_obj_test.get_schema(
        repo_key_1,
        ["datasets", "samples"],
        source="all",
        data_type="all",
        return_type="dict",
    )
    assert isinstance(resp.datasets, dict)
    assert isinstance(resp.samples, dict)


def test_get_schema_with_valid_schema_level_value_return_type_dict(
    mocker, get_full_schema_payload_from_api_fixture_valid_level_names
):
    # valid schema  value and return type dict
    # it should return dict in response

    mocker.patch(
        polly_services.schema.schema_hlpr.__name__
        + ".get_full_schema_payload_from_api",
        return_value=get_full_schema_payload_from_api_fixture_valid_level_names,
    )

    omix_obj_test = omixatlas.OmixAtlas(token, env="testpolly")
    # ingestion_test_1
    repo_key_1 = "1654268055800"
    resp = omix_obj_test.get_schema(
        repo_key_1, ["dataset"], source="all", data_type="all", return_type="dict"
    )
    assert isinstance(resp.dataset, dict)


# no need of mocking -> request will not go till the API
def test_get_schema_invalid_schema_level_value_passed():
    # wrong source passed
    # ingestion_test_1
    repo_key_2 = "1654268055800"
    omix_obj_test = omixatlas.OmixAtlas(token, env="testpolly")
    with pytest.raises(
        paramException,
        match=r".*schema_level input is incorrect. Use the query SHOW TABLES IN <repo_name>.*",
    ):
        omix_obj_test.get_schema(repo_key_2, ["abc"], source="all", data_type="all")


def test_get_schema_type_info():
    # returns the schema level based on schema type / table name
    # ingestion_test_1
    repo_key = "1654268055800"
    # table names in geo
    schema_level = ["datasets", "samples"]
    omix_obj_test = omixatlas.OmixAtlas(token, env="testpolly")
    res = polly_services.schema.schema_hlpr.get_schema_type_info(
        omix_obj_test, repo_key, schema_level, ""
    )

    assert isinstance(res, dict)
    assert res.get("datasets") == "files"
    assert res.get("samples") == "gct_metadata"
