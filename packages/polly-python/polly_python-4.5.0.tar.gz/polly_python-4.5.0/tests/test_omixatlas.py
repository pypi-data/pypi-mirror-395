from polly import omixatlas
import polly
from polly.auth import Polly
import os
from polly.errors import (
    RequestException,
    apiErrorException,
    InvalidPathException,
    paramException,
    InvalidParameterException,
    # RequestException,
)
import json
import pytest
import requests
import pandas as pd
from polly import constants as const
import test_constants as test_const
from polly.constants import BASE_TEST_FORMAT_CONSTANTS_URL
from polly.errors import error_handler
import polly_services
from polly_services.files import files_hlpr
from polly_services import polly_services_hlpr

# import polly.omixatlas_hlpr as omix_hlpr
from test_constants import (
    INGESTION_TEST_1_REPO_ID,
    MOCK_RESPONSE_DOWNLOAD_DATA,
    MOCKED_DICT_RESPONSE,
)

# from botocore.exceptions import ClientError


key = "POLLY_API_KEY"
token = os.getenv(key)

test_key = "TEST_POLLY_API_KEY"
testpolly_token = os.getenv(test_key)

dev_key = "DEV_POLLY_API_KEY"
devpolly_token = os.getenv(dev_key)


def test_obj_initialised():
    Polly.auth(token)
    assert omixatlas.OmixAtlas() is not None
    assert omixatlas.OmixAtlas(token) is not None
    assert Polly.get_session(token) is not None


def test_get_all_omixatlas(mocker):
    Polly.auth(token)
    obj = omixatlas.OmixAtlas()
    response = mocker.patch.object(obj.session, "get")
    response.return_value.status_code = 200
    response.return_value.json.return_value = MOCKED_DICT_RESPONSE
    assert type(obj.get_all_omixatlas()) is dict
    assert type(obj.get_all_omixatlas(query_api_version="v1")) is dict


def test_get_omixatlas(mocker):
    Polly.auth(token)
    obj = omixatlas.OmixAtlas(token)
    key = "geo"
    response = mocker.patch.object(obj.session, "get")
    response.return_value.status_code = 200
    response.return_value.json.return_value = MOCKED_DICT_RESPONSE
    assert type(obj._get_omixatlas(key)) is dict


def test_omixatlas_summary(mocker):
    Polly.auth(token)
    obj = omixatlas.OmixAtlas()
    key = "elucidata.liveromix_atlas"
    response = mocker.patch.object(obj.session, "get")
    response.return_value.status_code = 200
    response.return_value.json.return_value = MOCKED_DICT_RESPONSE
    assert type(obj.omixatlas_summary(key)) is dict
    assert type(obj.omixatlas_summary(key, query_api_version="v1")) is dict


def test_download_data(mocker):
    # mocking session response of {self.resource_url}/{repo_name}/download api call -> positive scenario
    obj = omixatlas.OmixAtlas(testpolly_token, env="testpolly")
    response = mocker.patch.object(obj.session, "get")
    response.return_value.status_code = 200
    response.return_value.json.return_value = MOCK_RESPONSE_DOWNLOAD_DATA
    result = obj.download_data(
        INGESTION_TEST_1_REPO_ID, "Dummy_dataset_id", internal_call=True
    )
    assert result["data"]["attributes"]["download_url"] is not None

    # mocking session response of {self.resource_url}/{repo_name}/download api call -> negative scenario
    obj = omixatlas.OmixAtlas(testpolly_token, env="testpolly")
    response = mocker.patch.object(obj.session, "get")
    response.return_value.status_code = 403
    response.return_value.json.return_value = test_const.MOCK_403_ACCESS_DENIED_RESPONSE
    with pytest.raises(
        RequestException,
        match=r"('Access denied', 'Access denied for requested resource')",
    ):
        obj.download_data(
            INGESTION_TEST_1_REPO_ID, "Dummy_dataset_id", internal_call=True
        )

    # request exception tests - when providing incorrect repo_key, incorrect dataset_id
    invalid_workspace_id = "test_repo"
    obj = omixatlas.OmixAtlas(testpolly_token, env="testpolly")
    response = mocker.patch.object(obj.session, "get")
    response.return_value.status_code = 403
    response.return_value.json.return_value = test_const.MOCK_REPO_NOT_FOUND_RESPONSE
    with pytest.raises(
        RequestException,
        match=r"'Data not found not found', 'Repository with repo key * not found'",
    ):
        obj.download_data(invalid_workspace_id, "Dummy_dataset_id", internal_call=True)


def test_download_data_deprecation_message(mocker):
    obj = omixatlas.OmixAtlas(testpolly_token, env="testpolly")
    response = mocker.patch.object(obj.session, "get")
    response.return_value.status_code = 200
    response.return_value.json.return_value = MOCK_RESPONSE_DOWNLOAD_DATA
    obj.download_data(INGESTION_TEST_1_REPO_ID, "Dummy_dataset_id")
    with pytest.warns(Warning) as record:
        obj.download_data(INGESTION_TEST_1_REPO_ID, "Dummy_dataset_id")
        if not record:
            pytest.fail("Expected a warning!")


def test_add_dataset_str_type_source_folder_path():
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    # ingestion_test_1
    repo_id = "1654268055800"
    # source folder path is in str
    # it should in dict
    source_folder_path = "<ingestion file_path>"
    with pytest.raises(
        paramException,
        match=r".* source_folder_path should be a dict with valid data and metadata path values .*",
    ):
        omix_obj.add_datasets(repo_id, source_folder_path)


def test_add_dataset_dict_type_source_folder_path_no_metadata_key():
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    repo_id = "1654268055800"
    # <ingestion_data_file_path>
    source_folder_path_data = os.getcwd()
    source_folder_path = {"data": source_folder_path_data}
    with pytest.raises(
        paramException,
        match=r".* does not have `metadata` path. Format the source_folder_path_dict .*",
    ):
        omix_obj.add_datasets(repo_id, source_folder_path)


def test_add_dataset_dict_type_source_folder_path_no_data_key():
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    repo_id = "1654268055800"
    # <ingestion_metadata_file_path>
    source_folder_path_metadata = os.getcwd()
    source_folder_path = {"metadata": source_folder_path_metadata}
    with pytest.raises(
        paramException,
        match=r".* does not have `data` path. Format the source_folder_path_dict like this .*",
    ):
        omix_obj.add_datasets(repo_id, source_folder_path)


def test_add_dataset_dict_type_source_folder_path_wrong_data_path():
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    # ingestion_test_1
    repo_id = "1654268055800"
    # <ingestion_data_file_path>
    source_folder_path_data = f"{os.getcwd()}/data_val"
    source_folder_path_metadata = f"{os.getcwd()}/metadata_val"
    source_folder_path = {
        "data": source_folder_path_data,
        "metadata": source_folder_path_metadata,
    }
    with pytest.raises(
        paramException,
        match=r".* `data` path passed is not found. Please pass the correct path .*",
    ):
        omix_obj.add_datasets(repo_id, source_folder_path)


def test_add_dataset_missing_metadata_file():
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    # ingestion_test_1
    repo_id = "1654268055800"
    base_add_datatest_test_file_path = BASE_TEST_FORMAT_CONSTANTS_URL

    # creating directory
    parent_dir = os.getcwd()
    data_dir = "data_file"
    metadata_dir = "metadata_file"
    data_path = os.path.join(parent_dir, data_dir)
    metadata_path = os.path.join(parent_dir, metadata_dir)

    # data directory
    if not os.path.isdir(data_path):
        os.makedirs(data_path)
    # metadata directory
    if not os.path.isdir(metadata_path):
        os.makedirs(metadata_path)

    # data file 1
    data_file_1 = f"{base_add_datatest_test_file_path}/data_file/tcga_LIHC_Copy_Number_Segment_TCGA-FV-A3R2-01A.gct"
    data_file_2 = f"{base_add_datatest_test_file_path}/data_file/tcga_LIHC_Copy_Number_Segment_TCGA-FV-A3R3-01A.gct"
    response_1 = requests.get(data_file_1)
    error_handler(response_1)
    response_2 = requests.get(data_file_2)
    error_handler(response_2)

    file_1_name = "tcga_LIHC_Copy_Number_Segment_TCGA-FV-A3R2-01A.gct"
    file_2_name = "tcga_LIHC_Copy_Number_Segment_TCGA-FV-A3R3-01A.gct"

    # creating files in data path
    with open(os.path.join(data_path, file_1_name), "w") as file_1:
        file_1_content = response_1.text
        file_1.write(file_1_content)

    with open(os.path.join(data_path, file_2_name), "w") as file_2:
        file_2_content = response_2.text
        file_2.write(file_2_content)

    metadata_file_1 = f"{base_add_datatest_test_file_path}/metadata_file/tcga_LIHC_Copy_Number_Segment_TCGA-FV-A3R2-01A.jpco"

    metadata_file_1_name = "tcga_LIHC_Copy_Number_Segment_TCGA-FV-A3R2-01A.jpco"

    metadata_resp_1 = requests.get(metadata_file_1)
    error_handler(metadata_resp_1)

    # creating files in metadata path
    with open(os.path.join(metadata_path, metadata_file_1_name), "w") as file_3:
        metadata_1_content = metadata_resp_1.text
        file_3.write(metadata_1_content)

    source_folder_path = {"data": data_path, "metadata": metadata_path}

    with pytest.raises(
        paramException,
        match=r".* No metadata for these data files .*",
    ):
        omix_obj.add_datasets(repo_id, source_folder_path)


# mock the list folder API
@pytest.fixture()
def list_folders_function_mock_fixture(mocker):
    Polly.auth(testpolly_token, env="testpolly")
    nobj = omixatlas.OmixAtlas()
    # ingestion_test_1
    repo_id = test_const.INGESTION_TEST_1_REPO_ID

    fake_json = {
        "data": {"id": "", "type": "file_paths", "attributes": {"file_paths": []}}
    }
    response = mocker.patch.object(nobj.session, "get")
    response.return_value.status_code = 200
    response.return_value.json.return_value = fake_json
    # random dataset_id -> as the api is mocked
    # will give same result
    dataset_id = "abcd"

    result = files_hlpr.check_destination_folder_for_dataset_id(
        nobj, dataset_id, repo_id
    )
    return result


def test_add_dataset_wrong_priority_value():
    Polly.auth(token)
    omix_obj = omixatlas.OmixAtlas()
    # ingestion_test_1
    repo_id = "1654268055800"
    source_folder_path_data = f"{os.getcwd()}/data_file"
    source_folder_path_metadata = f"{os.getcwd()}/metadata_file"
    source_folder_path = {
        "data": source_folder_path_data,
        "metadata": source_folder_path_metadata,
    }
    priority = "super_high"
    with pytest.raises(
        paramException,
        match=r".*`priority` should be a string. Only 3 values are allowed i.e. `low`, `medium`, `high`.*",
    ):
        omix_obj.add_datasets(repo_id, source_folder_path, priority)


def test_add_dataset_incorrect_priority_value_format():
    Polly.auth(token)
    omix_obj = omixatlas.OmixAtlas()
    # ingestion_test_1
    repo_id = "1654268055800"
    source_folder_path_data = f"{os.getcwd()}/data_file"
    source_folder_path_metadata = f"{os.getcwd()}/metadata_file"
    source_folder_path = {
        "data": source_folder_path_data,
        "metadata": source_folder_path_metadata,
    }
    priority = ["super_high"]
    with pytest.raises(
        paramException,
        match=r"`priority` should be a string. Only 3 values are allowed i.e. `low`, `medium`, `high`",
    ):
        omix_obj.add_datasets(repo_id, source_folder_path, priority)


def test_add_dataset_data_file_with_wrong_extension():
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    # ingestion_test_1
    repo_id = "1654268055800"

    file_3_name = "incorrect_ext_data_file.txt"

    # creating directory
    parent_dir = os.getcwd()
    data_dir = "data_file_wrong_ext"
    metadata_dir = "metadata_file_wrong_ext"
    data_path = os.path.join(parent_dir, data_dir)
    metadata_path = os.path.join(parent_dir, metadata_dir)

    # data directory
    if not os.path.isdir(data_path):
        os.makedirs(data_path)
    # metadata directory
    if not os.path.isdir(metadata_path):
        os.makedirs(metadata_path)

    # creating files in data path
    with open(os.path.join(data_path, file_3_name), "w") as file_3:
        file_3_content = "wrong extension data file"
        file_3.write(file_3_content)

    source_folder_path = {"data": data_path, "metadata": metadata_path}

    with pytest.raises(
        paramException,
        match=r".* File format for file .* invalid.It can be =>.*",
    ):
        omix_obj.add_datasets(repo_id, source_folder_path)


def test_add_dataset_metadata_file_with_wrong_extension():
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    # ingestion_test_1
    repo_id = "1654268055800"

    metadata_2_name = "incorrect_ext_data_file.txt"

    # creating directory
    parent_dir = os.getcwd()
    data_dir = "data_file_wrong_ext"
    metadata_dir = "metadata_file_wrong_ext"
    data_path = os.path.join(parent_dir, data_dir)
    metadata_path = os.path.join(parent_dir, metadata_dir)

    # data directory
    if not os.path.isdir(data_path):
        os.makedirs(data_path)
    # metadata directory
    if not os.path.isdir(metadata_path):
        os.makedirs(metadata_path)

    # creating files in data path
    with open(os.path.join(metadata_path, metadata_2_name), "w") as file_3:
        file_3_content = "wrong extension data file"
        file_3.write(file_3_content)

    source_folder_path = {"data": data_path, "metadata": metadata_path}

    with pytest.raises(
        paramException,
        match=r".* File format for file .* invalid.It can be =>.*",
    ):
        omix_obj.add_datasets(repo_id, source_folder_path)


