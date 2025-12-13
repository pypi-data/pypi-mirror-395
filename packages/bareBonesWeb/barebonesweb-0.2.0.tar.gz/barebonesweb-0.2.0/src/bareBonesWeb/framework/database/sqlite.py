from typing import Literal
from sqlite3 import connect, Connection, Cursor
import os
from ...__cache import __cached as _cache
#from ...__cache import __setattr__ as _setcache



SQL_INTEGER = "INT"
SQL_REAL = "REAL"
SQL_STRING = "TEXT"
SQL_NULL = "NULL"
SQL_UNIQUE = "UNIQUE"
SQL_NOT_NULL = "NOT NULL"
SQL_PRIMARY_KEY = "PRIMARY KEY"
SQL_AUTOINCREMENT = "AUTOINCREMENT"

ColumnConstraint = Literal["UNIQUE", "NOT NULL", "PRIMARY KEY", "AUTOINCREMENT"]
ColumnType = Literal["INT", "REAL", "NUMERIC", "TEXT", "NULL"]

ColumnSpec = (
    ColumnType | 
    tuple[ColumnType, ColumnConstraint] | 
    tuple[ColumnType, ColumnConstraint, ColumnConstraint]
)


class sqlite_database:
    """
    An sqlite database for bareBonesWeb
    """

    _conn: Connection
    _cur: Cursor

    def __init__(self, name: str = "instance") -> None:
        db_folder = _cache.get("database_folder")
        if not db_folder:
            raise ValueError("Application not made")
        if not os.path.exists(db_folder):
            os.makedirs(db_folder)

        self._conn = connect(os.path.normpath(_cache["database_folder"]+"/"+name+".sqlite3"))
        self._cur = self._conn.cursor()
        self.commit = self._conn.commit
        self.exec = self._cur.execute

    def exec_script(self, database_file: str):
        """
        Runs a sql script from your database folder
        """
        path = os.path.normpath(_cache["database_folder"]+"/"+database_file)
        if os.path.exists(path):
            with open(path, "r") as file:
                self._cur.executescript(file.read())
            self._conn.commit()

    def add_table(self, name: str, **kwargs: ColumnSpec):
                sql_query = f"CREATE TABLE IF NOT EXISTS {name}({",".join([key+" "+" ".join(value) for key, value in kwargs.items()])})"
                self.exec(sql_query)