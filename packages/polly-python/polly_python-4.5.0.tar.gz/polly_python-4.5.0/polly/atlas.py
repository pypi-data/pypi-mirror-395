from polly.auth import Polly
from polly.session import PollySession
from polly.errors import (
    ResourceNotFoundError,
    BadRequestError,
    UnauthorizedException,
)
from typing import Callable, List, Optional, Dict, Any, Iterator
from requests import Response
import pandas as pd


class Column:
    """
    Represents a database column with various constraints and properties.

    Parameters:
        column_name (str): The name of the column.
        data_type (str): The data-type of the column (e.g., integer,varchar,date).
        primary_key (Optional[bool], optional): Whether the column is a primary key or not . Defaults to False.
        foreign_key (Optional[bool], optional): Whether the column is a foreign key or not. Defaults to False.
        unique (Optional[bool], optional): Whether the column has a unique constraint. Defaults to False.
        null (Optional[bool], optional): Whether the column allows NULL values. Defaults to True.
        max_length (Optional[int], optional): The maximum length of the column (for data types like varchar,char).
        Defaults to None.
        precision (Optional[int], optional): The precision for numeric types (total number of digits). Defaults to None.
        scale (Optional[int], optional): The scale for numeric types (number of digits to the right of the decimal).
        Defaults to None.
        referenced_column (Optional[str], optional): The name of the referenced column if current column is a foreign key.
        Defaults to None.
        referenced_table (Optional[str], optional): The name of the referenced table if current column is a foreign key.
        Defaults to None.
        on_delete (Optional[str], optional): The ON DELETE strategy for foreign key constraints.Defaults to CASCADE.
        foreign_key_constraint_name (Optional[str], optional): The name of the foreign key constraint. Defaults to None.

    Usage:
        from polly.auth import Polly
        from polly.atlas import Atlas, Table, Column

        Polly.auth("<access_key>")

        column = Column(column_name="user_id", data_type="integer", primary_key=True, unique=True, null=False)

    ## Constraints
    - **Primary Key**: Combines not null + unique , ensuring each row has a unique identifier.
    - **Foreign Key**: Establishes foriegn key relationships between tables.
    - **Unique**: Ensures all values in a column are distinct.
    - **Null**: Ensures if a column can be nullable or not.

    ## Supported Data Types

    ### Numeric Data Types
    - `smallint` (2 bytes): Range -32,768 to 32,767
    - `integer` (4 bytes): Range -2,147,483,648 to 2,147,483,647
    - `bigint` (8 bytes): Range -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807
    - `decimal(p,s) / numeric(p,s)`: Variable storage, exact precision up to 38 digits
    - `real` (4 bytes): Single-precision floating-point numbers
    - `double precision` (8 bytes): Double-precision floating-point numbers
    - `serial / bigserial`: Auto-incrementing integer types
    - `money` (8 bytes): Fixed-point for currency values

    *Note:* `bigserial` can only be used as a primary key column.

            `precision` and `scale` settings are applicable only to decimal and numeric types.




    ### Character Data Types
    - `char(max_length) / character(max_length)`: Fixed-length string (padded with spaces)
    - `varchar(max_length) / character varying(max_length)`: Variable-length string
    - `text`: Unlimited-length string

    *Note:* `max_length` is required for char and varchar. text does not require a length constraint.

    ### Date & Time Data Types
    - `date`: Stores calendar dates (`YYYY-MM-DD`)
    - `time`: Stores time of day (`HH:MM:SS`)
    - `timestamp`/ `timestamp without time zone`: Stores date and time without timezone(`2025-04-03 14:30:00`)
    - `timestamptz`/`timestamp with time zone `: Stores date and time with timezone(`2025-04-03 14:30:00+05:30`)
    - `interval`: Represents a duration (e.g., `"2 hours 30 minutes"`)


    ### Boolean & JSON Data Types
    - `boolean`: Stores `true`, `false` values
    - `json`: Stores structured JSON data
    """

    def __init__(
        self,
        column_name: str,
        data_type: str,
        primary_key: Optional[bool] = False,
        foreign_key: Optional[bool] = False,
        unique: Optional[bool] = False,
        null: Optional[bool] = True,
        max_length: Optional[int] = None,
        precision: Optional[int] = None,
        scale: Optional[int] = None,
        referenced_column: Optional[str] = None,
        referenced_table: Optional[str] = None,
        on_delete: Optional[str] = None,
        foreign_key_constraint_name: Optional[str] = None,
    ):
        """
        Initializes a Column instance with a given name, type, and optional constraint.

        Args:
            column_name: The name of the column
            data_type: The type of the column
            primary_key: Whether the column is a primary key. Defaults to False.
            foreign_key: Whether the column is a foreign key. Defaults to False.
            unique: Whether the column has a unique constraint. Defaults to False.
            null: Whether the column allows NULL values. Defaults to True.
            max_length: The maximum length of the column (for string types). Defaults to None.
            precision: The precision for numeric types. Defaults to None.
            scale: The scale for numeric types. Defaults to None.
            referenced_column: The name of the referenced column (for foreign keys). Defaults to None.
            referenced_table: The name of the referenced table (for foreign keys). Defaults to None.
            on_delete: The ON DELETE action for foreign key constraints. Defaults to None.
            foreign_key_constraint_name: The name of the foreign key constraint. Defaults to None.

        Examples:
            >>> column = (
            Column(column_name='patient_id', data_type='text', primary_key=True,unique=True,max_length=255))
        """

        self.column_name = column_name
        self.data_type = data_type
        self.primary_key = primary_key
        self.foreign_key = foreign_key
        self.unique = unique
        self.null = null
        self.max_length = max_length
        self.precision = precision
        self.scale = scale
        self.referenced_column = referenced_column
        self.referenced_table = referenced_table
        self.on_delete = on_delete
        self.foreign_key_constraint_name = foreign_key_constraint_name

        if not isinstance(column_name, str) or not column_name:
            raise TypeError("column_name must be a non-empty text")

        if not isinstance(data_type, str):
            raise TypeError("data_type must be a text")

    def __repr__(self):
        return (
            f"Column("
            f"column_name='{self.column_name}', "
            f"data_type='{self.data_type}', "
            f"primary_key={self.primary_key}, "
            f"foreign_key={self.foreign_key}, "
            f"unique={self.unique}, "
            f"null={self.null}, "
            f"max_length={self.max_length}, "
            f"precision={self.precision}, "
            f"scale={self.scale}, "
            f"referenced_column={self.referenced_column}, "
            f"referenced_table={self.referenced_table}, "
            f"on_delete={self.on_delete}, "
            f"foreign_key_constraint_name={self.foreign_key_constraint_name}"
            f")"
        )