def test_delete_dataset_wrong_format_of_dataset_id():
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    # ingestion_test_1
    repo_id = "1654268055800"
    dataset_ids = "tcga_LIHC_Copy_Number_Segment_TCGA-FV-A3R3-01A"

    with pytest.raises(
        paramException, match=r".* dataset_ids should be list of strings.*"
    ):
        omix_obj.delete_datasets(repo_id, dataset_ids)


def test_devpolly_login():
    Polly.auth(devpolly_token, env="devpolly")
    assert omixatlas.OmixAtlas() is not None
    assert omixatlas.OmixAtlas(devpolly_token, env="devpolly") is not None


# error message not properly put after shifting to API key by cloud platform team
# def test_delete_unauthorized_error_wrong_token():
#     dev_token = "abcdefgh"
#     Polly.auth(dev_token, env="testpolly")
#     with pytest.raises(UnauthorizedException, match=r"Expired or Invalid Token"):
#         omixatlas.OmixAtlas()


def test_delete_empty_repo_id():
    Polly.auth(devpolly_token, env="devpolly")
    omix_obj = omixatlas.OmixAtlas()
    repo_id = ""
    dataset_ids = ["GSE100009_GPL11154"]

    with pytest.raises(paramException, match=r".*repo_id should not be empty.*"):
        omix_obj.delete_datasets(repo_id, dataset_ids)


@pytest.fixture()
def get_query_metadata_fixture():
    """Get success response for query_metadata enpoint from github"""
    base_polly_py_test_url = test_const.POLLY_PY_TEST_FILES_URL

    data_file = f"{base_polly_py_test_url}/query_metadata_success_response.json"
    data = requests.get(data_file)
    error_handler(data)
    return data


@pytest.fixture()
def get_download_url_fixture():
    """Get success response of dummy urls from github"""
    base_polly_py_test_url = test_const.POLLY_PY_TEST_FILES_URL

    data_file = f"{base_polly_py_test_url}/download_urls_response.json"
    data = requests.get(data_file)
    error_handler(data)
    return data


def test_query_metadata(mocker):
    """
    Mock function for query_metadata().
    """
    Polly.auth(token)
    obj = omixatlas.OmixAtlas()
    query = test_const.SAMPLE_QUERY
    mocker.patch(
        polly.omixatlas.__name__ + ".OmixAtlas._get_query_id",
        return_value="query_id",
    )
    mocker.patch(
        polly.omixatlas.__name__ + ".OmixAtlas._process_query_to_completion",
        return_value=pd.DataFrame(),
    )
    assert type(obj.query_metadata(query)) is pd.DataFrame


def test_query_metadata_iterator(mocker, generator_function):
    """
    Mock function for query_metadata_iterator().
    """
    Polly.auth(token)
    query = test_const.SAMPLE_QUERY
    mocker.patch(
        polly.omixatlas.__name__ + ".OmixAtlas._get_query_id",
        return_value="query_id",
    )
    mocker.patch(
        polly.omixatlas.__name__ + ".OmixAtlas._process_query_to_completion",
        return_value=generator_function,
    )
    obj = omixatlas.OmixAtlas(token)
    gen = obj.query_metadata(query)
    assert gen is not None


@pytest.fixture()
def generator_function():
    """
    A dummy generator function for mocking a generator
    """
    dummy_list = [{"key": "value"}]
    for i in dummy_list:
        yield i


def test_process_query_to_completion_iterator(
    mocker, generator_function, get_query_metadata_fixture
):
    """
    Mock function for _process_query_to_completion() with iterator.
    """
    Polly.auth(token)
    obj = omixatlas.OmixAtlas()
    mocked_response = get_query_metadata_fixture
    response = mocker.patch.object(obj.session, "get")
    response.return_value.status_code = 200
    response.return_value = mocked_response
    mocker.patch(
        polly.omixatlas.__name__ + ".OmixAtlas._fetch_results_as_file",
        return_value=generator_function,
    )
    query_id = "query_id"
    iterator_function = True
    gen = obj._process_query_to_completion(query_id, iterator_function)
    assert gen is not None


def test_process_query_to_completion(mocker, get_query_metadata_fixture):
    """
    Mock function for _process_query_to_completion() without iterator.
    """
    Polly.auth(token)
    obj = omixatlas.OmixAtlas()
    mocked_response = get_query_metadata_fixture
    response = mocker.patch.object(obj.session, "get")
    response.return_value.status_code = 200
    response.return_value = mocked_response
    mocker.patch(
        polly.omixatlas.__name__ + ".OmixAtlas._fetch_results_as_file",
        return_value=pd.DataFrame(),
    )
    query_id = "query_id"
    iterator_function = False
    df = obj._process_query_to_completion(query_id, iterator_function)
    assert type(df) is pd.DataFrame


def test_fetch_results_as_file(mocker, get_download_url_fixture):
    """
    Mock function for _fetch_results_as_file() without iterator.
    """
    Polly.auth(token)
    obj = omixatlas.OmixAtlas()
    mocked_response = get_download_url_fixture
    response = mocker.patch.object(obj.session, "get")
    response.return_value.status_code = 200
    response.return_value = mocked_response
    mocker.patch(
        polly.omixatlas.__name__ + ".OmixAtlas._extract_results_from_download_urls",
        return_value=pd.DataFrame(),
    )
    query_id = "query_id"
    iterator_function = False
    df = obj._fetch_results_as_file(query_id, iterator_function)
    assert type(df) is pd.DataFrame


def test_fetch_results_as_file_iterator(
    mocker, generator_function, get_download_url_fixture
):
    """
    Mock function for _fetch_results_as_file() with iterator.
    """
    Polly.auth(token)
    obj = omixatlas.OmixAtlas()
    mocked_response = get_download_url_fixture
    response = mocker.patch.object(obj.session, "get")
    response.return_value.status_code = 200
    response.return_value = mocked_response
    mocker.patch(
        polly.omixatlas.__name__ + ".OmixAtlas._extract_results_from_download_urls",
        return_value=generator_function,
    )
    query_id = "query_id"
    iterator_function = True
    gen = obj._fetch_results_as_file(query_id, iterator_function)
    assert gen is not None


# Test 1 -> pass no parameters to update -> will raise an error
def test_update_oa_no_params_passed():
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    # ingestion_test_1 repo
    repo_id = "1654268055800"
    with pytest.raises(
        paramException,
        match=r".* parameters passed to update, please pass at least one of the following .*",
    ):
        omix_obj.update(repo_key=repo_id)


# Test 2 -> wrong description type
def test_update_oa_wrong_description_type():
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    # ingestion_test_1 repo
    repo_id = "1654268055800"
    with pytest.raises(
        paramException,
        match=r".* should be a string.*",
    ):
        omix_obj.update(
            repo_key=repo_id, description=["Created Omixatlas to test description"]
        )


# Test 3 -> wrong display name type
def test_update_oa_wrong_display_name_type():
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    # ingestion_test_1 repo
    repo_id = "1654268055800"
    with pytest.raises(
        paramException,
        match=r".* should be a string.*",
    ):
        omix_obj.update(repo_key=repo_id, display_name=1234)


@pytest.fixture()
def update_default_patch_req_fixture():
    # put the response in a json
    # and do json.loads to load it into a dictionary
    base_polly_py_test_url = test_const.POLLY_PY_TEST_FILES_URL
    parent_dir = os.getcwd()
    test_dir = "tests"
    test_path = os.path.join(parent_dir, test_dir)
    if not os.path.isdir(test_path):
        os.makedirs(test_path)

    create_response_file = f"{base_polly_py_test_url}/update_pos_response.json"
    create_post_response_json = requests.get(create_response_file)

    error_handler(create_post_response_json)
    fake_create_post_response_json_dict = json.loads(create_post_response_json.text)
    return fake_create_post_response_json_dict


# Test 4 -> positive case -> update description
def test_update_function_by_updating_description(
    mocker, update_default_patch_req_fixture
):
    # updated description value
    description_val = "updated description of lib repo dev v1"
    # ingestion_test_1
    repo_key_val = "1654268055800"
    Polly.auth(testpolly_token, env="testpolly")
    nobj = omixatlas.OmixAtlas()
    # mocked response with status and no specific value
    # as no specific response is mocked -> generic message will be printed
    response = mocker.patch.object(nobj.session, "patch")
    # http create response code -> 201
    response.return_value.status_code = 200
    response.return_value.json.return_value = update_default_patch_req_fixture

    res = nobj.update(repo_key=repo_key_val, description=description_val)

    description_value = res.iloc[0, 4]
    assert description_value == description_val


# create omixatlas tests
def test_create_oa_wrong_category_value():
    # Passing wrong value of category -> will throw error
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    with pytest.raises(
        paramException,
        match=r".* should be a string and its value must be one of .*",
    ):
        omix_obj.create(
            "omix_category_test_13",
            "Created Omixatlas to test Category",
            category="test",
        )


def test_create_oa_wrong_description_type():
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    with pytest.raises(
        paramException,
        match=r".* should be a string.*",
    ):
        omix_obj.create(
            "omix_category_test_13", ["Created Omixatlas to test description"]
        )


def test_create_oa_wrong_display_name_type():
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    with pytest.raises(
        paramException,
        match=r".* should be a string.*",
    ):
        omix_obj.create(1234, "Created Omixatlas to test description")


def test_create_oa_wrong_image_url_type():
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    with pytest.raises(
        paramException,
        match=r".* should be a string.*",
    ):
        omix_obj.create(
            "omix_desc_test_12",
            "Created Omixatlas to test description",
            image_url=["/a/c/img.png"],
        )


@pytest.fixture()
def create_default_param_res_fixture_df():
    Polly.auth(testpolly_token, env="testpolly")
    res_dict = {}
    res_dict["Repository Id"] = "1684738195734"
    res_dict["Repository Name"] = "doing_test_for_mocking_v5"
    res_dict["Category"] = "private"
    res_dict["Display Name"] = "doing_test_for_mocking_v5"
    res_dict["Description"] = "testing locally create for mocking v5"
    df = pd.DataFrame([res_dict])
    return df


@pytest.fixture()
def create_default_post_req_fixture():
    # put the response in a json
    # and do json.loads to load it into a dictionary
    base_polly_py_test_url = test_const.POLLY_PY_TEST_FILES_URL
    parent_dir = os.getcwd()
    test_dir = "tests"
    test_path = os.path.join(parent_dir, test_dir)
    if not os.path.isdir(test_path):
        os.makedirs(test_path)

    create_response_file = f"{base_polly_py_test_url}/create_pos_response.json"
    create_post_response_json = requests.get(create_response_file)

    error_handler(create_post_response_json)
    fake_create_post_response_json_dict = json.loads(create_post_response_json.text)
    return fake_create_post_response_json_dict


def test_create_default_params(
    mocker, create_default_param_res_fixture_df, create_default_post_req_fixture
):
    # then mocking the response of PATCH API CALL for Update Schema
    Polly.auth(testpolly_token, env="testpolly")
    nobj = omixatlas.OmixAtlas()
    # mocked response with status and no specific value
    # as no specific response is mocked -> generic message will be printed
    response = mocker.patch.object(nobj.session, "post")
    # http create response code -> 201
    response.return_value.status_code = 201
    response.return_value.json.return_value = create_default_post_req_fixture

    # create default params
    display_name = "doing_test_for_mocking_v5"
    description = "testing locally create for mocking v5"

    res = nobj.create(display_name, description)

    pd.testing.assert_frame_equal(res, create_default_param_res_fixture_df)


@pytest.fixture()
def get_ingestion_test_1_fixture():
    """Get ingestion_test_1 from github and store it in local"""
    base_polly_py_test_url = test_const.POLLY_PY_TEST_FILES_URL
    parent_dir = os.getcwd()
    test_dir = "tests"
    test_path = os.path.join(parent_dir, test_dir)
    if not os.path.isdir(test_path):
        os.makedirs(test_path)

    ingestion_test_1_file = f"{base_polly_py_test_url}/ingestion_test_1.json"
    ingestion_test_1 = requests.get(ingestion_test_1_file)
    error_handler(ingestion_test_1)
    mock_json = json.loads(ingestion_test_1.text)
    # with open(os.path.join(test_path, ingestion_test_1_file_name), "w") as file_1:
    #     file_1_content = ingestion_test_1.text
    #     file_1.write(file_1_content)

    # with open(f"{test_path}/{ingestion_test_1_file_name}") as ingestion_test_1_file:
    #     #fake_json = ingestion_test_1_file.read()
    #     fake_json = json.load(ingestion_test_1_file)

    return mock_json


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
def get_omixatlas_mock_fixture_polly_services(mocker, get_ingestion_test_1_fixture):
    Polly.auth(testpolly_token, env="testpolly")
    nobj = omixatlas.OmixAtlas()
    # ingestion_test_1
    repo_id = test_const.INGESTION_TEST_1_REPO_ID
    fake_json = get_ingestion_test_1_fixture
    response = mocker.patch.object(nobj.session, "get")
    response.return_value.status_code = 200
    response.return_value.json.return_value = fake_json

    result = polly_services_hlpr.get_omixatlas(nobj, repo_id)
    return result


