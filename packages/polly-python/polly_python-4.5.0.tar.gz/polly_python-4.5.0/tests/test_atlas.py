import pytest
from unittest.mock import patch, MagicMock
from polly.atlas import Atlas, handle_success_and_error_response, PayloadTooLargeError
from requests.models import Response
from polly.atlas import Table, Column
import requests
from polly.errors import UnauthorizedException, ResourceNotFoundError, BadRequestError


@pytest.fixture
def mock_session():
    """Mock Polly session."""
    with patch("polly.auth.Polly.default_session") as mock_session:
        yield mock_session


@pytest.fixture
def mock_response():
    """Mock response object."""
    response = MagicMock(spec=Response)
    response.status_code = 200
    response.json.return_value = {"data": {"attributes": {"name": "Test Atlas"}}}
    return response


def test_create_atlas(mock_session, mock_response):
    """Test creating an atlas."""
    mock_session.post.return_value = mock_response
    atlas = Atlas.create_atlas(atlas_id="atlas_1", atlas_name="Test Atlas")
    assert atlas.atlas_id == "atlas_1"


def test_delete_atlas(mock_session):
    """Test deleting an atlas."""
    mock_session.delete.return_value = MagicMock(status_code=204)
    Atlas.delete_atlas(atlas_id="atlas_1")
    mock_session.delete.assert_called_once()


def test_atlas_exists(mock_session):
    """Test checking if an atlas exists."""
    mock_response = MagicMock(status_code=200)
    mock_response.json.return_value = {"data": {"id": "atlas_1"}}
    mock_session.get.return_value = mock_response

    with patch.object(Atlas, "list_tables", return_value=[]):
        atlas = Atlas(atlas_id="atlas_1")
        assert atlas.exists() is True

        mock_response.json.return_value = {"data": {"id": "wrong_id"}}
        assert atlas.exists() is False

        mock_session.get.side_effect = ResourceNotFoundError("Resource not found")

        with pytest.raises(ResourceNotFoundError):
            atlas.exists()


def test_list_atlases(mock_session):
    """Test listing atlases."""
    mock_session.get.return_value = MagicMock(
        status_code=200,
        json=lambda: {
            "data": [
                {
                    "id": "atlas_1",
                    "attributes": {
                        "name": "Test Atlas",
                        "columns": [
                            {"column_name": "patient_id", "data_type": "VARCHAR"}
                        ],
                    },
                }
            ]
        },
    )

    atlases = Atlas.list_atlases()

    assert isinstance(atlases, list)
    assert len(atlases) > 0
    assert atlases[0].atlas_id == "atlas_1"


def test_get_name(mock_session, mock_response):
    """Test getting an atlas name."""
    atlas = Atlas(atlas_id="atlas_1")
    mock_session.get.return_value = mock_response
    name = atlas.get_name()
    assert name == "Test Atlas"


def test_handle_payload_too_large():
    """Test handling payload too large error."""
    response = MagicMock(spec=Response)
    response.status_code = 413
    with pytest.raises(PayloadTooLargeError):
        handle_success_and_error_response(response)


def test_create_atlas_404(mock_session):
    """Test creating an atlas when the server responds with 404."""
    mock_session.post.return_value = MagicMock(status_code=404)
    with pytest.raises(Exception):
        Atlas.create_atlas(atlas_id="atlas_1", atlas_name="Test Atlas")


def test_create_atlas_missing_parameters(mock_session):
    """Test atlas creation with missing parameters."""
    with pytest.raises(TypeError):
        Atlas.create_atlas(atlas_name="Test Atlas")


def test_create_atlas_invalid_response(mock_session):
    """Test atlas creation with invalid response."""
    mock_session.post.return_value = MagicMock(status_code=500)
    mock_session.post.return_value.raise_for_status.side_effect = (
        requests.exceptions.HTTPError
    )


def test_delete_atlas_invalid_status(mock_session):
    """Test deleting an atlas with an invalid response."""
    mock_session.delete.return_value = MagicMock(status_code=400)
    with pytest.raises(Exception):
        Atlas.delete_atlas(atlas_id="atlas_1")


def test_list_atlases_empty(mock_session):
    """Test listing atlases when no atlases exist."""
    mock_session.get.return_value = MagicMock(
        status_code=200, json=lambda: {"data": []}
    )
    atlases = Atlas.list_atlases()
    assert len(atlases) == 0


def test_get_name_not_found(mock_session):
    """Test getting name of an atlas that doesn't exist."""
    atlas = Atlas(atlas_id="atlas_1")
    mock_session.get.return_value = MagicMock(status_code=404)
    with pytest.raises(Exception):
        atlas.get_name()


