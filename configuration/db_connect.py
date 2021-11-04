import logging
import pyodbc
from sqlalchemy import create_engine,text
from sqlalchemy.engine import URL
from flask import g
from configuration.constants import SERVER,USER,PASSWORD,DB

logger = logging.getLogger("db_connect message: ")




def database_connection():
    try:
        connect = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL server}; SERVER=' + SERVER + ';DATABASE=' +
                                 DB + ';UID=' + USER + ';PWD=' + PASSWORD)
        return connect
    except Exception as ex:
        logger.info(ex)


def database_connection_alchemy():
    url_credentials = f"DRIVER={{ODBC Driver 17 for SQL server}};SERVER={SERVER};DATABASE={DB};UID={USER};PWD={PASSWORD}"
    url=URL.create("mssql+pyodbc", query={"odbc_connect": url_credentials})
    if not getattr(g,"db_connection", None):
        g.db_connection = create_engine(url, echo=True)
    return g.db_connection