def test_validate_schema_function_empty_repo_id(
    mocker, get_omixatlas_mock_fixture_polly_services
):
    # mocking get_omixatlas call inside polly_services_hlpr that is called in
    # validate_schema in the schema class in polly_services
    mocker.patch(
        polly_services.polly_services_hlpr.__name__ + ".get_omixatlas",
        return_value=get_omixatlas_mock_fixture_polly_services,
    )

    # load data
    response = requests.get(const.SCHEMA_VALIDATION.get("empty_repo_id"))
    error_handler(response)
    test_data = json.loads(response.text)
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    # if repo_id is empty, it will not match payload identifier
    with pytest.raises(
        paramException,
        match=r"Value of repo_id key in the schema payload dict is not valid repo_id.*",
    ):
        omix_obj.validate_schema(test_data)


def test_validate_schema_function_missing_repo_id(
    mocker, get_omixatlas_mock_fixture_polly_services
):
    mocker.patch(
        polly_services.polly_services_hlpr.__name__ + ".get_omixatlas",
        return_value=get_omixatlas_mock_fixture_polly_services,
    )

    # load data
    response = requests.get(const.SCHEMA_VALIDATION.get("missing_repo_id"))
    error_handler(response)
    test_data = json.loads(response.text)
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    with pytest.raises(
        paramException,
        match=r"schema_dict not in correct format, repo_id key not present.*",
    ):
        omix_obj.validate_schema(test_data)


def test_validate_schema_function_missing_schema_key(
    mocker, get_omixatlas_mock_fixture_polly_services
):
    mocker.patch(
        polly_services.polly_services_hlpr.__name__ + ".get_omixatlas",
        return_value=get_omixatlas_mock_fixture_polly_services,
    )

    # load data
    response = requests.get(const.SCHEMA_VALIDATION.get("missing_schema_key"))
    error_handler(response)
    test_data = json.loads(response.text)
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    with pytest.raises(
        paramException,
        match=r"schema_dict not in correct format, schema key not present*",
    ):
        omix_obj.validate_schema(test_data)


def test_validate_schema_repo_id_and_id_different_in_body(
    mocker, get_omixatlas_mock_fixture_polly_services
):
    mocker.patch(
        polly_services.polly_services_hlpr.__name__ + ".get_omixatlas",
        return_value=get_omixatlas_mock_fixture_polly_services,
    )

    # load data
    response = requests.get(const.SCHEMA_VALIDATION.get("repo_id_and_id_diff"))
    error_handler(response)
    test_data = json.loads(response.text)
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    with pytest.raises(
        paramException,
        match=r"Value of repo_id key and id key is not same in the payload*",
    ):
        omix_obj.validate_schema(test_data)


"""def test_validate_schema_function_wrong_repo_id():
    # load data
    response = requests.get(const.SCHEMA_VALIDATION.get("wrong_repo_id"))
    error_handler(response)
    test_data = json.loads(response.text)
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    with pytest.raises(
        RequestException,
        match=r".*No repository for identifier.*",
    ):
        omix_obj.validate_schema(test_data)"""


def test_validate_schema_function_field_name_capital(
    mocker, get_omixatlas_mock_fixture_polly_services
):
    mocker.patch(
        polly_services.polly_services_hlpr.__name__ + ".get_omixatlas",
        return_value=get_omixatlas_mock_fixture_polly_services,
    )

    # load data
    response = requests.get(const.SCHEMA_VALIDATION.get("field_name_cap"))
    error_handler(response)
    test_data = json.loads(response.text)
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()

    res_df = omix_obj.validate_schema(test_data)
    msg_val = res_df.iloc[2]["message"]

    assert isinstance(res_df, pd.DataFrame)
    assert "Lowercase only, Start with alphabets" in msg_val


def test_validate_schema_function_field_name_having_underscore(
    mocker, get_omixatlas_mock_fixture_polly_services
):
    mocker.patch(
        polly_services.polly_services_hlpr.__name__ + ".get_omixatlas",
        return_value=get_omixatlas_mock_fixture_polly_services,
    )

    response = requests.get(const.SCHEMA_VALIDATION.get("field_name_underscore"))
    error_handler(response)
    test_data = json.loads(response.text)
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()

    res_df = omix_obj.validate_schema(test_data)
    msg_val = res_df.iloc[0]["message"]

    assert isinstance(res_df, pd.DataFrame)
    assert "Cannot include special characters except `_`" in msg_val


def test_validate_schema_function_field_name_having_resv_keywords(
    mocker, get_omixatlas_mock_fixture_polly_services
):
    mocker.patch(
        polly_services.polly_services_hlpr.__name__ + ".get_omixatlas",
        return_value=get_omixatlas_mock_fixture_polly_services,
    )

    response = requests.get(const.SCHEMA_VALIDATION.get("field_name_resv_keyword"))
    error_handler(response)
    test_data = json.loads(response.text)
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()

    res_df = omix_obj.validate_schema(test_data)
    msg_val = res_df.iloc[2]["message"]

    assert isinstance(res_df, pd.DataFrame)
    assert "Cannot be SQL reserved DDL and DML keywords" in msg_val


def test_validate_schema_function_field_name_having_original_name_empty(
    mocker, get_omixatlas_mock_fixture_polly_services
):
    mocker.patch(
        polly_services.polly_services_hlpr.__name__ + ".get_omixatlas",
        return_value=get_omixatlas_mock_fixture_polly_services,
    )

    response = requests.get(const.SCHEMA_VALIDATION.get("original_name_empty"))
    error_handler(response)
    test_data = json.loads(response.text)
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()

    res_df = omix_obj.validate_schema(test_data)
    msg_val = res_df.iloc[0]["message"]

    assert isinstance(res_df, pd.DataFrame)
    assert "String should have at least 1 character" in msg_val


def test_validate_schema_function_field_name_having_original_name_greater_than_50_chars(
    mocker, get_omixatlas_mock_fixture_polly_services
):
    mocker.patch(
        polly_services.polly_services_hlpr.__name__ + ".get_omixatlas",
        return_value=get_omixatlas_mock_fixture_polly_services,
    )

    response = requests.get(const.SCHEMA_VALIDATION.get("original_name_grtr_50"))
    error_handler(response)
    test_data = json.loads(response.text)
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()

    res_df = omix_obj.validate_schema(test_data)
    msg_val = res_df.iloc[0]["message"]

    assert isinstance(res_df, pd.DataFrame)
    assert "String should have at most 50 characters" in msg_val


def test_validate_schema_function_field_name_having_type_is_not_supported(
    mocker, get_omixatlas_mock_fixture_polly_services
):
    mocker.patch(
        polly_services.polly_services_hlpr.__name__ + ".get_omixatlas",
        return_value=get_omixatlas_mock_fixture_polly_services,
    )

    response = requests.get(const.SCHEMA_VALIDATION.get("type_cosco"))
    error_handler(response)
    test_data = json.loads(response.text)
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()

    res_df = omix_obj.validate_schema(test_data)
    msg_val = res_df.iloc[0]["message"]

    assert isinstance(res_df, pd.DataFrame)
    assert (
        "Input should be 'boolean', 'integer', 'float', 'text' or 'object'" in msg_val
    )


def test_validate_schema_function_field_name_having_is_array_string(
    mocker, get_omixatlas_mock_fixture_polly_services
):
    mocker.patch(
        polly_services.polly_services_hlpr.__name__ + ".get_omixatlas",
        return_value=get_omixatlas_mock_fixture_polly_services,
    )

    response = requests.get(const.SCHEMA_VALIDATION.get("is_arr_str"))
    error_handler(response)
    test_data = json.loads(response.text)
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()

    res_df = omix_obj.validate_schema(test_data)
    msg_val = res_df.iloc[0]["message"]

    assert isinstance(res_df, pd.DataFrame)
    assert "Input should be a valid boolean" in msg_val


def test_validate_schema_function_field_name_having_is_keyword_string(
    mocker, get_omixatlas_mock_fixture_polly_services
):
    mocker.patch(
        polly_services.polly_services_hlpr.__name__ + ".get_omixatlas",
        return_value=get_omixatlas_mock_fixture_polly_services,
    )

    response = requests.get(const.SCHEMA_VALIDATION.get("is_keyword_str"))
    error_handler(response)
    test_data = json.loads(response.text)
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()

    res_df = omix_obj.validate_schema(test_data)
    msg_val = res_df.iloc[0]["message"]
    assert isinstance(res_df, pd.DataFrame)
    assert "Input should be a valid boolean" in msg_val


def test_validate_schema_function_field_name_having_filter_size_less(
    mocker, get_omixatlas_mock_fixture_polly_services
):
    mocker.patch(
        polly_services.polly_services_hlpr.__name__ + ".get_omixatlas",
        return_value=get_omixatlas_mock_fixture_polly_services,
    )

    response = requests.get(const.SCHEMA_VALIDATION.get("filter_size_less"))
    error_handler(response)
    test_data = json.loads(response.text)
    print(test_data)
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()

    res_df = omix_obj.validate_schema(test_data)
    msg_val = res_df.iloc[0]["message"]
    assert isinstance(res_df, pd.DataFrame)
    assert "Input should be greater than or equal to 1" in msg_val


def test_validate_schema_function_field_name_having_filter_size_greater(
    mocker, get_omixatlas_mock_fixture_polly_services
):
    mocker.patch(
        polly_services.polly_services_hlpr.__name__ + ".get_omixatlas",
        return_value=get_omixatlas_mock_fixture_polly_services,
    )

    response = requests.get(const.SCHEMA_VALIDATION.get("filter_size_greater"))
    error_handler(response)
    test_data = json.loads(response.text)
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()

    res_df = omix_obj.validate_schema(test_data)
    msg_val = res_df.iloc[0]["message"]
    assert isinstance(res_df, pd.DataFrame)
    assert "Input should be less than or equal to 3000" in msg_val


def test_validate_schema_function_field_name_having_display_name_empty(
    mocker, get_omixatlas_mock_fixture_polly_services
):
    mocker.patch(
        polly_services.polly_services_hlpr.__name__ + ".get_omixatlas",
        return_value=get_omixatlas_mock_fixture_polly_services,
    )

    response = requests.get(const.SCHEMA_VALIDATION.get("display_name_empty"))
    error_handler(response)
    test_data = json.loads(response.text)
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()

    res_df = omix_obj.validate_schema(test_data)
    loc = res_df.iloc[0]["attribute"]
    msg_val = res_df.iloc[0]["message"]
    assert isinstance(res_df, pd.DataFrame)
    assert "display_name" in loc
    assert "String should have at least 1 character" in msg_val


def test_validate_schema_function_field_name_having_display_name_greater(
    mocker, get_omixatlas_mock_fixture_polly_services
):
    mocker.patch(
        polly_services.polly_services_hlpr.__name__ + ".get_omixatlas",
        return_value=get_omixatlas_mock_fixture_polly_services,
    )

    response = requests.get(const.SCHEMA_VALIDATION.get("display_name_grtr_50"))
    error_handler(response)
    test_data = json.loads(response.text)
    print(test_data)
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()

    res_df = omix_obj.validate_schema(test_data)
    loc = res_df.iloc[0]["attribute"]
    msg_val = res_df.iloc[0]["message"]
    assert isinstance(res_df, pd.DataFrame)
    assert "display_name" in loc
    assert "String should have at most 50 characters" in msg_val


def test_validate_schema_function_field_name_having_is_filter_is_keyword(
    mocker, get_omixatlas_mock_fixture_polly_services
):
    mocker.patch(
        polly_services.polly_services_hlpr.__name__ + ".get_omixatlas",
        return_value=get_omixatlas_mock_fixture_polly_services,
    )

    response = requests.get(const.SCHEMA_VALIDATION.get("is_keywrd_is_filter"))
    error_handler(response)
    test_data = json.loads(response.text)
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()

    res_df = omix_obj.validate_schema(test_data)
    msg_val = res_df.iloc[0]["message"]
    assert isinstance(res_df, pd.DataFrame)
    assert "is_keyword is False and is_filter is True" in msg_val


def test_validate_schema_function_field_name_having_is_filter_is_ontology(
    mocker, get_omixatlas_mock_fixture_polly_services
):
    mocker.patch(
        polly_services.polly_services_hlpr.__name__ + ".get_omixatlas",
        return_value=get_omixatlas_mock_fixture_polly_services,
    )

    response = requests.get(const.SCHEMA_VALIDATION.get("is_keywrd_is_ontology"))
    error_handler(response)
    test_data = json.loads(response.text)
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()

    res_df = omix_obj.validate_schema(test_data)
    msg_val = res_df.iloc[0]["message"]
    assert isinstance(res_df, pd.DataFrame)
    assert "is_filter is False and is_ontology is True" in msg_val