def test_delete_column(mock_session):
    """Test deleting a column."""
    mock_get_response = MagicMock()
    mock_get_response.status_code = 200
    mock_get_response.json.return_value = {"data": {"attributes": {"columns": []}}}
    mock_session.get.return_value = mock_get_response

    mock_delete_response = MagicMock()
    mock_delete_response.status_code = 204
    mock_session.delete.return_value = mock_delete_response

    table_instance = Table(atlas_id="atlas_1", table_name="test_table")
    response = table_instance.delete_column(column_name="age")

    assert response is None


def test_list_columns(mock_session):
    """Test listing columns in a table."""
    mock_session.get.return_value = MagicMock(
        status_code=200,
        json=lambda: {
            "data": {
                "attributes": {
                    "columns": [
                        {
                            "column_name": "age",
                            "data_type": "integer",
                        }
                    ]
                }
            }
        },
    )

    table_instance = Table(atlas_id="atlas_1", table_name="patient_table")
    columns = table_instance.list_columns()

    assert len(columns) == 1
    assert columns[0].column_name == "age"
    assert columns[0].data_type == "integer"


def test_get_column_details(mock_session):
    """Test getting details of a column."""
    column = Column(column_name="column_1", data_type="string")

    assert column.column_name == "column_1"
    assert column.data_type == "string"


def test_create_table(mock_session):
    """Test creating a table."""
    mock_session.post.return_value = MagicMock(
        status_code=200,
        json=lambda: {
            "data": {
                "attributes": {
                    "table_name": "Test Table",
                    "columns": [
                        {
                            "column_name": "column_1",
                            "data_type": "text",
                        }
                    ],
                }
            }
        },
    )

    atlas_instance = Atlas(atlas_id="atlas_1")
    columns = [Column(column_name="column_1", data_type="text")]

    table = atlas_instance.create_table(table_name="Test Table", columns=columns)

    assert table is not None
    assert table.table_name == "Test Table"
    assert len(table.columns) == 1
    assert table.columns[0].column_name == "column_1"


def test_delete_table(mock_session):
    """Test deleting a table."""
    mock_session.delete.return_value = MagicMock(status_code=204)

    atlas_instance = Atlas(atlas_id="atlas_1")
    response = atlas_instance.delete_table(table_name="Test Table")
    assert response is None


def test_list_tables(mock_session):
    """Test listing tables in an atlas."""
    mock_session.get.return_value = MagicMock(
        status_code=200,
        json=lambda: {
            "data": [
                {
                    "id": "table_1",
                    "attributes": {
                        "table_name": "Test Table",
                        "columns": [{"column_name": "column_1", "data_type": "text"}],
                    },
                }
            ]
        },
    )

    atlas_instance = Atlas(atlas_id="atlas_1")
    tables = atlas_instance.list_tables()

    assert len(tables) == 1
    assert tables[0].table_name == "Test Table"


def test_get_table_details(mock_session):
    """Test getting details of a table."""
    mock_session.get.return_value = MagicMock(
        status_code=200,
        json=lambda: {
            "data": {
                "attributes": {
                    "name": "Test Table",
                    "columns": [
                        {
                            "column_name": "column_1",
                            "data_type": "text",
                        }
                    ],
                }
            }
        },
    )

    table = Table(atlas_id="atlas_1", table_name="Test Table")

    assert table.table_name == "Test Table"
    assert len(table.columns) == 1
    assert table.columns[0].column_name == "column_1"


def test_handle_not_found(mock_session):
    """Test handling a 404 response."""
    mock_session.get.return_value = MagicMock(status_code=404)
    with pytest.raises(Exception):
        Atlas.get_name(atlas_id="nonexistent_atlas")


def test_handle_bad_request(mock_session):
    """Test handling a 400 Bad Request response."""
    mock_session.post.return_value = MagicMock(status_code=400)
    with pytest.raises(Exception):
        Atlas.create_atlas(atlas_id="atlas_1", atlas_name="Test Atlas")


def test_create_atlas_duplicate(mock_session):
    """Test creating an atlas that already exists."""
    mock_response = MagicMock()
    mock_response.status_code = 409
    mock_response.json.return_value = {"errors": [{"detail": "Atlas already exists"}]}
    mock_session.post.return_value = mock_response

    with pytest.raises(Exception) as exc_info:
        Atlas.create_atlas(atlas_id="atlas_1", atlas_name="Test Atlas")

    assert "Atlas already exists" in str(exc_info.value)


def test_create_table_duplicate(mock_session):
    """Test creating a table that already exists."""
    mock_response = MagicMock()
    mock_response.status_code = 409
    mock_response.json.return_value = {"errors": [{"detail": "Table already exists"}]}
    mock_session.post.return_value = mock_response

    atlas = Atlas(atlas_id="atlas_1")
    with pytest.raises(Exception) as exc_info:
        atlas.create_table(table_name="Test Table", columns=[])

    assert "Table already exists" in str(exc_info.value)


