import logging
import pyodbc
from flask import g

logger = logging.getLogger("db_connect message: ")


def database_connection():
    server = 'localhost'
    db = 'CardsGame'
    user = 'TestAdmin'
    password = 'Admin1234'

    try:
        connect = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL server}; SERVER=' + server + ';DATABASE=' +
                                 db + ';UID=' + user + ';PWD=' + password)
        g.db_connection = connect
    except Exception as ex:
        logger.info(ex)