def test_validate_schema_function_positive_case(
    mocker, get_omixatlas_mock_fixture_polly_services
):
    mocker.patch(
        polly_services.polly_services_hlpr.__name__ + ".get_omixatlas",
        return_value=get_omixatlas_mock_fixture_polly_services,
    )

    response = requests.get(const.SCHEMA_VALIDATION.get("positive_case"))
    error_handler(response)
    test_data = json.loads(response.text)
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()

    res_df = omix_obj.validate_schema(test_data)
    res_df_len = len(res_df.index)

    assert res_df_len == 0


def test_validate_schema_function_having_original_name_int(
    mocker, get_omixatlas_mock_fixture_polly_services
):
    mocker.patch(
        polly_services.polly_services_hlpr.__name__ + ".get_omixatlas",
        return_value=get_omixatlas_mock_fixture_polly_services,
    )

    response = requests.get(const.SCHEMA_VALIDATION.get("original_name_int"))
    error_handler(response)
    test_data = json.loads(response.text)
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()

    res_df = omix_obj.validate_schema(test_data)
    msg_val = res_df.iloc[0]["message"]
    attribute_val = res_df.iloc[0]["attribute"]
    assert isinstance(res_df, pd.DataFrame)
    assert attribute_val == "original_name"
    assert "Input should be a valid string" in msg_val


def test_validate_schema_function_having_field_size_str(
    mocker, get_omixatlas_mock_fixture_polly_services
):
    mocker.patch(
        polly_services.polly_services_hlpr.__name__ + ".get_omixatlas",
        return_value=get_omixatlas_mock_fixture_polly_services,
    )

    response = requests.get(const.SCHEMA_VALIDATION.get("filter_size_str"))
    error_handler(response)
    test_data = json.loads(response.text)
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()

    res_df = omix_obj.validate_schema(test_data)
    msg_val = res_df.iloc[0]["message"]
    attribute_val = res_df.iloc[0]["attribute"]
    assert isinstance(res_df, pd.DataFrame)
    assert attribute_val == "filter_size"
    assert "Input should be a valid integer" in msg_val


# def test_download_metadata():
#     Polly.auth(token)
#     omix_obj = omixatlas.OmixAtlas()
#     repo_key = "geo"
#     dataset_id = "GSE10001_GPL6246"
#     assert omix_obj.download_metadata(repo_key, dataset_id, os.getcwd()) is None
#     file_path = f"{os.getcwd()}/{dataset_id}.json"
#     assert os.path.exists(file_path) is True
#     os.remove(file_path)


@pytest.fixture()
def get_ingestion_test_1_oa_summary_fixture():
    """Get ingestion_test_1 from github and store it in local"""
    base_polly_py_test_url = test_const.POLLY_PY_TEST_FILES_URL
    parent_dir = os.getcwd()
    test_dir = "tests"
    test_path = os.path.join(parent_dir, test_dir)
    if not os.path.isdir(test_path):
        os.makedirs(test_path)

    ingestion_test_1_os_summary_file = (
        f"{base_polly_py_test_url}/ingestion_test_1_oa_summary.json"
    )
    ingestion_test_1_oa_summary_response = requests.get(
        ingestion_test_1_os_summary_file
    )
    error_handler(ingestion_test_1_oa_summary_response)
    fake_json_ingestion_test_1_oa_summary = json.loads(
        ingestion_test_1_oa_summary_response.text
    )
    return fake_json_ingestion_test_1_oa_summary


@pytest.fixture()
def get_ingestion_test_1_dataset_metadata_fixture():
    """get dataset metadata for a dummy dataset(ingestion_test_1) from github and store in local"""
    base_polly_py_test_url = test_const.POLLY_PY_TEST_FILES_URL
    parent_dir = os.getcwd()
    test_dir = "tests"
    test_path = os.path.join(parent_dir, test_dir)
    if not os.path.isdir(test_path):
        os.makedirs(test_path)

    ingestion_test_1_dataset_metadata_file = (
        f"{base_polly_py_test_url}/ingestion_test_1_oa_metadata_dummy.json"
    )
    ingestion_test_1_dataset_metadata_response = requests.get(
        ingestion_test_1_dataset_metadata_file
    )
    error_handler(ingestion_test_1_dataset_metadata_response)
    fake_json_ingestion_test_1_oa_dataset_metadata = json.loads(
        ingestion_test_1_dataset_metadata_response.text
    )
    return fake_json_ingestion_test_1_oa_dataset_metadata


@pytest.fixture()
def get_omixatlas_summary_mock_fixture(mocker, get_ingestion_test_1_oa_summary_fixture):
    Polly.auth(testpolly_token, env="testpolly")
    nobj = omixatlas.OmixAtlas()
    # ingestion_test_1
    repo_id = test_const.INGESTION_TEST_1_REPO_ID
    fake_json = get_ingestion_test_1_oa_summary_fixture
    response = mocker.patch.object(nobj.session, "get")
    response.return_value.status_code = 200
    response.return_value.json.return_value = fake_json

    result = nobj.omixatlas_summary(repo_id)
    return result


def test_download_metadata(
    mocker,
    get_omixatlas_summary_mock_fixture,
    get_ingestion_test_1_dataset_metadata_fixture,
):
    valid_repo_key = "ingestion_test_1"
    valid_dataset_id = "GSE12345_GPL6789"
    invalid_dataset_id = "1234_6878"
    valid_path = os.getcwd()
    invalid_repo_key_type = 1234
    invalid_dataset_id_type = 1234
    invalid_path = "some_path/"
    invalid_path_type = {"path": os.getcwd()}
    # mocking response of omixatlas_summary when correct repo_id, dataset_id and path has been provided.
    mocker.patch(
        polly.omixatlas.__name__ + ".OmixAtlas.omixatlas_summary",
        return_value=get_omixatlas_summary_mock_fixture,
    )
    # mocking response of get_metadata when correct args are passed
    # mock_response_oa_get_metadata = json.loads(mock_response_oa_get_metadata_str)
    mocker.patch(
        polly.helpers.__name__ + ".get_metadata",
        return_value=get_ingestion_test_1_dataset_metadata_fixture,
    )

    omix_obj = omixatlas.OmixAtlas(testpolly_token, env="testpolly")
    # parameter exception checks
    with pytest.raises(
        InvalidParameterException,
        match=r"Empty or Invalid Parameters = .*",
    ):
        omix_obj.download_metadata(invalid_repo_key_type, valid_dataset_id, valid_path)
    with pytest.raises(
        InvalidParameterException,
        match=r"Empty or Invalid Parameters = .*",
    ):
        omix_obj.download_metadata(valid_repo_key, invalid_dataset_id_type, valid_path)
    with pytest.raises(
        InvalidParameterException,
        match=r"Empty or Invalid Parameters = .*",
    ):
        omix_obj.download_metadata(valid_repo_key, valid_dataset_id, invalid_path_type)
    with pytest.raises(
        InvalidPathException,
        match=r"This path does not represent a file or a directory. Please try again.*",
    ):
        omix_obj.download_metadata(valid_repo_key, valid_dataset_id, invalid_path)

    # downloading metadata using the main function download_metadata which internaly calls
    # omixatlas_summary and get_metadata
    assert (
        omix_obj.download_metadata(valid_repo_key, valid_dataset_id, valid_path) is None
    )
    file_path = f"{os.getcwd()}/{valid_dataset_id}.json"
    assert os.path.exists(file_path) is True
    os.remove(file_path)

    mocker.patch(
        polly.helpers.__name__ + ".get_metadata",
        side_effect=paramException(
            title="Param Error",
            detail="No matches found with the given repo details. Please try again.",
        ),
    )
    with pytest.raises(
        paramException,
        match=r"No matches found with the given repo details. Please try again.*",
    ):
        omix_obj.download_metadata(valid_repo_key, invalid_dataset_id, os.getcwd())


@pytest.fixture()
def get_linked_reports_fixture():
    """Get linked reports data from github"""
    base_polly_py_test_url = test_const.POLLY_PY_TEST_FILES_URL

    data_file = f"{base_polly_py_test_url}/fetch_reports_test_file.json"
    data = requests.get(data_file)
    error_handler(data)
    return data


def test_link_report(mocker, capsys, get_omixatlas_summary_mock_fixture):
    invalid_repo_key = 9
    valid_repo_key = "9"
    invalid_dataset_id = 9
    valid_dataset_id = "9"
    valid_workspace_id = 9
    invalid_workspace_id = "9"
    valid_workspace_path = "path_to_workspaces"
    invalid_workspace_path = 9
    valid_access_key = "private"
    invalid_access_key = 9
    obj = omixatlas.OmixAtlas(testpolly_token, "testpolly")
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.link_report(
            invalid_repo_key,
            valid_dataset_id,
            valid_workspace_id,
            valid_workspace_path,
            valid_access_key,
        )
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.link_report(
            valid_repo_key,
            invalid_dataset_id,
            valid_workspace_id,
            valid_workspace_path,
            valid_access_key,
        )
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.link_report(
            valid_repo_key,
            valid_dataset_id,
            invalid_workspace_id,
            invalid_workspace_path,
            valid_access_key,
        )
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.link_report(
            valid_repo_key,
            valid_dataset_id,
            valid_workspace_id,
            invalid_workspace_path,
            valid_access_key,
        )
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.link_report(
            valid_repo_key,
            valid_dataset_id,
            valid_workspace_id,
            valid_workspace_path,
            invalid_access_key,
        )
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.link_report(valid_repo_key, valid_dataset_id, valid_workspace_id)
    mocker.patch(
        polly_services.reporting.reporting_hlpr.__name__ + ".verify_workspace_details",
        return_value=None,
    )
    mocker.patch(
        polly_services.reporting.reporting_hlpr.__name__ + ".get_shared_id",
        return_value=None,
    )
    mocker.patch(
        polly_services.reporting.reporting_hlpr.__name__ + ".get_report_id",
        return_value="report_id",
    )
    mocker.patch(
        polly_services.reporting.reporting_hlpr.__name__ + ".change_file_access",
        return_value="sample_url",
    )
    mocker.patch(
        polly_services.polly_services_hlpr.__name__ + ".omixatlas_summary",
        return_value=get_omixatlas_summary_mock_fixture,
    )
    response = mocker.patch.object(obj.session, "post")
    response.return_value.status_code = 200
    # variation 1 for code coverage when access is same
    result = obj.link_report(
        valid_repo_key,
        valid_dataset_id,
        valid_workspace_id,
        valid_workspace_path,
        valid_access_key,
    )
    captured = capsys.readouterr()
    assert "File Successfully linked to dataset id" in captured.out
    assert result is None
    # variation 2 for code coverage when access is different
    mocker.patch(
        polly_services.reporting.reporting_hlpr.__name__ + ".get_shared_id",
        return_value="shared_id",
    )
    result = obj.link_report(
        valid_repo_key,
        valid_dataset_id,
        valid_workspace_id,
        valid_workspace_path,
        valid_access_key,
    )
    captured = capsys.readouterr()
    assert "File Successfully linked to dataset id" in captured.out
    assert result is None


def test_link_report_url(mocker, capsys, get_omixatlas_summary_mock_fixture):
    invalid_repo_key = 9
    valid_repo_key = "9"
    invalid_dataset_id = 9
    valid_dataset_id = "9"
    sample_url = "http://www.cwi.nl:80/%7Eguido/Python.html"
    obj = omixatlas.OmixAtlas(testpolly_token, "testpolly")
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.link_report(invalid_repo_key, valid_dataset_id, sample_url)
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.link_report(valid_repo_key, invalid_dataset_id, sample_url)
    mocker.patch(
        polly_services.polly_services_hlpr.__name__ + ".omixatlas_summary",
        return_value=get_omixatlas_summary_mock_fixture,
    )
    response = mocker.patch.object(obj.session, "post")
    response.return_value.status_code = 200
    obj.link_report(valid_repo_key, valid_dataset_id, sample_url)
    captured = capsys.readouterr()
    assert "Dataset -" in captured.out


def test_fetch_linked_reports(
    mocker, get_linked_reports_fixture, get_omixatlas_summary_mock_fixture
):
    invalid_repo_key = 9
    valid_repo_key = "9"
    invalid_dataset_id = 9
    valid_dataset_id = "9"
    obj = omixatlas.OmixAtlas(testpolly_token, "testpolly")
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.fetch_linked_reports(invalid_repo_key, valid_dataset_id)
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.fetch_linked_reports(valid_repo_key, invalid_dataset_id)
    mocked_response = get_linked_reports_fixture
    response = mocker.patch.object(obj.session, "get")
    response.return_value.status_code = 200
    response.return_value = mocked_response
    mocker.patch(
        polly_services.reporting.reporting_hlpr.__name__ + ".get_shared_id",
        return_value=None,
    )
    mocker.patch(
        polly_services.reporting.reporting_hlpr.__name__ + ".get_report_id",
        return_value="report_id",
    )
    mocker.patch(
        polly_services.reporting.reporting_hlpr.__name__ + ".change_file_access",
        return_value="sample_url",
    )
    mocker.patch(
        polly_services.reporting.reporting_hlpr.__name__ + ".check_is_file",
        return_value=True,
    )
    mocker.patch(
        polly_services.polly_services_hlpr.__name__ + ".omixatlas_summary",
        return_value=get_omixatlas_summary_mock_fixture,
    )
    mocker.patch(
        polly_services.reporting.reporting_hlpr.__name__ + ".return_workspace_file_url",
        return_value="sample_url",
    )
    df = obj.fetch_linked_reports(valid_repo_key, valid_dataset_id)
    assert isinstance(df, pd.DataFrame)


