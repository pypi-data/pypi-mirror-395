DATA_TYPES = {
    "Mutation": [
        {
            "format": ["maf"],
            "supported_repo": [
                {
                    "name": "cbioportal",
                    "header_mapping": {
                        "gene": "Hugo_Symbol",
                        "chr": "Chromosome",
                        "startPosition": "Start_Position",
                        "endPosition": "End_Position",
                        "referenceAllele": "Reference_Allele",
                        "variantAllele": "Tumor_Seq_Allele2",
                        "mutationType": "Variant_Classification",
                        "variantType": "Variant_Type",
                        "uniqueSampleKey": "Tumor_Sample_Barcode",
                    },
                },
                {"name": "tcga", "header_mapping": {}},
            ],
        }
    ]
}
COHORT_SUPPORTED_DATATYPES = ["Raw Counts Transcriptomics"]
COHORT_SUPPORTED_DATASOURCES = ["GEO"]
COHORT_LIST_COLS_TO_DROP = [
    "sample_characteristics",
    "timestamp_",
    "curated_control",
    "curated_cohort_id",
    "curated_cohort_name",
    "curated_is_control",
    "curated_max_age",
    "curated_min_age",
    "curated_age_unit",
]
MA_SUPPORTED_REPO = ["geo_transcriptomics_omixatlas"]

# validation flow files url github
VALIDATION_FLOW_FILES_URL = (
    "https://raw.githubusercontent.com/ElucidataInc/PublicAssets/master/"
    + "internal-user/validation_full_flow_files"
)

# POLLY_PY_TEST_FILES_URL = (
#     "https://raw.githubusercontent.com/ElucidataInc/PublicAssets/master/"
#     + "internal-user/polly_py_test_files"
# )

# # repo id used in the tests
# INGESTION_TEST_1_REPO_ID = "1654268055800"

# endpoints
CONSTANTS_ENDPOINT = "/constants"
REPOSITORIES_ENDPOINT = "/repositories"
REPOSITORY_PACKAGE_ENDPOINT = REPOSITORIES_ENDPOINT + "/{}/packages"
IMAGE_URL_ENDPOINT = (
    "https://elucidatainc.github.io/PublicAssets/discover-fe-assets/omixatlas_hex.svg"
)

# statuscodes
OK = 200
CREATED = 201
COMPUTE_ENV_VARIABLE = "POLLY_TYPE"
UPLOAD_URL_CREATED = 204
UPLOAD_ERROR_CODE = 400

# Multipart S3 upload parameters
KB = 1024
MB = KB * KB
GB = 1024 * MB
SMALL_FILE_SIZE = 20 * GB
MEDIUM_FILE_SIZE = 40 * GB

MULTIPART_THRESHOLD = 25 * MB
MAX_CONCURRENCY = 32

# Chunksize for file less than 20 gb
MULTIPART_CHUNKSIZE_SMALL_FILE_SIZE = 25 * MB
IO_CHUNKSIZE_SMALL_FILE_SIZE = 25 * MB

# Chunksize for file more than 20gb and less than 40gb
MULTIPART_CHUNKSIZE_MEDIUM_FILE_SIZE = 50 * MB
IO_CHUNKSIZE_MEDIUM_FILE_SIZE = 50 * MB

# Chunksize for file more than 40gb
MULTIPART_CHUNKSIZE_LARGE_FILE_SIZE = 100 * MB
IO_CHUNKSIZE_LARGE_FILE_SIZE = 100 * MB

# S3 Exceptions
EXPIRED_TOKEN = "ExpiredToken"

GETTING_UPLOAD_URLS_PAYLOAD = {"data": {"type": "files", "attributes": {"folder": ""}}}

INGESTION_LEVEL_METADATA = {
    "id": "metadata/ingestion",
    "type": "ingestion_metadata",
    "attributes": {
        "ignore": "false",
        "urgent": "true",
        "v1_infra": False,
        "priority": "low",
    },
}

METADATA = {"data": []}

GET_SCHEMA_RETURN_TYPE_VALS = ["dataframe", "dict"]

COMBINED_METADATA_FILE_NAME = "combined_metadata.json"

FILES_PATH_FORMAT = {"metadata": "<metadata_path>", "data": "<data_path>"}

