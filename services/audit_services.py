import uuid
from datetime import datetime
from flask import request, g
from sqlalchemy.orm import Session

from configuration.db_connect import database_connection_alchemy
from repositories.audit_repository import db_open_and_audit, db_close_and_audit


def initialize_db_and_audit():
    request_details = str(request.remote_addr) + " - " + str(request.url) + " - " + str(request.method) + " - " \
                      + str(request.get_json())
    g.request_details = request_details.replace("'", "''")  # to avoid errors by ' in database insert
    g.time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    g.id_session = uuid.uuid1()
    g.status = "Requested"
    database_connection_alchemy()
    db_open_and_audit()

def finalize_db_and_audit(error):
    if error:
        g.status = str(error).replace("'", "''")  # to avoid errors by ' in database insert
        print(str(error))
    g.status="Done!"
    db_close_and_audit()