def test_list_tables_empty(mock_session):
    """Test listing tables when no tables exist."""
    mock_session.get.return_value = MagicMock(
        status_code=200, json=lambda: {"data": []}
    )
    atlas = Atlas(atlas_id="atlas_1")
    tables = atlas.list_tables()
    assert tables == []


def test_delete_table_not_found(mock_session):
    """Test deleting a table that does not exist."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.json.return_value = {"errors": [{"detail": "Table not found"}]}

    mock_session.delete.return_value = mock_response

    atlas = Atlas(atlas_id="atlas_1")

    with pytest.raises(Exception, match="Table not found") as exc_info:
        atlas.delete_table(table_name="NonExistentTable")

    assert "Table not found" in str(exc_info.value)


def test_get_table_details_not_found(mock_session):
    """Test getting details of a non-existent table."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.json.return_value = {"errors": [{"detail": "Table not found"}]}
    mock_session.get.return_value = mock_response

    with pytest.raises(ResourceNotFoundError, match="Table not found"):
        Table(atlas_id="atlas_1", table_name="NonExistentTable")


def test_create_column_invalid_data():
    """Test creating a column with invalid data."""
    with pytest.raises(TypeError, match="column_name must be a non-empty text"):
        Column(column_name=None, data_type="text")

    with pytest.raises(TypeError, match="data_type must be a text"):
        Column(column_name="age", data_type=123)


def test_list_columns_empty(mock_session):
    """Test listing columns in a table with no columns."""
    mock_session.get.return_value = MagicMock(
        status_code=200, json=lambda: {"data": {"attributes": {"columns": []}}}
    )
    table = Table(atlas_id="atlas_1", table_name="Test Table")
    columns = table.list_columns()
    assert columns == []