INGESTION_FILES_PATH_DIR_NAMES = ["metadata", "data"]

SCHEMA_CONFIG_KEY_NAMES = ["source", "datatype"]

VALIDATION_SCOPE_CONSTANTS = ["basic", "advanced"]

SCHEMA_CONFIG_FORMAT = {"source": "<source_name", "datatype": "<datatype_name>"}

FORMATTED_METADATA = {"id": "", "type": "", "attributes": {}}

FILE_FORMAT_CONSTANTS_URL = (
    "https://elucidatainc.github.io/PublicAssets/file_format_constants.txt"
)

VALIDATION_STATUS_FILE_NAME = "validation_status.txt"

# this constant is used as a base url for getting data files for
# testing ingestion functionality
BASE_TEST_FORMAT_CONSTANTS_URL = (
    "https://raw.githubusercontent.com/ElucidataInc/PublicAssets/master/"
    + "internal-user/add_dataset_test_file"
)

ENCRYPTION_KEY_URL = (
    "https://raw.githubusercontent.com/ElucidataInc/PublicAssets/"
    + "56440d3be03afe700af65d41e7fdf610befccce9/key/Encryptionkey.key"
)

COMPRESSION_TYPES = [
    ".br," ".bz2",
    ".bz",
    ".gz",
    ".lz",
    ".lz4",
    ".sz",
    ".rz",
    ".xz",
    ".zip",
    ".tar",
    ".bgz",
]

FILE_FORMAT_CONSTANTS = {
    "data": [
        ".gct",
        ".vcf",
        ".h5ad",
        ".mmcif",
        ".h5seurat",
        ".biom",
        ".zip",
        ".fs",
        ".tar.gz",
        ".fcs",
        ".vcf.bgz",
        ".gct.bz",
        ".csv",
    ],
    "metadata": [".json", ".jpco"],
}
NOT_NEEDED_SCHEMA_FIELDS = [
    "is_current",
    "data_table_version",
    "data_table_name",
    "timestamp_",
]


OMIXATLAS_CATEGORY_VALS = ["private", "public", "diy_poa"]
OMIXATLAS_DATA_TYPE_VALS = ["single_cell", "bulk_rna_seq"]

VALIDATION_LEVEL_CONSTANTS = {"advanced": "value", "basic": "schema"}


SCHEMA_WRITE_SUCCESS = (
    "Job for your schema update has been recorded. Depending on the changes,"
    + "minor updates or complete reindexing will be performed for you data. The repository will be locked for the "
    + "duration of this update. Please refer to the ingestion monitoring dashboard for visibility on this process."
)

MOVE_DATA_SUCCESS = (
    "Your ingestion request is successfully logged. "
    + "You can go to ingestion monitoring dashboard for tracking it's status."
)

SCHEMA_INSERT_SUCCESS = "Schema has been Inserted. Please use get_schema functionality to get the inserted schema."

DATA_COMMIT_MESSAGE = (
    "Your request is successfully logged. "
    + "You can go to ingestion monitoring dashboard for tracking it's status."
)

WAIT_FOR_COMMIT = (
    "Please wait for 30 seconds while your ingestion request is getting logged."
)

WAIT_FOR_COMMIT_DELETE = (
    "Please wait for 30 seconds while your deletion request is getting logged."
)


SCHEMA_UPDATE_SUCCESS = (
    "The schema update is in progress. It should only take a few minutes and you can track the status"
    + " of this update in the ingestion monitoring dashboard. The repository will be locked for this time "
    + " and any further changes in the schema or properties of omixatlas can not be done."
)

SCHEMA_REINGEST_SUCCESS = (
    "The data needs to be re-ingested to accommodate the changes made in the schema. This may "
    + "take from a few minutes to a few hours depending on the number of datasets in the atlas. The"
    + " repository will be locked for this time and any further changes in the schema or properties of "
    + " omixatlas can not be done. Please refer to the ingestion monitoring dashboard to check the"
    + " status of re-indexing."
)

SCHEMA_NO_CHANGE_SUCCESS = (
    "Schema has been updated. Use get schema to view the updated schema"
)