def test_delete_linked_report(mocker, capsys, get_omixatlas_summary_mock_fixture):
    invalid_repo_key = 9
    valid_repo_key = "9"
    invalid_dataset_id = 9
    valid_dataset_id = "9"
    valid_report_id = "report_id"
    invalid_report_id = 9
    obj = omixatlas.OmixAtlas(testpolly_token, "testpolly")
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.delete_linked_report(invalid_repo_key, valid_dataset_id, valid_report_id)
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.delete_linked_report(valid_repo_key, invalid_dataset_id, valid_report_id)
    with pytest.raises(
        InvalidParameterException,
        match=r".* Invalid Parameters .*",
    ):
        obj.delete_linked_report(valid_repo_key, valid_dataset_id, invalid_report_id)
    response = mocker.patch.object(obj.session, "delete")
    response.return_value.status_code = 200
    mocker.patch(
        polly_services.polly_services_hlpr.__name__ + ".omixatlas_summary",
        return_value=get_omixatlas_summary_mock_fixture,
    )
    result = obj.delete_linked_report(valid_repo_key, valid_dataset_id, valid_report_id)
    captured = capsys.readouterr()
    assert "Linked file with report_id" in captured.out
    assert result is None


# update dataset test cases
def test_update_dataset_str_type_source_folder_path():
    """
    incorrect datatype of source folder path
    shall throw an error
    """
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    # ingestion_test_1
    repo_id = "1654268055800"
    # source folder path is in str
    # it should in dict
    source_folder_path = "<ingestion file_path>"
    with pytest.raises(
        paramException,
        match=r".* source_folder_path should be a dict with valid data and metadata path values .*",
    ):
        omix_obj.update_datasets(repo_id, source_folder_path)


def test_update_dataset_dict_type_source_folder_path_wrong_data_path():
    """
    incorrect data path shall throw an error
    """
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    # ingestion_test_1
    repo_id = "1654268055800"
    # <ingestion_data_file_path>
    source_folder_path_data = f"{os.getcwd()}/data_val"
    source_folder_path = {"data": source_folder_path_data}
    with pytest.raises(
        paramException,
        match=r".* path passed is not found. Please pass the correct path and call the function again.*",
    ):
        omix_obj.update_datasets(repo_id, source_folder_path)


# wrong test -> this test is not applicable now
# def test_update_dataset_data_metadata():
#     """
#     tests:
#     if data and metadata are correctly provided
#     if not already present in oa -> uploaded.
#     if already present in oa -> updated
#     """
#     Polly.auth(testpolly_token, env="testpolly")
#     omix_obj = omixatlas.OmixAtlas()
#     repo_id = "1654268055800"

#     base_add_datatest_test_file_path = BASE_TEST_FORMAT_CONSTANTS_URL
#     base_add_metadata_test_file_path = BASE_TEST_FORMAT_CONSTANTS_URL
#     priority = "high"
#     # creating directory
#     parent_dir = os.getcwd()
#     data_dir = "dataset_ext_name_checks"
#     metadata_dir = "metadata_name_ext_checks"
#     data_path = os.path.join(parent_dir, data_dir)
#     metadata_path = os.path.join(parent_dir, metadata_dir)

#     # data directory
#     if not os.path.isdir(data_path):
#         os.makedirs(data_path)
#     # metadata directory
#     if not os.path.isdir(metadata_path):
#         os.makedirs(metadata_path)

#     # data file 1
#     dataset_files_folder_path = f"{base_add_datatest_test_file_path}/{data_dir}"
#     data_file_1 = (
#         f"{dataset_files_folder_path}"
#         + "/DLS_BB057_CV244_AML_BMMC_ATAC088_ATAC089_GEX062_GEX063_MTDNA073_MTDNA074_0.05rnaclustres_0.05corr.zip"
#     )
#     response_1 = requests.get(data_file_1)
#     error_handler(response_1)
#     file_1_name = "DLS_BB057_CV244_AML_BMMC_ATAC088_ATAC089_GEX062_GEX063_MTDNA073_MTDNA074_0.05rnaclustres_0.05corr.zip"
#     with open(os.path.join(data_path, file_1_name), "w") as file_1:
#         file_1_content = response_1.text
#         file_1.write(file_1_content)

#     metadata_file_folder_path = (
#         f"{base_add_metadata_test_file_path}/metadata_name_ext_checks"
#     )

#     metadata_file_1 = (
#         f"{metadata_file_folder_path}/"
#         + "DLS_BB057_CV244_AML_BMMC_ATAC088_ATAC089_GEX062_GEX063_MTDNA073_MTDNA074_0.05rnaclustres_0.05corr.json"
#     )
#     metadata_resp_1 = requests.get(metadata_file_1)
#     error_handler(metadata_resp_1)

#     meta_file_1_nam = (
# "DLS_BB057_CV244_AML_BMMC_ATAC088_ATAC089_GEX062_GEX063_MTDNA073_MTDNA074_0.05rnaclustres_0.05corr.json"
#     )

#     # creating files in metadata path
#     with open(os.path.join(metadata_path, meta_file_1_nam), "w") as m_file_1:
#         metadata_1_content = metadata_resp_1.text
#         m_file_1.write(metadata_1_content)

#     source_folder_path = {"data": data_path, "metadata": metadata_path}
#     destination_folder = "transcriptomics_75"

#     res = omix_obj.update_datasets(
#         repo_id, source_folder_path, destination_folder, priority
#     )

#     assert isinstance(res, pd.DataFrame)

#     # number of rows should be 6 in the df -> 5 data files listed above
#     # And 1 combined metadata file
#     num_of_rows = len(res.index)
#     assert num_of_rows == 2

# TODO: need to revert commented code
# def test_update_dataset_update_metadata_with_no_dataset_in_oa():
#     """
#     updating a metadata with no data in the oa
#     shall throw a warning and skip the update
#     """
#     Polly.auth(testpolly_token, env="testpolly")
#     omix_obj = omixatlas.OmixAtlas()
#     # ingestion_test_1
#     repo_id = "1654268055800"
#     base_add_metadata_test_file_path = BASE_TEST_FORMAT_CONSTANTS_URL

#     # creating directory
#     parent_dir = os.getcwd()
#     metadata_dir = "metadata_name_new"
#     metadata_path = os.path.join(parent_dir, metadata_dir)

#     # metadata directory
#     if not os.path.isdir(metadata_path):
#         os.makedirs(metadata_path)
#     metadata_file_folder_path = (
#         f"{base_add_metadata_test_file_path}/metadata_name_ext_checks"
#     )
#     # metadata file such that corresponding data file is not present in OA
#     metadata_file_1 = (
#         f"{metadata_file_folder_path}/"
#         + "DLS_BB057_CV244_AML_BMMC_ATAC088_ATAC089_GEX062_GEX063_MTDNA073_MTDNA074_0.05rnaclustres_0.05corr.json"
#     )
#     metadata_resp_1 = requests.get(metadata_file_1)
#     error_handler(metadata_resp_1)

#     meta_file_1_nam = "DLS_BB057_CV244_AML_BMMC_ATAC088_ATAC089_GEX062_GEX063_
#     MTDNA073_MTDNA074_0.05rnaclustres_0.05corrN.json"

#     # creating files in metadata path
#     with open(os.path.join(metadata_path, meta_file_1_nam), "w") as m_file_1:
#         metadata_1_content = metadata_resp_1.text
#         m_file_1.write(metadata_1_content)
#     source_folder_path = {"metadata": metadata_path}
#     destination_folder = "transcriptomics_75"

#     with pytest.warns(Warning) as record:
#         omix_obj.update_datasets(repo_id, source_folder_path, destination_folder)
#         if not record:
#             pytest.fail("Expected a warning!")
#     print(record)
#     assert len(record) >= 1


# these files are there in s3 but not ingested in infra
# that is why it is not showing in the list files API
# that is why a warning is getting raised because system shows that these files
# are present in it from before -> so this test is failing
# needs to be discussed with shilpa once
# def test_update_dataset_all_edge_cases_of_ext_and_names_with_one_missing_data():
#     """
#     tests:
#     1. support for the different file formats for data and metadata
#     2. warning shall be given if a metadata is being updated without any data file.
#     3. all datafiles with supported formats shall be updated if metadata files provided
#     """
#     # test_update_dataset_all_edge_cases_of_ext_and_names_with_one_missing_metadata
#     # names with `.`s, tar.gz, gct.bz, vcf.bgz
#     # multi word extensions
#     # zips formats
#     Polly.auth(testpolly_token, env="testpolly")
#     omix_obj = omixatlas.OmixAtlas()
#     repo_id = "1654268055800"
#     base_add_datatest_test_file_path = BASE_TEST_FORMAT_CONSTANTS_URL
#     base_add_metadata_test_file_path = BASE_TEST_FORMAT_CONSTANTS_URL

#     # creating directory
#     parent_dir = os.getcwd()
#     data_dir = "data_file_ext_checks"
#     metadata_dir = "metadata_file_ext_checks"
#     data_path = os.path.join(parent_dir, data_dir)
#     metadata_path = os.path.join(parent_dir, metadata_dir)

#     # data directory
#     if not os.path.isdir(data_path):
#         os.makedirs(data_path)
#     # metadata directory
#     if not os.path.isdir(metadata_path):
#         os.makedirs(metadata_path)

#     dataset_files_folder_path = (
#         f"{base_add_datatest_test_file_path}/dataset_ext_name_checks"
#     )
#     data_file_1 = (
#         f"{dataset_files_folder_path}"
#         + "/DLS_BB057_CV244_AML_BMMC_ATAC088_ATAC089_GEX062_GEX063_MTDNA073_MTDNA074_0.05rnaclustres_0.05corr.zip"
#     )
#     data_file_2 = f"{dataset_files_folder_path}/a.b.tar.gz"
#     data_file_3 = f"{dataset_files_folder_path}/abc.gct.bz"
#     data_file_4 = f"{dataset_files_folder_path}/def.vcf.bgz"

#     response_1 = requests.get(data_file_1)
#     error_handler(response_1)
#     response_2 = requests.get(data_file_2)
#     error_handler(response_2)
#     response_3 = requests.get(data_file_3)
#     error_handler(response_3)
#     response_4 = requests.get(data_file_4)
#     error_handler(response_4)

#     file_1_name = "DLS_BB057_CV244_AML_BMMC_ATAC088_ATAC089_GEX062_GEX063_MTDNA073_MTDNA074_0.05rnaclustres_0.05corr.zip"
#     file_2_name = "a.b.tar.gz"
#     file_3_name = "abc.gct.bz"
#     file_4_name = "def.vcf.bgz"

#     # creating files in data path
#     with open(os.path.join(data_path, file_1_name), "w") as file_1:
#         file_1_content = response_1.text
#         file_1.write(file_1_content)

#     with open(os.path.join(data_path, file_2_name), "w") as file_2:
#         file_2_content = response_2.text
#         file_2.write(file_2_content)

#     with open(os.path.join(data_path, file_3_name), "w") as file_3:
#         file_3_content = response_3.text
#         file_3.write(file_3_content)

#     with open(os.path.join(data_path, file_4_name), "w") as file_4:
#         file_4_content = response_4.text
#         file_4.write(file_4_content)

#     metadata_file_folder_path = (
#         f"{base_add_metadata_test_file_path}/metadata_name_ext_checks"
#     )

#     metadata_file_1 = (
#         f"{metadata_file_folder_path}/"
#         + "DLS_BB057_CV244_AML_BMMC_ATAC088_ATAC089_GEX062_GEX063_MTDNA073_MTDNA074_0.05rnaclustres_0.05corr.json"
#     )
#     metadata_file_2 = f"{metadata_file_folder_path}/a.b.json"
#     metadata_file_3 = f"{metadata_file_folder_path}/abc.json"
#     metadata_file_4 = f"{metadata_file_folder_path}/def.json"
#     metadata_file_5 = f"{metadata_file_folder_path}/tcga_LIHC_Copy_Number_Segment_TCGA-G3-A25Z-01A.b.json"

#     metadata_resp_1 = requests.get(metadata_file_1)
#     error_handler(metadata_resp_1)

#     metadata_resp_2 = requests.get(metadata_file_2)
#     error_handler(metadata_resp_2)

#     metadata_resp_3 = requests.get(metadata_file_3)
#     error_handler(metadata_resp_3)

#     metadata_resp_4 = requests.get(metadata_file_4)
#     error_handler(metadata_resp_4)

#     metadata_resp_5 = requests.get(metadata_file_5)
#     error_handler(metadata_resp_5)

# meta_file_1_nam = (
#         "DLS_BB057_CV244_AML_BMMC_ATAC088_ATAC089_GEX062_GEX063_MTDNA073_MTDNA074_0.05rnaclustres_0.05corr.json"
# )
#     metadata_file_2_name = "a.b.json"
#     metadata_file_3_name = "abc.json"
#     metadata_file_4_name = "def.json"
#     metadata_file_5_name = "tcga_LIHC_Copy_Number_Segment_TCGA-G3-A25Z-01A.b.json"

