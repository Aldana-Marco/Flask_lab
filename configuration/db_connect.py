import logging

import pyodbc

db_connection = ""
logger = logging.getLogger("db_connect message: ")


def database_connection():
    server = 'localhost'
    db = 'CardsGame'
    user = 'AdminCardsGame'
    password = 'Admin1234'

    try:
        connect = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL server}; SERVER=' + server + ';DATABASE=' +
                                 db + ';UID=' + user + ';PWD=' + password)
        # Solution
        global db_connection
        db_connection = connect
    except Exception as ex:
        logger.info(ex)