SCHEMA_UPDATE_GENERIC_MSG = "Schema update is in progress. Please refer to ingestion monitoring dashboard for more details."

SCHEMA_REPLACE_GENERIC_MSG = "Schema replace is in progress. Please refer to ingestion monitoring dashboard for more details."

SCHEMA_UPDATE = "schema_update"
SCHEMA_REINGESTION = "reingestion"
SCHEMA_NO_CHANGE = "no_change"

SCHEMA_VERDICT_DICT = {
    "schema_update": SCHEMA_UPDATE_SUCCESS,
    "reingestion": SCHEMA_REINGEST_SUCCESS,
    "no_change": SCHEMA_NO_CHANGE_SUCCESS,
}

VALIDATION_NOT_EXECUTED = (
    "Validation not executed on any of the metadata files.  "
    + "Possible reasons to help you troubleshoot :-"
    + "\n"
    + "All the metadata file passed may have `validate flag in the `__index__` dict to be "
    + "false. Plese set them to true for the files which needs to be validated."
)

DELETION_OPERATION_UNSUCCESSFUL_FOR_ALL_DATASET_IDS = (
    "Files not deleted. Possible reasons to help you troubleshoot :- "
    + "\n"
    + "1. All the datasets passed to delete might not be "
    + "present in the Omixatlas. Please check warning message logged during execution. "
    + "\n"
    + "2. Paths passed for dataset id may be wrong for all the "
    + "dataset ids. Please correct them and try again. Use get_all_file_paths function to "
    + "to get all file_paths corresponding to a dataset_id in Omixatlas. "
    + "\n"
    + "3. Dataset_id was not passed in the list of dataset_ids to be deleted. "
    + "\n"
    + "In case of any other queries, please connect with polly.support@elucidata.io"
)

FIELD_NAME_LOC = "field_name"

DDL_CONST_LIST = [
    "ALL",
    "ALTER",
    "AND",
    "ARRAY",
    "AS",
    "AUTHORIZATION",
    "BETWEEN",
    "BIGINT",
    "BINARY",
    "BOOLEAN",
    "BOTH",
    "BY",
    "CASE",
    "CASHE",
    "CAST",
    "CHAR",
    "COLUMN",
    "CONF",
    "CONSTRAINT",
    "COMMIT",
    "CREATE",
    "CROSS",
    "CUBE",
    "CURRENT",
    "CURRENT_DATE",
    "CURRENT_TIMESTAMP",
    "CURSOR",
    "DATABASE",
    "DATE",
    "DAYOFWEEK",
    "DECIMAL",
    "DELETE",
    "DESCRIBE",
    "DISTINCT",
    "DOUBLE",
    "DROP",
    "ELSE",
    "END",
    "EXCHANGE",
    "EXISTS",
    "EXTENDED",
    "EXTERNAL",
    "EXTRACT",
    "FALSE",
    "FETCH",
    "FLOAT",
    "FLOOR",
    "FOLLOWING",
    "FOR",
    "FOREIGN",
    "FROM",
    "FULL",
    "FUNCTION",
    "GRANT",
    "GROUP",
    "GROUPING",
    "HAVING",
    "IF",
    "IMPORT",
    "IN",
    "INNER",
    "INSERT",
    "INT",
    "INTEGER",
    "INTERSECT",
    "INTERVAL",
    "INTO",
    "IS",
    "JOIN",
    "LATERAL",
    "LEFT",
    "LESS",
    "LIKE",
    "LOCAL",
    "MACRO",
    "MAP",
    "MORE",
    "NONE",
    "NOT",
    "NULL",
    "NUMERIC",
    "OF",
    "ON",
    "ONLY",
    "OR",
    "ORDER",
    "OUT",
    "OUTER",
    "OVER",
    "PARTIALSCAN",
    "PARTITION",
    "PERCENT",
    "PRECEDING",
    "PRECISION",
    "PRESERVE",
    "PRIMARY",
    "PROCEDURE",
    "RANGE",
    "READS",
    "REDUCE",
    "REGEXP",
    "REFERENCES",
    "REVOKE",
    "RIGHT",
    "RLIKE",
    "ROLLBACK",
    "ROLLUP",
    "ROW",
    "ROWS",
    "SELECT",
    "SET",
    "SMALLINT",
    "START",
    "TABLE",
    "TABLESAMPLE",
    "THEN",
    "TIME",
    "TIMESTAMP",
    "TO",
    "TRANSFORM",
    "TRIGGER",
    "TRUE",
    "TRUNCATE",
    "UNBOUNDED",
    "UNION",
    "UNIQUEJOIN",
    "UPDATE",
    "USER",
    "USING",
    "UTC_TIMESTAMP",
    "VALUES",
    "VARCHAR",
    "VIEWS",
    "WHEN",
    "WHERE",
    "WINDOW",
    "WITH",
]

