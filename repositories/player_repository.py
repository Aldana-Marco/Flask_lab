"""

"""
# ---------------------------------------------------------------------------------------------------------------Imports
from flask import g
from sqlalchemy import text, select
from sqlalchemy.orm import Session

# --------------------------------------------------------------------------------------------------Initializing objects
from repositories.db_models.models import players_table
from repositories.db_models.sql_constants import *
from domain.schemas import PlayerSchema


# ---------------------------------------------------------------------------------Class player for interactions with DB
class PlayerRepository:
    # ------------Generic method for SQL CRUD...Parameters(sql query,bool to commit or not,bool to return values or not)
    def _query(self, sql_request: str, commit_required: bool, return_required: bool):
        with g.engine.begin() as connection:  # connection with db
            sql_result = connection.execute(sql_request)  # send sql query
            if commit_required:  # Execute if we need commit
                session = Session(g.engine)
                session.commit()
                session.close()
            players_list = []
            if return_required:  # Execute if we need a return value
                for row in sql_result.fetchall():
                    players_list.append(dict(zip(PLAYER_PROPERTIES, row)))
                players = PlayerSchema().load(players_list, many=True)
                return players

    # -----------------------------------------------------------------------------methods for each query cards sentence
    def insert_player(self, name: str):
        orm_query = players_table.insert().values(PlayerName=name)
        self._query(orm_query, True, False)
        orm_query = players_table.select().where(text("IdPlayer=(SELECT MAX(IdPlayer) FROM Players)"))
        return self._query(orm_query, False, True)

    def select_all_players(self):
        orm_query = players_table.select()
        players = self._query(orm_query, False, True)
        return players

    def select_player_by_id(self, player_id: int):
        orm_query = select([players_table]).where(players_table.c.IdPlayer == player_id)
        return self._query(orm_query, False, True)

    def update_player_score(self, parameter_dict: dict, id_player: int):
        orm_query = players_table.update(). \
            where(players_table.c.IdPlayer == id_player). \
            values(parameter_dict)
        self._query(orm_query, True, False)
        return self.select_player_by_id(id_player)

    def delete_player(self, id_player: int):
        orm_query = players_table.delete().where(players_table.c.IdPlayer == id_player)
        self._query(orm_query, True, False)
        return "Player deleted:"
# ----------------------------------------------------------------------------------------------------------------------
