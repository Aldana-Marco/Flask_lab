from sqlalchemy import create_engine, select, insert
from flask import g
from sqlalchemy.orm import Session

from configuration.constants import SERVER, USER, PASSWORD, DB
from repositories.db_models.models import metadata, players_table, create_players


def database_connection_alchemy():
    if not getattr(g, "db_connection", None):
        g.engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{SERVER}/{DB}?charset=utf8mb4", echo=True)


def init_database():
    metadata.create_all(g.engine)
    create_players(["julio", "Juan", "pepe", "jose", "Mario", "Ivan", "Maria", "Martha", "Johana", "Julia", "Fernanda"])
#    select_player_by_id
