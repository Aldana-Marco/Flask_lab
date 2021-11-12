"""

"""
# ---------------------------------------------------------------------------------------------------------------Imports
from flask import g
from sqlalchemy.orm import Session

from repositories.db_models.models import audits_table


# -------------------------------------------------------------------------------------------Create an audit in database
def open_audit():
    with g.engine.begin() as connection:
        orm_query = audits_table.insert().values(
            Request=g.request_details, Time=g.time, IdSession=g.id_session, Status=g.status)
        connection.execute(orm_query)
        session = Session(g.engine)
        session.commit()
        session.close()
        print("Request is running...")


# ------------------------------------------------------------------------Close Database and update audit status to done
def db_close_and_audit(status):
    with g.engine.connect() as connection:
        with connection.begin():
            orm_query = audits_table.update(). \
                where(audits_table.c.IdSession == g.id_session). \
                values(Status=status)
            connection.execute(orm_query)
            session = Session(g.engine)
            session.commit()
            session.close()
            print("closing database...")
            if getattr(g, "db_connection", None):
                g.db_connection.close()
# ----------------------------------------------------------------------------------------------------------------------
