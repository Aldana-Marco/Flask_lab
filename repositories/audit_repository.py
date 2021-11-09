from flask import g
from sqlalchemy.orm import Session

from configuration.db_connect import database_connection_alchemy
from repositories.sql.player_sql import SQL_INSERT_AUDIT, SQL_UPDATE_AUDIT_STATUS


def db_open_and_audit():
    # create an audit in database
    with g.engine.begin() as connection:
        sentence=SQL_INSERT_AUDIT.format(g.request_details, g.time, g.id_session, g.status)
        connection.execute(sentence)
        session = Session(g.engine)
        session.commit()
        session.close()
        print("Request is running...")

def db_close_and_audit():
    # update status in audit database
    with g.engine.connect() as connection:
        with connection.begin():
            g.engine.execute(SQL_UPDATE_AUDIT_STATUS.format(g.status, g.id_session))
            session = Session(g.engine)
            session.commit()
            session.close()
            print("closing database...")
            if getattr(g, "db_connection", None):
                g.db_connection.close()
