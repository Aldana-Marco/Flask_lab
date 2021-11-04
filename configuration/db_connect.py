from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from flask import g
from configuration.constants import SERVER, USER, PASSWORD, DB


def database_connection_alchemy():
    url_credentials = f"DRIVER={{ODBC Driver 17 for SQL server}};SERVER={SERVER};DATABASE={DB};UID={USER};" \
                      f"PWD={PASSWORD}"
    url = URL.create("mssql+pyodbc", query={"odbc_connect": url_credentials})
    if not getattr(g, "db_connection", None):
        g.db_connection = create_engine(url, echo=True)
    return g.db_connection