def test_delete_column_not_found(mock_session):
    """Test deleting a column that does not exist."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.json.return_value = {"errors": [{"detail": "Column not found"}]}
    mock_session.get.return_value = mock_response

    with pytest.raises(ResourceNotFoundError, match="Column not found"):
        Table(atlas_id="atlas_1", table_name="Test Table")


def test_delete_atlas_not_found(mock_session):
    """Test deleting an atlas that does not exist."""
    mock_session.delete.return_value = MagicMock(status_code=404)
    with pytest.raises(Exception):
        Atlas.delete_atlas(atlas_id="non_existent_atlas")


def test_list_atlases_unauthorized(mock_session):
    """Test listing atlases without authorization."""
    mock_session.get.return_value = MagicMock(status_code=401)
    with pytest.raises(Exception):
        Atlas.list_atlases()


def test_get_name_unauthorized(mock_session):
    """Test getting an atlas name without authorization."""
    mock_session.get.return_value = MagicMock(status_code=401)
    with pytest.raises(UnauthorizedException):
        atlas = Atlas(atlas_id="atlas_1")
        atlas.get_name()


def test_create_table_unauthorized(mock_session):
    """Test creating a table without authorization."""
    mock_session.post.return_value = MagicMock(status_code=401)
    atlas = Atlas(atlas_id="atlas_1")
    with pytest.raises(Exception):
        atlas.create_table(table_name="Test Table", columns=[])


def test_delete_table_unauthorized(mock_session):
    """Test deleting a table without authorization."""
    mock_session.delete.return_value = MagicMock(status_code=401)
    atlas = Atlas(atlas_id="atlas_1")
    with pytest.raises(Exception):
        atlas.delete_table(table_name="Test Table")


def test_list_columns_unauthorized(mock_session):
    """Test listing columns in a table without authorization."""
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.json.return_value = {
        "errors": [{"detail": "Expired or Invalid Token"}]
    }
    mock_session.get.return_value = mock_response

    with pytest.raises(UnauthorizedException, match="Expired or Invalid Token"):
        Table(atlas_id="atlas_1", table_name="Test Table")


def test_delete_column_unauthorized(mock_session):
    """Test deleting a column without authorization."""
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.json.return_value = {
        "errors": [{"detail": "Expired or Invalid Token"}]
    }
    mock_session.get.return_value = mock_response

    with pytest.raises(UnauthorizedException, match="Expired or Invalid Token"):
        Table(atlas_id="atlas_1", table_name="Test Table")


def test_list_columns_empty_table(mock_session):
    """Test listing columns when no columns exist in the table."""
    mock_session.get.return_value = MagicMock(
        status_code=200, json=lambda: {"data": {"attributes": {"columns": []}}}
    )
    table_instance = Table(atlas_id="atlas_1", table_name="Test Table")
    columns = table_instance.list_columns()
    assert columns == []


def test_create_column_invalid_data_type():
    """Test creating a column with invalid data type."""
    with pytest.raises(TypeError, match="data_type must be a text"):
        Column(column_name="age", data_type=123)


def test_create_column_invalid_column_name():
    """Test creating a column with an invalid column name."""
    with pytest.raises(TypeError, match="column_name must be a non-empty text"):
        Column(column_name=None, data_type="text")


def test_list_atlases_success(mock_session):
    """Test listing atlases when the response is successful (HTTP 200)."""
    mock_session.get.return_value = MagicMock(
        status_code=200,
        json=lambda: {
            "data": [
                {
                    "id": "atlas_1",
                    "attributes": {
                        "name": "Test Atlas",
                        "columns": [{"column_name": "id", "data_type": "integer"}],
                    },
                }
            ]
        },
    )
    atlases = Atlas.list_atlases()

    assert isinstance(atlases, list)
    assert len(atlases) > 0
    assert atlases[0].atlas_id == "atlas_1"


def test_create_table_invalid_name(mock_session):
    """Test creating a table with an invalid name."""
    mock_session.post.return_value = MagicMock(
        status_code=400, json=lambda: {"errors": [{"detail": "Invalid table name"}]}
    )
    atlas_instance = Atlas(atlas_id="atlas_1")
    with pytest.raises(BadRequestError, match="Invalid table name"):
        atlas_instance.create_table(table_name="", columns=[])


@pytest.fixture
def mock_column():
    """Mock Column instance."""
    return Column(column_name="age", data_type="integer")


def test_column_data_type_integer(mock_column):
    """Test setting column with INTEGER data type."""
    assert mock_column.data_type == "integer"


def test_column_data_type_text(mock_column):
    """Test setting column with TEXT data type."""
    mock_column.data_type = "text"
    assert mock_column.data_type == "text"


def test_column_with_json_data_type(mock_session):
    """Test creating a column with JSON data type."""
    column = Column(column_name="settings", data_type="json")
    assert column.data_type == "json"


def test_create_column_with_money_data_type():
    """Test creating a column with MONEY data type."""
    column = Column(column_name="salary", data_type="money")
    assert column.data_type == "money"


def test_add_rows(mock_session):
    """Test the add_rows method."""
    columns = [
        Column(column_name="id", data_type="text", primary_key=True),
        Column(column_name="data", data_type="json"),
    ]

    rows = [
        {
            "id": "1",
            "data": {
                "type": "file",  # Correct type, but missing path in attributes
                "attributes": {"storage": "workspace"},  # location is missing
            },
        },
        {
            "id": "2",
            "data": {
                "type": "file",  # Correct type, missing path again
                "attributes": {"storage": "workspace"},  # location is missing
            },
        },
        {
            "id": "3",
            "data": {
                "type": "image",  # Incorrect type
                "attributes": {
                    "storage": "workspace",
                    "location": "4073/new/img1.jpg",  # Correct path, but type is incorrect
                },
            },
        },
        {"id": "4", "bmi": 25},
    ]

    table = Table(atlas_id="atlas_1", table_name="test_table", columns=columns)

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"attributes": {"rows": rows}}}
    mock_session.post.return_value = mock_response

    with patch("builtins.print") as mock_print:
        table.add_rows(rows)

        mock_print.assert_any_call(
            "Column 'data' of data type JSON has 2 rows with type 'file' "
            "but missing the required attributes 'location' and 'storage'."
        )


def test_update_rows(mock_session):
    """Test the update_rows method."""
    columns = [
        Column(column_name="id", data_type="text", primary_key=True),
        Column(column_name="data", data_type="json"),
    ]

    rows = [
        {
            "id": "1",
            "data": {
                "type": "file",  # Correct type, but missing path in attributes
                "attributes": {"storage": "workspace"},  # location is missing
            },
        },
        {
            "id": "2",
            "data": {
                "type": "file",  # Correct type, missing path again
                "attributes": {"storage": "workspace"},  # location is missing
            },
        },
        {
            "id": "3",
            "data": {
                "type": "image",  # Incorrect type
                "attributes": {
                    "storage": "workspace",
                    "location": "4073/new/img1.jpg",  # Correct path, but type is incorrect
                },
            },
        },
        {"id": "4", "bmi": 25},
    ]

    table = Table(atlas_id="atlas_1", table_name="test_table", columns=columns)

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"attributes": {"rows": rows}}}
    mock_session.post.return_value = mock_response

    with patch("builtins.print") as mock_print:
        table.update_rows(rows)

        mock_print.assert_any_call(
            "Column 'data' of data type JSON has 2 rows with type 'file'"
            " but missing the required attributes 'location' and 'storage'."
        )