DML_CONST_LIST = [
    "ALTER",
    "AND",
    "AS",
    "BETWEEN",
    "BY",
    "CASE",
    "CAST",
    "CONSTRAINT",
    "CREATE",
    "CROSS",
    "CUBE",
    "CURRENT_DATE",
    "CURRENT_PATH",
    "CURRENT_TIME",
    "CURRENT_TIMESTAMP",
    "CURRENT_USER",
    "DEALLOCATE",
    "DELETE",
    "DESCRIBE",
    "DISTINCT",
    "DROP",
    "ELSE",
    "END",
    "ESCAPE",
    "EXCEPT",
    "EXECUTE",
    "EXISTS",
    "EXTRACT",
    "FALSE",
    "FIRST",
    "FOR",
    "FROM",
    "FULL",
    "GROUP",
    "GROUPING",
    "HAVING",
    "IN",
    "INNER",
    "INSERT",
    "INTERSECT",
    "INTO",
    "IS",
    "JOIN",
    "LAST",
    "LEFT",
    "LIKE",
    "LOCALTIME",
    "LOCALTIMESTAMP",
    "NATURAL",
    "NORMALIZE",
    "NOT",
    "NULL",
    "OF",
    "ON",
    "OR",
    "ORDER",
    "OUTER",
    "PREPARE",
    "RECURSIVE",
    "RIGHT",
    "ROLLUP",
    "SELECT",
    "TABLE",
    "THEN",
    "TRUE",
    "UNESCAPE",
    "UNION",
    "UNNEST",
    "USING",
    "VALUES",
    "WHEN",
    "WHERE",
    "WITH",
]

# curation_library constants
SUPPORTED_ENTITY_TYPES = [
    "disease",
    "drug",
    "species",
    "tissue",
    "cell_type",
    "cell_line",
    "gene",
]

CURATION_COHORT_CACHE = "./.cache/"

SCHEMA_VALIDATION_BASE_URL = (
    "https://raw.githubusercontent.com/ElucidataInc/PublicAssets/master/"
    + "internal-user/schema_validation"
)

SCHEMA_VALIDATION = {
    "empty_repo_id": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_empty_repo_id.json",
    "missing_repo_id": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_missing_repo_id.json",
    "missing_schema_key": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_missing_schema_key.json",
    "wrong_repo_id": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_wrong_repo_id.json",
    "field_name_cap": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_field_name_capital.json",
    "field_name_underscore": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_field_name_with_underscore.json",
    "field_name_resv_keyword": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_field_name_with_resv_keyword.json",
    "original_name_empty": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_original_name_empty.json",
    "original_name_grtr_50": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_original_name_gtr_50.json",
    "type_cosco": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_type_cosco.json",
    "is_arr_str": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_is_arr_str.json",
    "is_keyword_str": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_is_keywrd_str.json",
    "filter_size_less": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_filter_size_less.json",
    "filter_size_greater": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_filter_size_greater.json",
    "display_name_empty": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_display_name_empty.json",
    "display_name_grtr_50": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_display_name_grtr_50.json",
    "is_keywrd_is_filter": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_is_keywrd_is_filter.json",
    "is_keywrd_is_ontology": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_field_name_is_filter_is_ontology.json",
    "positive_case": f"{SCHEMA_VALIDATION_BASE_URL}/positive_case.json",
    "original_name_int": f"{SCHEMA_VALIDATION_BASE_URL}/original_name_int.json",
    "filter_size_str": f"{SCHEMA_VALIDATION_BASE_URL}/filter_size_str.json",
    "repo_id_and_id_diff": f"{SCHEMA_VALIDATION_BASE_URL}/demo_oa_2_repo_id_and_id_diff.json",
}