def check_workspace_format(columns, rows):
    for col in columns:
        if col.data_type == "json":
            error_row_count = 0
            for row in rows:
                if (
                    col.column_name in row
                    and isinstance(row[col.column_name], dict)
                    and row[col.column_name].get("type") == "file"
                ):
                    attrs = row[col.column_name].get("attributes")
                    if not attrs or "storage" not in attrs or "location" not in attrs:
                        error_row_count += 1

            if error_row_count > 0:
                print(
                    f"Column '{col.column_name}' of data type JSON has {error_row_count} rows "
                    "with type 'file' but missing the required attributes 'location' and 'storage'."
                )


class Table:
    """
    Initializes an instance of a Table with the unique identifier atlas_id, table_name and optional list of columns.

    Parameters:
            atlas_id: Atlas ID.
            table_name: The name of the table to be initialized.
            columns: List of column objects representing the columns in the table.


    Usage:
        from polly.auth import Polly
        from polly.atlas import Atlas, Table, Column

        Polly.auth("<access_key>")

        table = Table(atlas_id="atlas_1", table_name="patient_exposure")
    """

    atlas_id: str
    table_name: str
    columns: List[Column]

    def __init__(self, atlas_id: str, table_name: str, columns: List[Column] = None):
        """
        Initializes an instance of a Table with the unique identifier atlas_id, table_name and optional list of columns

        Args:
            atlas_id: The unique identifier for the Atlas.
            table_name: The name of the table to be initialized.
            columns: List of column objects representing the columns in the table.

        Examples:
            >>> table = Table(atlas_id='1234', table_name='my_table')
        """
        self.atlas_id = atlas_id
        self._get_session: Callable[[], PollySession] = lambda: Polly.default_session
        self._get_session().headers["Accept"] = "application/vnd.api+json"
        self._get_session().headers["Accept-Encoding"] = "gzip"
        self.table_name = table_name
        self.columns = columns if columns else self.list_columns()
        self.rows = []

    @classmethod
    def from_kwargs(cls, atlas_id: str, **kwargs):
        table_name: str = kwargs.get("table_name")
        col_dict = kwargs.get("columns")

        columns: List[Column] = [
            Column(
                **{key: value for key, value in column.items() if key != "data_nature"}
            )
            for column in col_dict
        ]

        return cls(atlas_id, table_name, columns)

    def __repr__(self):
        return f"Table(table_name='{self.table_name}', columns={self.columns})"

    def list_columns(self) -> List[Column]:
        """
        Retrieve the list of columns associated with the table.

        Returns:
            A list of Column objects representing the columns in the table.

        Examples:
            >>> patient_table = Table(atlas_id='atlas_1', table_name='patient')
            >>> columns = patient_table.list_columns()
        """
        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}/tables/{self.table_name}"
        response = self._get_session().get(url=url)
        validated_response = handle_success_and_error_response(response=response)
        all_columns = []
        if validated_response:
            for column in validated_response["data"]["attributes"]["columns"]:
                all_columns.append(
                    Column(
                        column_name=column["column_name"],
                        data_type=column["data_type"],
                        primary_key=column.get("primary_key", False),
                        foreign_key=column.get("foreign_key", False),
                        unique=column.get("unique", False),
                        null=column.get("null", False),
                        max_length=column.get("max_length"),
                        precision=column.get("precision"),
                        scale=column.get("scale"),
                        referenced_column=column.get("referenced_column"),
                        referenced_table=column.get("referenced_table"),
                        on_delete=column.get("on_delete"),
                        foreign_key_constraint_name=column.get(
                            "foreign_key_constraint_name"
                        ),
                    )
                )
        return all_columns

    def get_column(self, column_name: str) -> Column:
        """
        Retrieve a specific column from the table based on its name.

        Args:
            column_name: The name of the column to retrieve.

        Returns:
            The Column object representing the specified column.

        Raises:
            ValueError: If no column with the specified name is found in the table.

        Examples:
            >>> patient_table = Table(atlas_id='atlas_1', table_name='patient')
            >>> column = patient_table.get_column(column_name='patient_id')
        """
        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}/tables/{self.table_name}/columns/{column_name}"
        response = self._get_session().get(url=url)
        validated_response = handle_success_and_error_response(response=response)
        if validated_response:
            return Column(
                validated_response["data"]["attributes"]["column_name"],
                validated_response["data"]["attributes"]["data_type"],
                validated_response["data"]["attributes"]["primary_key"],
                validated_response["data"]["attributes"]["foreign_key"],
                validated_response["data"]["attributes"]["unique"],
                validated_response["data"]["attributes"]["null"],
                validated_response["data"]["attributes"]["max_length"],
                validated_response["data"]["attributes"]["precision"],
                validated_response["data"]["attributes"]["scale"],
                validated_response["data"]["attributes"]["referenced_column"],
                validated_response["data"]["attributes"]["referenced_table"],
                validated_response["data"]["attributes"]["on_delete"],
                validated_response["data"]["attributes"].get(
                    "foreign_key_constraint_name", None
                ),
            )

    def add_column(self, column: Column) -> Column:
        """
        Adds a new column to the table.

        Args:
            column: The Column object representing the column to add.

        Returns:
            The Column object that was added to the table.

        Examples:
            >>> new_column = Column(column_name='patient_age', data_type='int')
            >>> added_column = patient_table.add_column(column=new_column)
        """
        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}/tables/{self.table_name}/columns"
        payload = {
            "data": {
                "type": "column",
                "id": column.column_name,
                "attributes": {
                    "column_name": column.column_name,
                    "data_type": column.data_type,
                    "primary_key": column.primary_key,
                    "foreign_key": column.foreign_key,
                    "unique": column.unique,
                    "null": column.null,
                    "max_length": column.max_length,
                    "precision": column.precision,
                    "scale": column.scale,
                    "referenced_column": column.referenced_column,
                    "referenced_table": column.referenced_table,
                    "on_delete": column.on_delete,
                    "foreign_key_constraint_name": column.foreign_key_constraint_name,
                },
            }
        }
        response = self._get_session().post(url=url, json=payload)
        validated_response = handle_success_and_error_response(response=response)
        if validated_response:
            column = Column(
                validated_response["data"]["attributes"]["column_name"],
                validated_response["data"]["attributes"]["data_type"],
                validated_response["data"]["attributes"]["primary_key"],
                validated_response["data"]["attributes"]["foreign_key"],
                validated_response["data"]["attributes"]["unique"],
                validated_response["data"]["attributes"]["null"],
                validated_response["data"]["attributes"]["max_length"],
                validated_response["data"]["attributes"]["precision"],
                validated_response["data"]["attributes"]["scale"],
                validated_response["data"]["attributes"]["referenced_column"],
                validated_response["data"]["attributes"]["referenced_table"],
                validated_response["data"]["attributes"]["on_delete"],
                validated_response["data"]["attributes"].get(
                    "foreign_key_constraint_name", None
                ),
            )
            self.columns.append(column)
            return column

    def delete_column(self, column_name: str) -> None:
        """
        Delete a column from the table based on its name.

        Args:
            column_name: The name of the column to be deleted

        Examples:
            >>> patient_table = Table(atlas_id='atlas_1', table_name='patient')
            >>> patient_table.delete_column(column_name='patient_age')
        """
        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}/tables/{self.table_name}/columns/{column_name}"
        response = self._get_session().delete(url=url)
        validated_response = handle_success_and_error_response(response=response)
        if validated_response:
            self.columns = [
                column for column in self.columns if column.column_name != column_name
            ]

    def add_rows(self, rows: List[dict]):
        """
        Adds new rows to the table.

        Args:
            rows: A list of dictionaries representing rows to be added.

        Examples:
            >>> patient_table = Table(atlas_id='atlas_1', table_name='patient')
            >>> rows = [
            >>>     {"patient_id": "P0311", "patient_age": 23},
            >>>     {"patient_id": "P0312", "patient_age": 24},
            >>> ]
            >>> patient_table.add_rows(rows)
        """
        check_workspace_format(self.columns, rows)
        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}/tables/{self.table_name}/rows"
        payload = {
            "data": {
                "type": "rows",
                "attributes": {"operation": "add", "rows": rows},
            }
        }
        response = self._get_session().post(url=url, json=payload)
        validated_response = handle_success_and_error_response(response=response)
        if validated_response:
            print(validated_response["data"])

    def insert_rows(self, rows):
        self.rows.extend(rows)

    def delete_rows(self, rows: List[dict]):
        """
        Delete rows from the table based on the column value

        Args:
            rows: A list of key-value pairs representing rows to delete,
                where the key is the primary key column name and value is the corresponding entry.

        Examples:
            >>> patient_table = Table(atlas_id='atlas_1',table_name='patient')
            >>> rows = [
            >>>     {'patient_id': 'P0311'},
            >>>     {'patient_id': 'P0322'}
            >>> ]
            >>> patient_table.delete_rows(rows=rows)
        """
        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}/tables/{self.table_name}/rows"
        payload = {
            "data": {
                "type": "rows",
                "attributes": {"operation": "delete", "rows": rows},
            }
        }
        response = self._get_session().post(url=url, json=payload)
        validated_response = handle_success_and_error_response(response=response)
        if validated_response:
            print(validated_response["data"])

    def rename_column(self, old_column_name: str, new_column_name: str) -> None:
        """
        Rename the name of a column in the table.

        Args:
            old_column_name: The current name of the column to rename.
            new_column_name: The new name to assign to the column.

        Returns:
            None.

        Examples:
            >>> table = Table(atlas_id='my_atlas', table_name='patient')
            >>> table.rename_column(old_column_name='age', new_column_name='patient_age')
        """
        existing_column = next(
            (col for col in self.columns if col.column_name == old_column_name), None
        )

        if not existing_column:
            raise ValueError(
                f"Column '{old_column_name}' not found in table '{self.table_name}'."
            )

        base_url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}"
        url = f"{base_url}/tables/{self.table_name}/columns/{old_column_name}"

        payload = {
            "data": {
                "type": "column",
                "id": old_column_name,
                "attributes": {
                    "column_name": new_column_name,
                    "data_type": existing_column.data_type,
                },
            }
        }

        response = self._get_session().patch(url=url, json=payload)
        handle_success_and_error_response(response=response)

        existing_column.column_name = new_column_name

    def update_rows(self, rows: List[dict]):
        """
        Update rows in the table based on provided row data.

        Args:
            rows: A list of dictionaries representing the rows to update.

        Examples:
            >>> patient_table = Table(atlas_id='atlas_1', table_name='patient')
            >>> rows = [
            >>>    {"patient_id": "P0311", "patient_age": 23},
            >>>    {"patient_id": "P0322", "patient_age": 24},
            >>> ]
            >>> patient_table.update_rows(rows=rows)
        """

        check_workspace_format(self.columns, rows)
        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}/tables/{self.table_name}/rows"
        payload = {
            "data": {
                "type": "rows",
                "attributes": {"operation": "update", "rows": rows},
            }
        }
        response = self._get_session().post(url=url, json=payload)
        validated_response = handle_success_and_error_response(response=response)
        if validated_response:
            print(validated_response["data"])

    def head(self) -> pd.DataFrame:
        """
        Retrieve the first five rows of the table as a Pandas DataFrame.

        Returns:
            A Pandas DataFrame containing the first five rows of the table.

        Examples:
            >>> patient_table = Table(atlas_id='atlas_1', table_name='patient')
            >>> head_df = patient_table.head()
        """

        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}/tables/{self.table_name}/rows"
        index = ""
        for column in self.columns:
            if column.primary_key:
                index = column.column_name
                break
        response = self._get_session().get(url=url)
        validated_response = handle_success_and_error_response(response=response)
        if validated_response:
            rows = validated_response["data"]["rows"]
            if not rows:
                return pd.DataFrame()
            return pd.DataFrame(rows, columns=rows[0].keys()).set_index(index)

        return pd.DataFrame()

    def iter_rows(self, page_size: Optional[int]) -> Iterator[List[Dict[str, Any]]]:
        """
        Iterate over the rows of the table in a paginated manner.

        Args:
            page_size: Page size for iteration over the table. Defaults to 500000 rows.

        Yields:
            A list of dictionaries representing rows of the table, with column names as keys and corresponding values.

        Examples:
            >>> patient_table = Table(atlas_id='atlas_1', table_name='patient')
            >>> for page_rows in patient_table.iter_rows():
            >>>     for row in page_rows:
        """
        if not page_size:
            page_size = 500000
        next = f"/atlas/{self.atlas_id}/tables/{self.table_name}/rows?page[size]={page_size}&page[number]=1"
        while next:
            url = f"{self._get_session().atlas_domain_url}{next}"
            response = self._get_session().get(url=url)
            validated_response = handle_success_and_error_response(response=response)
            rows = validated_response["data"]["rows"]
            if not rows:
                break
            yield rows
            next = validated_response["links"]["next"]
            next = str(next).replace("/sarovar", "")

    def to_df(self) -> pd.DataFrame:
        """
        Return the complete table as a Pandas DataFrame.

        Returns:
            A Pandas DataFrame containing the data from the table.

        Examples:
            >>> patient_table = Table(atlas_id='atlas_1', table_name='patient')
            >>> df = patient_table.to_df()
        """
        index = ""
        for column in self.columns:
            if column.primary_key:
                index = column.column_name
                break
        next = f"/atlas/{self.atlas_id}/tables/{self.table_name}/rows?page[size]=500000&page[number]=1"
        all_rows = []
        while next:
            url = f"{self._get_session().atlas_domain_url}{next}"
            response = self._get_session().get(url=url)
            validated_response = handle_success_and_error_response(response=response)
            rows = validated_response["data"]["rows"]
            if not rows:
                break
            all_rows.extend(rows)
            next = validated_response["links"]["next"]
            next = str(next).replace("/sarovar", "")
        return (
            pd.DataFrame(all_rows, columns=all_rows[0].keys()).set_index(index)
            if all_rows
            else pd.DataFrame()
        )


