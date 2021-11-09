import mysql.connector
import pymysql
import pyodbc

from sqlalchemy import create_engine

from sqlalchemy.engine import URL
from flask import g
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import Session

from configuration.constants import SERVER, USER, PASSWORD, DB, PORT


def database_connection_alchemy():
    if not getattr(g, "db_connection", None):
        g.engine=create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{SERVER}/{DB}?charset=utf8mb4", echo=True)

    #connection = pymysql.connect(
    #    host=SERVER,
    #    user=USER,
    #    password=PASSWORD,
    #    db=DB
    #)
    #g.db_connection = connection.cursor()
    #return g.db_connection
    #url_credentials = f"DRIVER={{ODBC Driver 17 for SQL server}};SERVER={SERVER};DATABASE={DB};UID={USER};" \
    #                  f"PWD={PASSWORD}"
    #url = URL.create("mssql+pyodbc", query={"odbc_connect": url_credentials})
    #if not getattr(g, "db_connection", None):
    #    g.db_connection = create_engine(url, echo=True)
    #return g.db_connection
    #