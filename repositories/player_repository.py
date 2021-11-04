import logging
from sqlalchemy.orm import Session
from flask import g

from configuration.db_connect import database_connection_alchemy
from repositories.sql.player_sql import *
from domain.json.schemas import PlayerSchema

logger = logging.getLogger("player_repository -> ")
player_schema = PlayerSchema()


class PlayerRepository:
    players = []

    def _query(self, sql_request: str, commit: bool, return_value: bool):
        sql_result= g.db_connection.execute(sql_request)
        if commit: # Execute only when we need to insert or modify a value in Database
            g.db_connection.commit()
        players_list = []
        if return_value:  # Execute if we need a return value
            for row in sql_result.fetchall():
                players_list.append(dict(zip(PLAYER_PROPERTIES, row)))
            players = player_schema.load(players_list, many=True)
            logger.info("Request successful: " + sql_request)
            return players
        else:  # Execute if we don't need a return value
            logger.info("Request successful: " + sql_request)

    def insert_player(self, name: str, score: int):
        self._query(SQL_INSERT_PLAYER.format(name, score), True, False)
        return self._query(SQL_SELECT_MAX_IDPLAYER, False, True)

    def select_all_players(self):
        return self._query(SQL_SELECT_ALL, False, True)

    def select_player_by_id(self, player_id: int):
        return self._query(SQL_SELECT_PLAYER.format(player_id), False, True)

    def update_player_score(self, parameter_dict: dict, id_player: int):
        new_player_parameters = []
        for parameter, value in parameter_dict.items():
            if parameter == "PlayerName" or parameter == "PlayerScore":
                new_player_parameters.append(f"{parameter} = '{value}'")
        self._query(f"UPDATE Player SET {' , '.join(new_player_parameters)} WHERE IdPLayer={id_player};", True, False)
        return self.select_player_by_id(id_player)

    def delete_player(self, id_player: int):
        query_player_found = self.select_player_by_id(id_player)
        if query_player_found:
            self._query(SQL_DELETE_PLAYER.format(id_player), True, False)
            return query_player_found
        else:
            logger.info("DeletePlayer Failed")
            return "Player not found"
