import logging
import pyodbc
from flask.globals import g

logger = logging.getLogger("db_connect message: ")


def database_connection():
    server = 'localhost'
    db = 'CardsGame'
    user = 'AdminCardsGame'
    password = 'Admin1234'

    try:
        connect = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL server}; SERVER=' + server + ';DATABASE=' +
                                 db + ';UID=' + user + ';PWD=' + password)
        g.db_connection = connect
        return g.db_connection
    except Exception as ex:
        logger.info(ex)
