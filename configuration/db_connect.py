"""

"""
# ---------------------------------------------------------------------------------------------------------------Imports
from sqlalchemy import create_engine
from flask import g

from configuration.constants import SERVER, USER, PASSWORD, DB
from repositories.db_models.models import metadata


# ---------------------------------------------------------------------------------------Open Connection to the Database
def database_connection_alchemy():
    if not getattr(g, "db_connection", None):
        g.engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{SERVER}/{DB}?charset=utf8mb4", echo=True)


# -----------------------------------------------------------------------------------Create the database if it's not set
def init_database():
    metadata.create_all(g.engine)
# ----------------------------------------------------------------------------------------------------------------------