#     # creating files in metadata path
#     with open(os.path.join(metadata_path, meta_file_1_nam), "w") as m_file_1:
#         metadata_1_content = metadata_resp_1.text
#         m_file_1.write(metadata_1_content)

#     with open(os.path.join(metadata_path, metadata_file_2_name), "w") as m_file_2:
#         metadata_2_content = metadata_resp_2.text
#         m_file_2.write(metadata_2_content)

#     with open(os.path.join(metadata_path, metadata_file_3_name), "w") as m_file_3:
#         metadata_3_content = metadata_resp_3.text
#         m_file_3.write(metadata_3_content)

#     with open(os.path.join(metadata_path, metadata_file_4_name), "w") as m_file_4:
#         metadata_4_content = metadata_resp_4.text
#         m_file_4.write(metadata_4_content)

#     with open(os.path.join(metadata_path, metadata_file_5_name), "w") as m_file_5:
#         metadata_5_content = metadata_resp_5.text
#         m_file_5.write(metadata_5_content)

#     source_folder_path = {"data": data_path, "metadata": metadata_path}
#     destination_folder = "transcriptomics_75"

#     # then updating the same datasets
#     res = omix_obj.update_datasets(repo_id, source_folder_path, destination_folder)
#     assert isinstance(res, pd.DataFrame)

#     # number of rows should be 6 in the df -> 5 data files listed above
#     # And 1 combined metadata file
#     num_of_rows = len(res.index)
#     assert num_of_rows == 6


def test_update_dataset_wrong_priority_value():
    """
    update dataset with incorrect priority value
    shall throw error
    """
    Polly.auth(token)
    omix_obj = omixatlas.OmixAtlas()
    # ingestion_test_1
    repo_id = "1654268055800"
    source_folder_path_data = f"{os.getcwd()}/data_file"
    source_folder_path_metadata = f"{os.getcwd()}/metadata_file"
    source_folder_path = {
        "data": source_folder_path_data,
        "metadata": source_folder_path_metadata,
    }

    priority = "super_high"
    with pytest.raises(
        paramException,
        match=r".*`priority` should be a string. Only 3 values are allowed i.e. `low`, `medium`, `high`.*",
    ):
        omix_obj.update_datasets(repo_id, source_folder_path, priority=priority)


def test_update_dataset_incorrect_priority_value_format():
    """
    testing args datatype/format:
    update dataset with incorrect priority value format
    shall throw error
    """
    Polly.auth(token)
    omix_obj = omixatlas.OmixAtlas()
    # ingestion_test_1
    repo_id = "1654268055800"
    source_folder_path_data = f"{os.getcwd()}/data_file"
    source_folder_path_metadata = f"{os.getcwd()}/metadata_file"
    source_folder_path = {
        "data": source_folder_path_data,
        "metadata": source_folder_path_metadata,
    }
    priority = ["super_high"]
    with pytest.raises(
        paramException,
        match=r"`priority` should be a string. Only 3 values are allowed i.e. `low`, `medium`, `high`",
    ):
        omix_obj.update_datasets(repo_id, source_folder_path, priority=priority)


def test_update_dataset_data_file_with_wrong_extension():
    """
    updating dataset file with invalid extension
    shall throw error
    """
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    repo_id = "1654268055800"

    file_3_name = "incorrect_ext_data_file.txt"

    # creating directory
    parent_dir = os.getcwd()
    data_dir = "data_file_wrong_ext"
    metadata_dir = "metadata_file_wrong_ext"
    data_path = os.path.join(parent_dir, data_dir)
    metadata_path = os.path.join(parent_dir, metadata_dir)

    # data directory
    if not os.path.isdir(data_path):
        os.makedirs(data_path)
    # metadata directory
    if not os.path.isdir(metadata_path):
        os.makedirs(metadata_path)

    # creating files in data path
    with open(os.path.join(data_path, file_3_name), "w") as file_3:
        file_3_content = "wrong extension data file"
        file_3.write(file_3_content)

    source_folder_path = {"data": data_path, "metadata": metadata_path}

    with pytest.raises(
        paramException,
        match=r".* File format for file .* invalid.It can be =>.*",
    ):
        omix_obj.update_datasets(repo_id, source_folder_path)


# TODO make changes in the tests when new validation flow of
# multi source, multi datatype is integrated
def test_update_dataset_metadata_file_with_wrong_extension():
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    # ingestion_test_1
    repo_id = "1654268055800"

    metadata_2_name = "incorrect_ext_data_file.txt"

    # creating directory
    parent_dir = os.getcwd()
    data_dir = "data_file_wrong_ext"
    metadata_dir = "metadata_file_wrong_ext"
    data_path = os.path.join(parent_dir, data_dir)
    metadata_path = os.path.join(parent_dir, metadata_dir)

    # data directory
    if not os.path.isdir(data_path):
        os.makedirs(data_path)
    # metadata directory
    if not os.path.isdir(metadata_path):
        os.makedirs(metadata_path)

    # creating files in data path
    with open(os.path.join(metadata_path, metadata_2_name), "w") as file_3:
        file_3_content = "wrong extension data file"
        file_3.write(file_3_content)

    source_folder_path = {"data": data_path, "metadata": metadata_path}

    with pytest.raises(
        paramException,
        match=r".* File format for file .* invalid.It can be =>.*",
    ):
        omix_obj.update_datasets(repo_id, source_folder_path)


@pytest.fixture()
def get_validatation_lib_mock_fixture():
    data = ["a", "b", "c"]
    empty_df = pd.DataFrame(data)

    err_dataset = empty_df
    status_dict = {
        "ACBC_MSKCC_2015_Copy_Number_AdCC10T": False,
        "ACBC_MSKCC_2015_Copy_Number_AdCC12T": False,
    }

    return err_dataset, status_dict


# def test_validation_addition_datasets_full_flow(
#     mocker, get_validatation_lib_mock_fixture, list_folders_function_mock_fixture
# ):
#     # mocking the list folders API funct
#     mocker.patch(
#         polly_services.files.files_hlpr.__name__
#         + ".check_destination_folder_for_dataset_id",
#         return_value=list_folders_function_mock_fixture,
#     )

#     Polly.auth(testpolly_token, env="testpolly")
#     omix_obj = omixatlas.OmixAtlas()
#     validation_obj = Validation()
#     # ingestion_test_1
#     repo_id = "1654268055800"
#     base_add_datatest_test_file_path = const.VALIDATION_FLOW_FILES_URL

#     # creating directory
#     parent_dir = os.getcwd()
#     data_dir = "dataset"
#     metadata_dir = "metadata"
#     data_path = os.path.join(parent_dir, data_dir)
#     metadata_path = os.path.join(parent_dir, metadata_dir)

#     # data directory
#     if not os.path.isdir(data_path):
#         os.makedirs(data_path)
#     # metadata directory
#     if not os.path.isdir(metadata_path):
#         os.makedirs(metadata_path)

#     # data file 1
#     data_file_1 = f"{base_add_datatest_test_file_path}/dataset/ACBC_MSKCC_2015_Copy_Number_AdCC10T.gct"
#     data_file_2 = f"{base_add_datatest_test_file_path}/dataset/ACBC_MSKCC_2015_Copy_Number_AdCC11T.gct"
#     data_file_3 = f"{base_add_datatest_test_file_path}/dataset/ACBC_MSKCC_2015_Copy_Number_AdCC12T.gct"
#     data_file_4 = f"{base_add_datatest_test_file_path}/dataset/ACBC_MSKCC_2015_Copy_Number_AdCC1T.gct"
#     response_1 = requests.get(data_file_1)
#     error_handler(response_1)
#     response_2 = requests.get(data_file_2)
#     error_handler(response_2)
#     response_3 = requests.get(data_file_3)
#     error_handler(response_3)
#     response_4 = requests.get(data_file_4)
#     error_handler(response_4)

#     file_1_name = "ACBC_MSKCC_2015_Copy_Number_AdCC1T.gct"
#     file_2_name = "ACBC_MSKCC_2015_Copy_Number_AdCC10T.gct"
#     file_3_name = "ACBC_MSKCC_2015_Copy_Number_AdCC12T.gct"
#     file_4_name = "ACBC_MSKCC_2015_Copy_Number_AdCC11T.gct"

#     # creating files in data path
#     with open(os.path.join(data_path, file_1_name), "w") as file_1:
#         file_1_content = response_1.text
#         file_1.write(file_1_content)

#     with open(os.path.join(data_path, file_2_name), "w") as file_2:
#         file_2_content = response_2.text
#         file_2.write(file_2_content)

#     with open(os.path.join(data_path, file_3_name), "w") as file_3:
#         file_3_content = response_3.text
#         file_3.write(file_3_content)

#     with open(os.path.join(data_path, file_4_name), "w") as file_4:
#         file_4_content = response_4.text
#         file_4.write(file_4_content)

#     metadata_file_1 = f"{base_add_datatest_test_file_path}/metadata/ACBC_MSKCC_2015_Copy_Number_AdCC10T.json"
#     metadata_file_2 = f"{base_add_datatest_test_file_path}/metadata/ACBC_MSKCC_2015_Copy_Number_AdCC11T.json"
#     metadata_file_3 = f"{base_add_datatest_test_file_path}/metadata/ACBC_MSKCC_2015_Copy_Number_AdCC12T.json"
#     metadata_file_4 = f"{base_add_datatest_test_file_path}/metadata/ACBC_MSKCC_2015_Copy_Number_AdCC1T.json"

#     metadata_file_1_name = "ACBC_MSKCC_2015_Copy_Number_AdCC10T.json"
#     metadata_file_2_name = "ACBC_MSKCC_2015_Copy_Number_AdCC11T.json"
#     metadata_file_3_name = "ACBC_MSKCC_2015_Copy_Number_AdCC12T.json"
#     metadata_file_4_name = "ACBC_MSKCC_2015_Copy_Number_AdCC1T.json"

#     metadata_resp_1 = requests.get(metadata_file_1)
#     error_handler(metadata_resp_1)
#     metadata_resp_2 = requests.get(metadata_file_2)
#     error_handler(metadata_resp_2)
#     metadata_resp_3 = requests.get(metadata_file_3)
#     error_handler(metadata_resp_3)
#     metadata_resp_4 = requests.get(metadata_file_4)
#     error_handler(metadata_resp_4)

#     # creating files in metadata path
#     with open(os.path.join(metadata_path, metadata_file_1_name), "w") as meta_file_1:
#         metadata_1_content = metadata_resp_1.text
#         meta_file_1.write(metadata_1_content)

#     with open(os.path.join(metadata_path, metadata_file_2_name), "w") as meta_file_2:
#         metadata_2_content = metadata_resp_2.text
#         meta_file_2.write(metadata_2_content)

#     with open(os.path.join(metadata_path, metadata_file_3_name), "w") as meta_file_3:
#         metadata_3_content = metadata_resp_3.text
#         meta_file_3.write(metadata_3_content)

#     with open(os.path.join(metadata_path, metadata_file_4_name), "w") as meta_file_4:
#         metadata_4_content = metadata_resp_4.text
#         meta_file_4.write(metadata_4_content)

#     source_folder_path = {"data": data_path, "metadata": metadata_path}
#     schema_config = {}
#     schema_config["source"] = "geo"
#     schema_config["datatype"] = "all"

#     # mock validation library response

#     mocker.patch(
#         dataset_metadata_validator.__name__ + ".check_metadata_for_errors",
#         return_value=get_validatation_lib_mock_fixture,
#     )

#     err_dataset_df, status_dict = validation_obj.validate_datasets(
#         repo_id, source_folder_path, schema_config=schema_config
#     )

#     assert isinstance(err_dataset_df, pd.DataFrame)
#     assert isinstance(status_dict, dict)

#     res_df = omix_obj.add_datasets(repo_id, source_folder_path, validation=True)
#     assert isinstance(res_df, pd.DataFrame)

#     # only two files will be uploaded
#     # Other two files will not be uploaded as they have failed validation
#     # applying assertion on res_df to check only two files
#     # coming in `res_df`
#     # 1 more file `combined_metadata` file will be uploaded
#     # TODO: revert to back to 3 value once the validation lib issues are fixed
#     assert res_df.shape[0] == 3
#     # assert res_df.shape[0] == 5


# DLS_BB057_CV244_AML_BMMC_ATAC088_ATAC089_GEX062_GEX063_MTDNA073_MTDNA074_0.05rnaclustres_0.05corr.zip
# this file is there in s3 but not ingested in the infra so it is giving warning that is why test is failing
# def test_update_dataset_correct_combined_metadata_json():
#     # test generation of combined_metadata json and content
#     # json should have ingestion and dataset details.

#     Polly.auth(testpolly_token, env="testpolly")
#     omix_obj = omixatlas.OmixAtlas()
#     repo_id = "1654268055800"
#     base_add_datatest_test_file_path = BASE_TEST_FORMAT_CONSTANTS_URL
#     base_add_metadata_test_file_path = BASE_TEST_FORMAT_CONSTANTS_URL
#     priority = "high"
#     # creating directory
#     parent_dir = os.getcwd()
#     data_dir = "dataset_ext_name_checks"
#     metadata_dir = "metadata_name_ext_checks"
#     data_path = os.path.join(parent_dir, data_dir)
#     metadata_path = os.path.join(parent_dir, metadata_dir)

