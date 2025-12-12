POLLY_PY_TEST_FILES_URL = (
    "https://raw.githubusercontent.com/ElucidataInc/PublicAssets/master/"
    + "internal-user/polly_py_test_files"
)
# repo id used in the tests
INGESTION_TEST_1_REPO_ID = "1654268055800"

MOCK_RESPONSE_DOWNLOAD_DATA = {
    "data": {
        "attributes": {
            "last-modified": "2022-11-09 10:46:07.000000",
            "size": "912.43 KB",
            "download_url": "https://github.com/ElucidataInc/PublicAssets/blob/master/internal-user/add_dataset_test_file/"
            + "data_file/tcga_LIHC_Copy_Number_Segment_TCGA-FV-A3R2-01A.gct",
        }
    }
}

MOCK_403_ACCESS_DENIED_RESPONSE = {
    "errors": [
        {
            "status": "403",
            "code": "forbidden",
            "title": "Access denied",
            "detail": "Access denied for requested resource",
        }
    ]
}

MOCK_REPO_NOT_FOUND_RESPONSE = {
    "errors": [
        {
            "status": "404",
            "code": "resource_not_found",
            "title": "Data not found not found",
            "detail": "Repository with repo key not found",
        }
    ]
}
FETCH_WORKSPACES_MOCKED_RESPONSE = [
    {
        "id": 10,
        "name": "document_workspace",
        "status": "active",
        "description": None,
        "last_modified": "2023-02-07 11:38:28",
        "tag_names": [],
        "favourite": False,
        "watch": False,
    },
    {
        "id": 10,
        "name": "schema backup ",
        "status": "active",
        "description": "",
        "last_modified": "2023-02-07 13:32:34",
        "tag_names": [],
        "favourite": False,
        "watch": False,
    },
]

WORKSPACE_CREATE_COPY_POST_REQUEST_RESPONSE = {
    "data": [
        {
            "type": "files",
            "id": "id",
            "attributes": {
                "body": "Workspace_copy started, You will be notified upon completion."
            },
        }
    ],
    "included": [
        {
            "type": "file",
            "id": "id",
            "attributes": {
                "file_name": "file_name",
                "s3_key": "s3_key",
                "operation_id": "0a0-3986-4d43-94be-dd787b2f5de8",
            },
            "links": {"self": "/async_operations/24e610a0-3986-4d43-94be-dd787b2f5de8"},
        }
    ],
}

WORKSPACE_CREATE_COPY_GET_REQUEST_RESPONSE = {
    "status": 200,
    "primary_data": {
        "user_id": 1709822200,
        "action": "WORKSPACE_COPY",
        "destination_key": "8836/autostop.py.rename",
        "source_key": "6552/autostop.py.rename",
        "status": "COMPLETE",
        "operation_id": "f175bba1-ec17-4354-a7df-90f46e0ec740",
        "created_timestamp": 1724312817,
        "modified_timestamp": 1724312817,
        "type": "file",
    },
}

WORKSPACE_RESPONSE_JSON = [{"key": "value"}]

SAMPLE_QUERY = "SELECT * FROM sc_data_lake.features_singlecell LIMIT 100"

MOCKED_DICT_RESPONSE = {
    "data": [
        {
            "repo_id": "1687428192072",
            "repo_name": "new_omix_for_refac_3",
            "indexes": {},
            "v2_indexes": {},
            "sources": [],
            "datatypes": [],
            "dataset_count": 0,
            "disease_count": 0,
            "tissue_count": 0,
            "organism_count": 0,
            "cell_line_count": 0,
            "cell_type_count": 0,
            "drug_count": 0,
            "data_type_count": 0,
            "data_source_count": 0,
            "sample_count": 0,
            "normal_sample_count": 0,
        },
        {
            "repo_id": "1687428145396",
            "repo_name": "new_omix_for_refac_2",
            "indexes": {},
            "v2_indexes": {},
            "sources": [],
            "datatypes": [],
            "dataset_count": 0,
            "disease_count": 0,
            "tissue_count": 0,
            "organism_count": 0,
            "cell_line_count": 0,
            "cell_type_count": 0,
            "drug_count": 0,
            "data_type_count": 0,
            "data_source_count": 0,
            "sample_count": 0,
            "normal_sample_count": 0,
        },
    ]
}


# Pipelines
MOCKED_LIST_RESPONSE = {
    "data": [
        {
            "id": "ce03e312-e9cf-46f0-985a-e14f93066cd3",
            "type": "pipelines",
            "attributes": {
                "name": "play",
                "display_name": "Play",
                "description": "A simple test PWL pipeline",
                "executor": "pwl",
                "deployment_stage": "dev",
                "parameter_schema": {
                    "type": "object",
                    "allOf": [{"$ref": "#/definitions/input_counts"}],
                    "title": "Play Pipeline Parameters",
                    "$schema": "http://json-schema.org/draft-07/schema",
                    "definitions": {
                        "input_counts": {
                            "type": "object",
                            "required": ["a", "b"],
                            "properties": {
                                "a": {"type": "integer", "description": "Parameter 1"},
                                "b": {"type": "integer", "description": "Parameter 2"},
                            },
                            "description": "Defines the input values to process.",
                        }
                    },
                    "description": "",
                },
                "config": {"infra": {"cpu": 0.5, "memory": 2, "storage": 30}},
                "org_id": "1",
                "user_id": "1643976121",
                "user_name": "some.user@elucidata.io",
                "created_at": 1693220349286,
                "last_updated_at": 1693220349286,
            },
            "links": {
                "self": "/pravaah/orchestration/pipelines/ce03e312-e9cf-46f0-985a-e14f93066cd3"
            },
        }
    ],
    "meta": {"total_count": 1},
    "links": {
        "self": "/pravaah/orchestration/pipelines?page[size]=10&page[after]=0",
    },
}

MOCKED_PIPELINE_GET_RESPONSE = {
    "data": {
        "id": "ce03e312-e9cf-46f0-985a-e14f93066cd3",
        "type": "pipelines",
        "attributes": {
            "name": "play",
            "display_name": "Play",
            "description": "A simple test PWL pipeline",
            "executor": "pwl",
            "deployment_stage": "dev",
            "parameter_schema": {
                "type": "object",
                "allOf": [{"$ref": "#/definitions/input_counts"}],
                "title": "Play Pipeline Parameters",
                "$schema": "http://json-schema.org/draft-07/schema",
                "definitions": {
                    "input_counts": {
                        "type": "object",
                        "required": ["a", "b"],
                        "properties": {
                            "a": {"type": "integer", "description": "Parameter 1"},
                            "b": {"type": "integer", "description": "Parameter 2"},
                        },
                        "description": "Defines the input values to process.",
                    }
                },
                "description": "",
            },
            "config": {"infra": {"cpu": 0.5, "memory": 2, "storage": 30}},
            "org_id": "1",
            "user_id": "16439733612",
            "user_name": "some.user@elucidata.io",
            "created_at": 1693220349286,
            "last_updated_at": 1693220349286,
        },
        "links": {
            "self": "/pravaah/orchestration/pipelines/ce03e312-e9cf-46f0-985a-e14f93066cd3"
        },
    }
}

MOCKED_RESPONSE_DICT = {
    "data": {
        "id": "some-id",
        "type": "pipelines",
        "attributes": {
            "org_id": "1",
            "user_id": "16439733612",
            "user_name": "some.user@elucidata.io",
            "created_at": 1693220349286,
            "last_updated_at": 1693220349286,
        },
        "links": {"self": "/pravaah/orchestration/pipelines/some-id"},
    }
}