class Atlas:
    """
    Atlas is a user-defined collection of tables that combines
    the  spreadsheets with the relational databases.
    Each table organizes data around a specific clinical factor or other criteria.
    With Atlas, users can seamlessly structure and analyze complex datasets.

    Parameters:
        atlas_id: Atlas ID


    Usage:
        from polly.auth import Polly
        from polly.atlas import Atlas, Table, Column

        Polly.auth("<access_key>")

        atlas = Atlas(atlas_id="atlas_1")
    """

    atlas_id: str
    tables: List[Table]

    def __init__(self, atlas_id: str):
        """
        Initializes the internal data Atlas with a given Atlas ID

        Args:
            atlas_id: The identifier for the Atlas

        Examples:
            >>> atlas = Atlas(atlas_id='atlas_1')
        """
        self.atlas_id = atlas_id
        self._get_session: Callable[[], PollySession] = lambda: Polly.default_session
        self._get_session().headers["Accept"] = "application/vnd.api+json"
        self._get_session().headers["Accept-Encoding"] = "gzip"
        if self.exists():
            self.tables: List[Table] = self.list_tables()
        else:
            self.tables = []

    @classmethod
    def create_atlas(cls, atlas_id: str, atlas_name: str):
        """
        Creates a new atlas with the specified name and atlas id.

        Args:
            atlas_id: The id of the new atlas to create.
            atlas_name: Name of atlas to be created.

        Returns:
            The newly created Atlas object.

        Examples:
            >>> atlas = Atlas.create_atlas(atlas_id='my_atlas', atlas_name='My Atlas')
        """
        session = Polly.default_session
        session.headers["Accept"] = "application/vnd.api+json"
        session.headers["Accept-Encoding"] = "gzip"
        url = f"{session.atlas_domain_url}/atlas"
        payload = {
            "data": {
                "type": "atlas",
                "attributes": {"id": f"{atlas_id}", "name": f"{atlas_name}"},
            }
        }
        response = session.post(url=url, json=payload)
        handle_success_and_error_response(response=response)

        return cls(atlas_id=atlas_id)

    @classmethod
    def delete_atlas(cls, atlas_id: str):
        """
        Delete an atlas  based on its atlas id.

        Args:
            Atlas_id: The id of the atlas to be deleted

        Examples:
            >>> atlas.delete_atlas(atlas_id="atlas_1")
        """
        session = Polly.default_session
        session.headers["Accept"] = "application/vnd.api+json"
        session.headers["Accept-Encoding"] = "gzip"
        url = f"{session.atlas_domain_url}/atlas/{atlas_id}"
        response = session.delete(url=url)
        handle_success_and_error_response(response=response)

    @classmethod
    def list_atlases(cls):
        """
        Retrieve the list of atlases associated with an Atlas id.

        Returns:
            A list of Atlas objects representing the atlases associated with an Atlas ID.

        Examples:
            >>> Atlas.list_atlases()
        """
        session = Polly.default_session
        session.headers["Accept"] = "application/vnd.api+json"
        session.headers["Accept-Encoding"] = "gzip"
        url = f"{session.atlas_domain_url}/atlas"
        response = session.get(url=url)
        validated_response = handle_success_and_error_response(response=response)
        all_atlases = []
        for atlas in validated_response["data"]:
            all_atlases.append(cls(atlas_id=atlas["id"]))

        return all_atlases

    def __repr__(self):
        return f"Atlas(atlas_id={self.atlas_id})"

    def get_name(self) -> str:
        """
        Retrieve the name of the Atlas using the Atlas ID

        Returns:
            The name of the Atlas as a string

        Examples:
            >>> atlas = Atlas(atlas_id='atlas_1')
            >>> atlas.get_name()
            'My Atlas'
        """
        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}"
        response = self._get_session().get(url=url)
        validated_response = handle_success_and_error_response(response=response)
        if validated_response:
            return validated_response["data"]["attributes"]["name"]

    def list_tables(self) -> Table:
        """
        Retrieve the list of tables associated with an Atlas.

        Returns:
            A list of Table objects representing the tables associated with an Atlas.

        Examples:
            >>> atlas = Atlas(atlas_id='atlas_1')
            >>> tables = atlas.list_tables()
        """
        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}/tables"
        response = self._get_session().get(url=url)
        validated_response = handle_success_and_error_response(response=response)
        all_tables = []
        if validated_response:
            for table_data in validated_response["data"]:
                all_tables.append(
                    Table.from_kwargs(self.atlas_id, **table_data["attributes"])
                )
        return all_tables

    def get_table(self, table_name: str) -> Table:
        """
        Retrieve a specific table object by name.

        Args:
            table_name: The name of the table to retrieve.

        Returns:
            The Table object representing the specified table.

        Notes:
            It loads the table object and not the table data. Use to_df() function to do so.

        Examples:
            >>> atlas = Atlas(atlas_id='1234')
            >>> table = atlas.get_table(table_name='my_table')
        """

        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}/tables/{table_name}"
        response = self._get_session().get(url=url)
        validated_response = handle_success_and_error_response(response=response)
        if validated_response:
            return Table.from_kwargs(
                atlas_id=self.atlas_id, **validated_response["data"]["attributes"]
            )

    def rename_table(self, old_table_name: str, new_table_name: str) -> Table:
        """
        Rename the name of an existing table in the Atlas.

        Args:
            old_table_name: The current name of the table to rename.
            new_table_name: The new name to assign to the table.

        Returns:
            The renamed Table object.

        Examples:
            >>> atlas = Atlas(atlas_id='my_atlas')
            >>> renamed_table = atlas.rename_table(old_table_name='patient', new_table_name='patient_info')
        """
        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}/tables/{old_table_name}"
        payload = {
            "data": {
                "type": "table",
                "id": old_table_name,
                "attributes": {"table_name": new_table_name},
            }
        }
        response = self._get_session().patch(url=url, json=payload)
        validated_response = handle_success_and_error_response(response=response)
        if validated_response:
            return Table.from_kwargs(
                atlas_id=self.atlas_id, **validated_response["data"]["attributes"]
            )

    def create_table(
        self, table_name: str, columns: List[Column], rows: Optional[List[dict]] = None
    ) -> Table:
        """
        Create a new table with the specified name and columns.

        Args:
            table_name: The name of the new table to create.
            columns: A list of Column objects representing the columns of the new table.
            rows (list, optional): A list of key-value pairs representing the table data.

        Returns:
            The newly created Table object.

        Examples:
            >>> atlas = Atlas(atlas_id='my_atlas')
            >>> columns = [
            >>>    Column(column_name='patient_id', data_type='integer', primary_key=True),
            >>>    Column(column_name='patient_ name', data_type='text')
            >>> ]
            >>> patient_table = atlas.create_table(table_name='patient', columns=columns)
        """
        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}/tables/"
        all_columns = []
        for item in columns:
            column = {
                "column_name": item.column_name,
                "data_type": item.data_type,
                "primary_key": item.primary_key,
                "foreign_key": item.foreign_key,
                "unique": item.unique,
                "null": item.null,
                "max_length": item.max_length,
                "precision": item.precision,
                "scale": item.scale,
                "referenced_column": item.referenced_column,
                "referenced_table": item.referenced_table,
                "on_delete": item.on_delete,
                "foreign_key_constraint_name": item.foreign_key_constraint_name,
            }
            all_columns.append(column)
        if not rows:
            rows = []
        payload = {
            "data": {
                "id": table_name,
                "type": "table",
                "attributes": {
                    "table_name": table_name,
                    "columns": all_columns,
                    "rows": rows,
                },
            }
        }
        response = self._get_session().post(url=url, json=payload)
        validated_response = handle_success_and_error_response(response=response)
        if validated_response:
            new_table = Table.from_kwargs(
                atlas_id=self.atlas_id, **validated_response["data"]["attributes"]
            )
            self.tables.append(new_table)
            return new_table
        else:
            raise ValueError("Table creation failed, invalid response received.")

    def delete_table(self, table_name: str) -> None:
        """
        Delete the table from the atlas.

        Args:
            table_name: The name of the table to delete.

        Examples:
            >>> atlas = Atlas(atlas_id='atlas_1')
            >>> atlas.delete_table(table_name='patient')
        """
        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}/tables/{table_name}"
        response = self._get_session().delete(url=url)
        validated_response = handle_success_and_error_response(response=response)
        if validated_response:
            self.tables = [
                table for table in self.tables if table.table_name != table_name
            ]

    def query(self, query: str) -> pd.DataFrame:
        """
        Execute a query on the Atlas tables.

        Args:
            query: The SQL query to execute.

        Returns:
            The result of the query execution.

        Examples:
            >>> atlas = Atlas(atlas_id='atlas_1')
            >>> result = atlas.query(query='SELECT * FROM patient;')
        """
        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}/queries"
        payload = {
            "data": {
                "id": self.atlas_id,
                "type": "query",
                "attributes": {"id": self.atlas_id, "query": query},
            }
        }
        response = self._get_session().post(url=url, json=payload)
        validated_response = handle_success_and_error_response(response=response)
        if validated_response:
            return validated_response["data"]["results"]

        return pd.DataFrame()

    def exists(self) -> bool:
        """
        Return True if atlas exists else False

        Returns:
            The name of the Atlas as a string

        Examples:
            >>> atlas = Atlas(atlas_id='atlas_1')
            >>> atlas.exists()
            True
        """
        url = f"{self._get_session().atlas_domain_url}/atlas/{self.atlas_id}"
        response = self._get_session().get(url=url)

        try:
            validated_response = handle_success_and_error_response(response=response)

            if response.status_code == 200 and isinstance(
                validated_response["data"], list
            ):
                return any(
                    atlas.get("id") == self.atlas_id
                    for atlas in validated_response["data"]
                )
            elif response.status_code == 200 and isinstance(
                validated_response["data"], dict
            ):
                return validated_response["data"].get("id") == self.atlas_id
            else:
                return False
        except ResourceNotFoundError:
            return False


class PayloadTooLargeError(Exception):
    """Custom exception for payload size exceeded."""

    def __init__(self, message="Payload size exceeds the allowed limit."):
        self.message = message
        super().__init__(self.message)


def handle_success_and_error_response(response: Response):
    error_message = "Unknown error"

    if response.status_code in [200, 201]:
        return response.json()

    if response.status_code == 204:
        return None

    if response.status_code == 401:
        raise UnauthorizedException()
    if response.status_code == 413:
        raise PayloadTooLargeError()
    error_message = get_error_message(response)

    if response.status_code == 400:
        raise BadRequestError(detail=error_message)
    elif response.status_code == 404:
        raise ResourceNotFoundError(detail=error_message)
    elif response.status_code == 409:
        raise Exception(f"Conflict: {error_message}")

    if int(response.status_code) >= 500:
        raise Exception(f"Server error: {error_message}")

    response.raise_for_status()


def get_error_message(response: Response):
    """Helper function to extract error message from response"""
    if "errors" in response.json():
        errors = response.json()["errors"]
        if isinstance(errors, list) and errors:
            return errors[0].get("detail", "Unknown error")
        return errors or "Unknown error"
    return "Unknown error"