#     # data directory
#     if not os.path.isdir(data_path):
#         os.makedirs(data_path)
#     # metadata directory
#     if not os.path.isdir(metadata_path):
#         os.makedirs(metadata_path)
#     data_file_1 = "DLS_BB057_CV244_AML_BMMC_ATAC088_ATAC089_GEX062_GEX063_MTDNA073_MTDNA074_0.05rnaclustres_0.05corr.zip"
#     # data file 1
#     dataset_files_folder_path = f"{base_add_datatest_test_file_path}/{data_dir}"
#     data_file_1 = (
#         f"{dataset_files_folder_path}"
#         + "/DLS_BB057_CV244_AML_BMMC_ATAC088_ATAC089_GEX062_GEX063_MTDNA073_MTDNA074_0.05rnaclustres_0.05corr.zip"
#     )
#     response_1 = requests.get(data_file_1)
#     error_handler(response_1)
#     file_1_name = "DLS_BB057_CV244_AML_BMMC_ATAC088_ATAC089_GEX062_GEX063_MTDNA073_MTDNA074_0.05rnaclustres_0.05corr.zip"
#     with open(os.path.join(data_path, file_1_name), "w") as file_1:
#         file_1_content = response_1.text
#         file_1.write(file_1_content)

#     metadata_file_folder_path = (
#         f"{base_add_metadata_test_file_path}/metadata_name_ext_checks"
#     )

#     metadata_file_1 = (
#         f"{metadata_file_folder_path}/"
#         + "DLS_BB057_CV244_AML_BMMC_ATAC088_ATAC089_GEX062_GEX063_MTDNA073_MTDNA074_0.05rnaclustres_0.05corr.json"
#     )
#     metadata_resp_1 = requests.get(metadata_file_1)
#     error_handler(metadata_resp_1)

# meta_file_1_nam = (
#     "DLS_BB057_CV244_AML_BMMC_ATAC088_ATAC089_GEX062_GEX063_MTDNA073_MTDNA074_0.05rnaclustres_0.05corr.json"
# )

#     # creating files in metadata path
#     with open(os.path.join(metadata_path, meta_file_1_nam), "w") as m_file_1:
#         metadata_1_content = metadata_resp_1.text
#         m_file_1.write(metadata_1_content)
#     source_folder_path = {"data": data_path, "metadata": metadata_path}
#     destination_folder = "transcriptomics_75"

#     # generating the data_metadata_mapping_dict
#     data_metadata_mapping_dict = {}
#     unmapped_file_names = []
#     (
#         data_metadata_mapping_dict,
#         unmapped_file_names,
#         unmapped_metadata_file_names,
#     ) = omix_obj._map_data_metadata_files_for_update(source_folder_path)
#     # coinstructing the metadata dict which then goes into the combined metadata.json

#     metadata_file_list = omix_hlpr.metadata_files_for_upload(metadata_path)
#     combined_metadata_dict = omix_obj._construct_metadata_dict_from_files(
#         repo_id,
#         metadata_file_list,
#         priority,
#         destination_folder,
#         data_metadata_mapping_dict,
#         metadata_path,
#         update=True,
#     )
#     assert combined_metadata_dict is not None
#     assert combined_metadata_dict["data"] is not None
#     types_in_metadata_dict = []
#     for item in combined_metadata_dict["data"]:
#         types_in_metadata_dict.append(item.get("type"))
#     assert "ingestion_metadata" in types_in_metadata_dict
#     assert "file_metadata" in types_in_metadata_dict


@pytest.fixture()
def get_metadata_fixture():
    """Get geo metadata from github"""
    base_polly_py_test_url = test_const.POLLY_PY_TEST_FILES_URL

    data_file = f"{base_polly_py_test_url}/geo_get_metadata_response.json"
    data = requests.get(data_file)
    error_handler(data)
    return data


@pytest.fixture()
def get_metadata_empty_hits_fixture():
    """Get response with empty hits from github"""
    base_polly_py_test_url = test_const.POLLY_PY_TEST_FILES_URL

    data_file = f"{base_polly_py_test_url}/final_pagination_mocked_response.json"
    data = requests.get(data_file)
    error_handler(data)
    return data


@pytest.fixture()
def get_metadata_csv_fixture():
    """Get geo metadata csv file from github"""
    base_polly_py_test_url = test_const.POLLY_PY_TEST_FILES_URL

    data_file = f"{base_polly_py_test_url}/geo_get_metadata_test_df.csv"
    try:
        data_df = pd.read_csv(data_file)
    except Exception as err:
        raise err
    return data_df


def test_get_metadata(mocker, get_metadata_csv_fixture):
    Polly.auth(token)
    obj = omixatlas.OmixAtlas()
    correct_repo_name = "geo"
    correct_repo_id = 9
    incorrect_repo_key = [9]
    correct_dataset_id = "GSE199927_GPL19057"
    incorrect_dataset_id = 1234
    correct_table_name = "samples"
    incorrect_table_name = "datasets"
    assert isinstance(
        obj.get_metadata(correct_repo_name, correct_dataset_id, correct_table_name),
        pd.DataFrame,
    )
    assert isinstance(
        obj.get_metadata(correct_repo_id, correct_dataset_id, correct_table_name),
        pd.DataFrame,
    )
    with pytest.raises(
        paramException,
        match=r".*Argument 'table_name' not valid, .*",
    ):
        obj.get_metadata(correct_repo_name, correct_dataset_id, incorrect_table_name)

    with pytest.raises(
        paramException,
        match=r".*Argument 'dataset_id' is either empty or invalid. .*",
    ):
        obj.get_metadata(correct_repo_id, incorrect_dataset_id, correct_table_name)

    with pytest.raises(
        paramException,
        match=r".*Argument 'repo_key' is either empty or invalid. .*",
    ):
        obj.get_metadata(incorrect_repo_key, correct_dataset_id, correct_table_name)
    dataframe_result = get_metadata_csv_fixture
    mocker.patch(
        polly.omixatlas.__name__ + ".OmixAtlas._retrieve_dataframe",
        return_value=dataframe_result,
    )
    result = obj.get_metadata(correct_repo_name, correct_dataset_id, correct_table_name)
    assert result.equals(dataframe_result) is True


def test_retrieve_dataframe(mocker, get_metadata_fixture, get_metadata_csv_fixture):
    Polly.auth(token)
    obj = omixatlas.OmixAtlas()
    index = "geo_gct_col_metadata"
    discover_url = (
        f"https://api.datalake.discover.{obj.session.env}.elucidata.io/elastic/v2"
    )
    page_size = 1000
    dataset_id = "GSE199927_GPL19057"
    intermediate_result = get_metadata_fixture
    dataframe_result = get_metadata_csv_fixture
    mocker.patch(
        polly.omixatlas.__name__ + ".OmixAtlas._initiate_retrieval",
        return_value=intermediate_result,
    )
    mocker.patch(
        polly.omixatlas.__name__ + ".OmixAtlas._complete_retrieval",
        return_value=dataframe_result,
    )
    result = obj._retrieve_dataframe(discover_url, page_size, dataset_id, index)
    assert isinstance(result, pd.DataFrame)


def test_initiate_retrieval(mocker, get_metadata_fixture):
    Polly.auth(token)
    obj = omixatlas.OmixAtlas()
    dataframe_result = get_metadata_fixture
    response = mocker.patch.object(obj.session, "post")
    response.return_value.status_code = 200
    response.return_value = dataframe_result
    index = "geo_gct_col_metadata"
    discover_url = (
        f"https://api.datalake.discover.{obj.session.env}.elucidata.io/elastic/v2"
    )
    page_size = 1000
    dataset_id = "GSE199927_GPL19057"
    query = {
        "query": {
            "term": {
                # Count entries for the following key-value pairs
                "src_dataset_id.keyword": dataset_id
            }
        },
        # Fetch X many rows at a time (you will still get the full output, which may be greater than 10K)
        # Setting this value to be greater than 10k will result in an error
        "size": page_size,
    }
    result = obj._initiate_retrieval(discover_url, query, index)
    assert isinstance(result, dict)


def test_complete_retrieval(
    mocker, get_metadata_fixture, get_metadata_empty_hits_fixture
):
    Polly.auth(token)
    obj = omixatlas.OmixAtlas()
    dataframe_result = get_metadata_empty_hits_fixture
    response = mocker.patch.object(obj.session, "post")
    response.return_value.status_code = 200
    response.return_value = dataframe_result
    discover_url = (
        f"https://api.datalake.discover.{obj.session.env}.elucidata.io/elastic/v2"
    )
    intermediate_result = get_metadata_fixture
    json_arg = json.loads(intermediate_result.text)
    result = obj._complete_retrieval(discover_url, json_arg)
    assert isinstance(result, pd.DataFrame)


@pytest.fixture()
def get_omixatlas_mock_fixture(mocker, get_ingestion_test_1_fixture):
    Polly.auth(testpolly_token, env="testpolly")
    nobj = omixatlas.OmixAtlas()
    # ingestion_test_1
    repo_id = test_const.INGESTION_TEST_1_REPO_ID
    fake_json = get_ingestion_test_1_fixture
    response = mocker.patch.object(nobj.session, "get")
    response.return_value.status_code = 200
    response.return_value.json.return_value = fake_json

    result = nobj._get_omixatlas(repo_id)
    return result


# @pytest.fixture
# def get_omixatlas_mock_fixture_polly_services(mocker, get_ingestion_test_1_fixture):
#     Polly.auth(testpolly_token, env="testpolly")
#     nobj = omixatlas.OmixAtlas()
#     # ingestion_test_1
#     repo_id = test_const.INGESTION_TEST_1_REPO_ID
#     fake_json = get_ingestion_test_1_fixture
#     response = mocker.patch.object(nobj.session, "get")
#     response.return_value.status_code = 200
#     response.return_value.json.return_value = fake_json

#     result = polly_services_hlpr.get_omixatlas(nobj, repo_id)
#     return result


@pytest.fixture()
def validate_schema_mock_fixture(
    mocker,
    get_omixatlas_mock_fixture_polly_services,
    get_ingestion_test_1_schema_fixture,
):
    # Return an empty DataFrame (no validation errors) for positive test cases
    # This fixture is used to mock validate_schema to skip actual validation
    error_df = pd.DataFrame()
    return error_df


# insert schema test 1 -> positive case
def test_insert_schema_positive_case(
    mocker, validate_schema_mock_fixture, capsys, get_ingestion_test_1_schema_fixture
):
    # Doing it on a repo that already exists
    # 1st -> Mock response of _get_omixatlas() call
    # inside validate schema -> make a seperate mocked function for that
    mocker.patch(
        polly.omixatlas.__name__ + ".OmixAtlas.validate_schema",
        return_value=validate_schema_mock_fixture,
    )
    # then mocking the response of POST API CALL for Insert Schema
    Polly.auth(testpolly_token, env="testpolly")
    nobj = omixatlas.OmixAtlas()
    response = mocker.patch.object(nobj.session, "post")
    response.return_value.status_code = 201

    # ingestion_test_1
    repo_id = test_const.INGESTION_TEST_1_REPO_ID

    body = get_ingestion_test_1_schema_fixture
    nobj.insert_schema(repo_id, body)
    # when successfully run
    # comparing the print in the function is coming out
    # in the stdout
    captured = capsys.readouterr()
    assert "Schema has been Inserted" in captured.out


# insert schema test 2 -> repo_id wrong format
def test_insert_schema_repo_id_wrong_format(get_ingestion_test_1_schema_fixture):
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    repo_id = [test_const.INGESTION_TEST_1_REPO_ID]
    body = get_ingestion_test_1_schema_fixture
    with pytest.raises(
        paramException,
        match=r".should be str or int",
    ):
        omix_obj.insert_schema(repo_id, body)


# incorrect repo_key -> repo_id
def test_insert_schema_wrong_repo_key_argument(
    mocker, validate_schema_mock_fixture, get_ingestion_test_1_schema_fixture
):
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()

    mocker.patch(
        polly.omixatlas.__name__ + ".OmixAtlas.validate_schema",
        return_value=validate_schema_mock_fixture,
    )

    # wrong repo key
    repo_key = "12345"
    body = get_ingestion_test_1_schema_fixture
    with pytest.raises(
        paramException,
        match=r".* Value of repo_key in the parameter and repo_id in the payload not same.*",
    ):
        omix_obj.insert_schema(repo_key, body)


# incorrect repo_key -> repo name
def test_insert_schema_wrong_repo_key_argument_repo_name(
    mocker,
    validate_schema_mock_fixture,
    get_ingestion_test_1_schema_fixture,
    get_omixatlas_mock_fixture_polly_services,
):
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()

    mocker.patch(
        polly.omixatlas.__name__ + ".OmixAtlas.validate_schema",
        return_value=validate_schema_mock_fixture,
    )

    # get_omixatlas to give details from omixatlas details from which repo_id is fetched is
    # and compared
    mocker.patch(
        polly_services.polly_services_hlpr.__name__ + ".get_omixatlas",
        return_value=get_omixatlas_mock_fixture_polly_services,
    )

    # repo_key valid not equal to repo identifier in the body
    repo_key = "lib_repo_dev"
    body = get_ingestion_test_1_schema_fixture
    with pytest.raises(
        paramException,
        match=r".* Value of repo_key in the parameter and repo_id in the payload not same.*",
    ):
        omix_obj.insert_schema(repo_key, body)