MIN_REQUIRED_KEYS_FOR_JOBS = ["cpu", "memory", "machineType", "image", "tag", "name"]

MACHINES_FOR_JOBS = (
    {
        "gp": "4 vCPU, 16GB RAM",
        "ci2xlarge": "16 vCPU, 32GB RAM",
        "ci3xlarge": "36 vCPU, 72GB RAM",
        "mi2xlarge": "4 vCPU, 32GB RAM",
        "mi3xlarge": "8 vCPU, 64GB RAM",
        "mi4xlarge": "16 vCPU, 122GB RAM",
        "mi5xlarge": "32 vCPU, 250GB RAM",
        "mi6xlarge": "64 vCPU, 500GB RAM",
        "mi7xlarge": "64 vCPU, 970GB RAM",
        "mix5xlarge": "16vCPU, 512GB RAM",
        "mix6xlarge": "24vCPU, 768GB RAM",
        "mix7xlarge": "64vCPU, 1024GB RAM",
        "gpusmall": "1 GPU, 4 vCPU, 16GB RAM",
        "gpumedium": "4 GPU, 32 vCPU, 240GB RAM",
        "gpularge": "8 GPU, 64 vCPU, 480GB RAM",
        "gpuxlarge": "8 GPU, 96 vCPU, 760GB RAM",
    },
)

DATA_LOG_MODES = ["latest", "all"]
MIXPANEL_KEY = "91fa77fcf07f7b672b5c5c6c09d8a14c"

PROD_ENV_NAME = "polly"

POLLY_PYTHON_PYPI_URL = "https://pypi.python.org/pypi/polly-python/json"
ERROR_MSG_GET_METADATA = "Argument 'table_name' not valid, please query 'SHOW TABLES IN repo_name' \
using query_metadata function and pick the appropriate table name you want the metadata \
for Example: samples, features, samples_singlecell etc. \
Currently, get_metadata works only for sample level table of gct and h5ad files. \
If you want to get metadata for other tables, please contact polly.support@elucidata.io"

TABLE_NAME_SAMPLE_LEVEL_INDEX_MAP = {
    "samples": "gct_col_metadata",
    "samples_singlecell": "h5ad_col_metadata",
}
POLLY_PYTHON_LATEST_VERSION_FILE = (
    "https://elucidatainc.github.io/PublicAssets/polly_python_latest_version.txt"
)

QUERY_MAX_RECORD_SIZE = 20000
# this control lever is for testing as data is less on testpolly
DEFAULT_PAGE_SIZE_LIST_FILES = 2600

DEFAULT_PAGE_SIZE_LIST_FILES_KEY_NAME = "default_page_size_list_files"

PAGE_REDUCTION_PERCENTAGE_LIST_FILES = 20

PAGE_REDUCTION_PERCENTAGE_LIST_FILES_KEY_NAME = "page_reduction_percentage_list_files"

LIST_FILE_API_CONTROL_LEVER_LINK = (
    "https://elucidatainc.github.io/PublicAssets/list_files_api_control_lever/"
    + "list_files_control_lever.json"
)
QUERY_API_V2 = "v2"

REPOSITORY_PAYLOAD = {
    "data": {
        "type": "repositories",
        "attributes": {
            "frontend_info": {
                "description": "<DESCRIPTION>",
                "display_name": "<REPO_DISPLAY_NAME>",
                "explorer_enabled": True,
                "initials": "<INITIALS>",
            },
            "indexes": {
                "csv": "<REPO_NAME>_csv",
                "files": "<REPO_NAME>_files",
                "gct_data": "<REPO_NAME>_gct_data",
                "gct_metadata": "<REPO_NAME>_gct_metadata",
                "h5ad_data": "<REPO_NAME>_h5ad_data",
                "h5ad_metadata": "<REPO_NAME>_h5ad_metadata",
                "ipynb": "<REPO_NAME>_ipynb",
                "json": "<REPO_NAME>_json",
            },
            "repo_name": "<REPO_NAME>",
            "category": "<CATEGORY>",
        },
    }
}
