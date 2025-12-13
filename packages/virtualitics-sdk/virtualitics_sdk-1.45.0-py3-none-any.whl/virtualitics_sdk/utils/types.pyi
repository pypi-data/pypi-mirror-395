from _typeshed import Incomplete
from enum import Enum

numeric_t: Incomplete
object_t = numeric_t | str | object

class ExtendedEnum(Enum):
    """
    Extends Python's generic enumeration
    """
    @classmethod
    def get_valid_enums(cls) -> list: ...
    @classmethod
    def check_valid_enum(cls, e: str) -> bool: ...
    @classmethod
    def validate(cls, e, return_none: bool = True): ...

class ConnectionType(str, Enum):
    postgresql: str
    mysql: str
    mariadb: str
    mssql: str
    mssql_pyodbc: str
    mssql_pymysql: str
    databricks: str
    spark: str
    snowflake: str
    s3: str
    other: str
    api: str
