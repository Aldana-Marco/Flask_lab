"""

"""
# ---------------------------------------------------------------------------------------------------------------Imports
import uuid
from datetime import datetime
from flask import request, g

from configuration.db_connect import database_connection_alchemy
from repositories.audit_repository import open_audit, db_close_and_audit


# ------------------------------------------------------------------------------Get the variables to send to audit event
def initialize_db_and_audit():
    request_details = str(request) + " " + str(request.get_data())
    g.request_details = request_details.replace("> b", "> ")  # to avoid errors by ' in database insert
    g.time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    g.id_session = uuid.uuid1()
    g.status = "Requested"
    database_connection_alchemy()
    open_audit()


# ----------------------------------------------------------------------Updating status to send to the close audit event
def finalize_db_and_audit(status):
    db_close_and_audit(status)
# ----------------------------------------------------------------------------------------------------------------------