# insert schema test 3 -> body in wrong format
def test_insert_schema_body_wrong_format():
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    repo_id = test_const.INGESTION_TEST_1_REPO_ID
    body = "abcd"

    with pytest.raises(
        paramException,
        match=r"body should not be empty and it should be of type dict",
    ):
        omix_obj.insert_schema(repo_id, body)


# update schema test 1 -> positive case
def test_update_schema_positive_case(
    mocker, validate_schema_mock_fixture, capsys, get_ingestion_test_1_schema_fixture
):
    # Doing it on a repo that already exists
    # 1st -> Mock response of `_get_omixatlas()` call
    # inside validate schema -> make a seperate mocked function for that
    mocker.patch(
        polly.omixatlas.__name__ + ".OmixAtlas.validate_schema",
        return_value=validate_schema_mock_fixture,
    )

    # then mocking the response of PATCH API CALL for Update Schema
    Polly.auth(testpolly_token, env="testpolly")
    nobj = omixatlas.OmixAtlas()
    # mocked response with status and no specific value
    # as no specific response is mocked -> generic message will be printed
    response = mocker.patch.object(nobj.session, "patch")
    response.return_value.status_code = 200

    # ingestion_test_1
    repo_id = test_const.INGESTION_TEST_1_REPO_ID

    body = get_ingestion_test_1_schema_fixture

    nobj.update_schema(repo_id, body)
    # when successfully run
    # comparing the print in the function is coming out
    # in the stdout
    captured = capsys.readouterr()
    assert "Schema update is in progress" in captured.out


# update schema test 2 -> repo_id wrong format
def test_update_schema_repo_id_wrong_format(get_ingestion_test_1_schema_fixture):
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    repo_id = [test_const.INGESTION_TEST_1_REPO_ID]
    body = get_ingestion_test_1_schema_fixture

    with pytest.raises(
        paramException,
        match=r".should be str or int",
    ):
        omix_obj.update_schema(repo_id, body)


# update schema test 3 -> body wrong format
def test_update_schema_body_wrong_format():
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    repo_id = test_const.INGESTION_TEST_1_REPO_ID
    body = "abcd"

    with pytest.raises(
        paramException,
        match=r"body should not be empty and it should be of type dict",
    ):
        omix_obj.update_schema(repo_id, body)


# incorrect repo_key -> repo_id
def test_update_schema_wrong_repo_key_argument(
    mocker, validate_schema_mock_fixture, get_ingestion_test_1_schema_fixture
):
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()

    mocker.patch(
        polly.omixatlas.__name__ + ".OmixAtlas.validate_schema",
        return_value=validate_schema_mock_fixture,
    )

    # wrong repo key
    repo_key = "12345"
    body = get_ingestion_test_1_schema_fixture
    with pytest.raises(
        paramException,
        match=r".* Value of repo_key in the parameter and repo_id in the payload not same.*",
    ):
        omix_obj.update_schema(repo_key, body)


# incorrect repo_key -> repo name
def test_update_schema_wrong_repo_key_argument_repo_name(
    mocker,
    validate_schema_mock_fixture,
    get_ingestion_test_1_schema_fixture,
    get_omixatlas_mock_fixture_polly_services,
):
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()

    mocker.patch(
        polly.omixatlas.__name__ + ".OmixAtlas.validate_schema",
        return_value=validate_schema_mock_fixture,
    )

    # get_omixatlas to give details from omixatlas details from which repo_id is fetched is
    # and compared
    mocker.patch(
        polly_services.polly_services_hlpr.__name__ + ".get_omixatlas",
        return_value=get_omixatlas_mock_fixture_polly_services,
    )

    # repo_key valid not equal to repo identifier in the body
    repo_key = "lib_repo_dev"
    body = get_ingestion_test_1_schema_fixture
    with pytest.raises(
        paramException,
        match=r".* Value of repo_key in the parameter and repo_id in the payload not same.*",
    ):
        omix_obj.update_schema(repo_key, body)


# replace schema tests
# replace schema test 1 -> positive case
def test_replace_schema_positive_case(
    mocker, validate_schema_mock_fixture, capsys, get_ingestion_test_1_schema_fixture
):
    # Doing it on a repo that already exists
    # 1st -> Mock response of `_get_omixatlas()` call
    # inside validate schema -> make a seperate mocked function for that
    mocker.patch(
        polly.omixatlas.__name__ + ".OmixAtlas.validate_schema",
        return_value=validate_schema_mock_fixture,
    )

    # then mocking the response of PUT API CALL for Replace Schema
    Polly.auth(testpolly_token, env="testpolly")
    nobj = omixatlas.OmixAtlas()
    # mocked response with status and no specific value
    # as no specific response is mocked -> generic message will be printed
    response = mocker.patch.object(nobj.session, "put")
    response.return_value.status_code = 200

    # ingestion_test_1
    repo_id = test_const.INGESTION_TEST_1_REPO_ID

    body = get_ingestion_test_1_schema_fixture

    nobj.replace_schema(repo_id, body)
    # when successfully run
    # comparing the print in the function is coming out
    # in the stdout
    captured = capsys.readouterr()
    assert "Schema has no errors\nSchema update is in progress" in captured.out


# replace schema test 2 -> repo_id wrong format
def test_replace_schema_repo_id_wrong_format(get_ingestion_test_1_schema_fixture):
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    repo_id = [test_const.INGESTION_TEST_1_REPO_ID]
    body = get_ingestion_test_1_schema_fixture

    with pytest.raises(
        paramException,
        match=r".should be str or int",
    ):
        omix_obj.replace_schema(repo_id, body)


# replace schema test 3 -> body wrong format
def test_replace_schema_body_wrong_format():
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()
    repo_id = test_const.INGESTION_TEST_1_REPO_ID
    body = "abcd"

    with pytest.raises(
        paramException,
        match=r"body should not be empty and it should be of type dict",
    ):
        omix_obj.replace_schema(repo_id, body)


# incorrect repo_key -> repo_id
def test_replace_schema_wrong_repo_key_argument(
    mocker, validate_schema_mock_fixture, get_ingestion_test_1_schema_fixture
):
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()

    mocker.patch(
        polly.omixatlas.__name__ + ".OmixAtlas.validate_schema",
        return_value=validate_schema_mock_fixture,
    )

    # wrong repo key
    repo_key = "12345"
    body = get_ingestion_test_1_schema_fixture
    with pytest.raises(
        paramException,
        match=r".* Value of repo_key in the parameter and repo_id in the payload not same.*",
    ):
        omix_obj.replace_schema(repo_key, body)


# incorrect repo_key -> repo name
def test_replace_schema_wrong_repo_key_argument_repo_name(
    mocker,
    validate_schema_mock_fixture,
    get_ingestion_test_1_schema_fixture,
    get_omixatlas_mock_fixture_polly_services,
):
    Polly.auth(testpolly_token, env="testpolly")
    omix_obj = omixatlas.OmixAtlas()

    mocker.patch(
        polly.omixatlas.__name__ + ".OmixAtlas.validate_schema",
        return_value=validate_schema_mock_fixture,
    )

    # get_omixatlas to give details from omixatlas details from which repo_id is fetched is
    # and compared
    mocker.patch(
        polly_services.polly_services_hlpr.__name__ + ".get_omixatlas",
        return_value=get_omixatlas_mock_fixture_polly_services,
    )

    # repo_key valid not equal to repo identifier in the body
    repo_key = "lib_repo_dev"
    body = get_ingestion_test_1_schema_fixture
    with pytest.raises(
        paramException,
        match=r".* Value of repo_key in the parameter and repo_id in the payload not same.*",
    ):
        omix_obj.replace_schema(repo_key, body)


def test_check_omixatlas_status(mocker, capsys, get_omixatlas_mock_fixture):
    Polly.auth(testpolly_token, env="testpolly")
    obj = omixatlas.OmixAtlas()
    # when the repo is not locked
    mocker.patch(
        polly.omixatlas.__name__ + ".OmixAtlas._get_omixatlas",
        return_value=get_omixatlas_mock_fixture,
    )
    repo_name = INGESTION_TEST_1_REPO_ID
    result = obj.check_omixatlas_status(repo_name)
    captured = capsys.readouterr()
    assert isinstance(result, bool)
    assert result is False
    assert (
        "is not locked. All operations on the omixatlas are permitted." in captured.out
    )

    # when the repo is  locked
    # updating the reponse to have a locked status
    get_omixatlas_mock_fixture["data"]["attributes"]["is_locked"] = True
    mocker.patch(
        polly.omixatlas.__name__ + ".OmixAtlas._get_omixatlas",
        return_value=get_omixatlas_mock_fixture,
    )
    result = obj.check_omixatlas_status(repo_name)
    captured = capsys.readouterr()
    assert isinstance(result, bool)
    assert result is True
    assert "is locked" in captured.out

    # when the there is no info on the loc status in the
    # response from the API
    get_omixatlas_mock_fixture["data"]["attributes"]["is_locked"] = None
    mocker.patch(
        polly.omixatlas.__name__ + ".OmixAtlas._get_omixatlas",
        return_value=get_omixatlas_mock_fixture,
    )
    result = obj.check_omixatlas_status(repo_name)
    captured = capsys.readouterr()
    assert result is None
    assert "Unable to fetch the lock status" in captured.out

    # tests for parameter exception
    # passing repo_id as a dict instead of valid str or int
    invalid_repo_name_type = {"repo": "1234"}
    with pytest.raises(
        paramException,
        match=r"paramException \(parameter error\): Argument 'repo_key' is either empty or invalid.*",
    ):
        obj.check_omixatlas_status(invalid_repo_name_type)

    invalid_repo_name = "1234abcd"
    mocker.patch(
        polly.omixatlas.__name__ + ".OmixAtlas._get_omixatlas",
        side_effect=apiErrorException("ERROR"),
    )
    obj.check_omixatlas_status(invalid_repo_name)
    captured = capsys.readouterr()
    assert (
        f" Error in getting the lock status for omixatlas: {invalid_repo_name}."
        in captured.out
    )


def test_download_data_file(mocker, capsys):
    # test for the _download_data_file function that is internally called by the download_dataset() fucntion.
    # the _download_data_funtion calls the download_data() to get the url for the file to be downloaded.
    # here we are mocking the download_data() where it returns a json with the download url and other details of the file
    # to be downloaded - this is a positive scenario
    mocker.patch(
        polly.omixatlas.__name__ + ".OmixAtlas.download_data",
        return_value=test_const.MOCK_RESPONSE_DOWNLOAD_DATA,
    )
    obj = omixatlas.OmixAtlas(testpolly_token, env="testpolly")
    repo_key = "1654268055800"
    dataset_id = ["GSE1234_GPL1234"]
    folder_path = os.getcwd()
    obj._download_data_file(repo_key, dataset_id, folder_path)
    full_path = os.getcwd() + "/" + "tcga_LIHC_Copy_Number_Segment_TCGA-FV-A3R2-01A.gct"
    assert os.path.exists(full_path) is True
    os.remove(full_path)

    # here we are mocking the response of download_data() while fetching the URL such that some exception is raised.
    # in that case, we are expecting that when we call _download_data_file there would be an print stating that
    # "Download of this file will be skipped" -> this is the negative scenario

    mocker.patch(
        polly.omixatlas.__name__ + ".OmixAtlas.download_data",
        side_effect=apiErrorException("ERROR"),
    )
    obj._download_data_file(repo_key, dataset_id, folder_path)
    captured = capsys.readouterr()
    assert (
        "error in getting the download url for dataset_id: ['GSE1234_GPL1234']. Download of this file will be skipped"
        in captured.out
    )


def test_download_dataset(mocker):
    # mocking _download_data_file function (called internally by the download_dataset) to return true
    # that would mean that the file has been downloaded successfully.
    # here we are asserting that no exceptions were raised when the download_dataset function was called.
    # futher we also test for the paramter checks
    mocker.patch(
        polly.omixatlas.__name__ + ".OmixAtlas._download_data_file",
        return_value=True,
    )
    obj = omixatlas.OmixAtlas(testpolly_token, env="testpolly")
    repo_key = "1654268055800"
    dataset_id = ["GSE1234_GPL5678", "GSE12345_GPL1234", "GSE1234_GPL15674"]
    folder_path = os.getcwd()
    try:
        obj.download_dataset(repo_key, dataset_id, folder_path)
    except Exception as exc:
        assert False, f"{exc}"

    invalid_repo_key_type = 1234
    invalid_dataset_id_type = "GSE100003_GPL15207"
    invalid_folder_path = "random/folder_path"

    with pytest.raises(
        paramException,
        match=r"paramException \(parameter error\): repo_key \(either id or name\) is required and should be a string",
    ):
        obj.download_dataset(invalid_repo_key_type, dataset_id, folder_path)

    with pytest.raises(
        paramException,
        match=r"paramException \(parameter error\): dataset_ids should be list of strings*",
    ):
        obj.download_dataset(repo_key, invalid_dataset_id_type, folder_path)

    with pytest.raises(
        paramException,
        match=r"paramException \(parameter error\): folder_path if provided should be a string and a valid folder path.*",
    ):
        obj.download_dataset(repo_key, dataset_id, invalid_folder_path)
