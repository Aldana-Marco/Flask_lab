import pyodbc

server = 'localhost'
db = 'CardsGame'
user = 'AdminCardsGame'
password = 'Admin1234'


def connection():
    try:
        connect = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL server}; SERVER=' + server + ';DATABASE=' +
                                 db + ';UID=' + user + ';PWD=' + password)
        print('connection successful')
        return connect
    except:
        return 'connection failed'

