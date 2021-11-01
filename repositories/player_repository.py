import logging
from flask import g
from repositories.sql.player_sql import SQL_SELECT_ALL, SQL_INSERT_PLAYER, SQL_SELECT_PLAYER, PLAYER_PROPERTIES
from domain.json.schemas import PlayerSchema

logger = logging.getLogger("player_repository -> ")
player_schema = PlayerSchema()


class PlayerRepository:
    players = []

    def insert_player(self, name: str, score: int):
        with g.db_connection.cursor() as cursor:
            cursor.execute(SQL_INSERT_PLAYER.format(name, score))
            cursor.commit()
            logger.info("InsertPlayer Successful")
            cursor.execute("SELECT MAX([IdPlayer]) FROM Player")
            player_id = cursor.fetchone()
            player_id = player_id[0]
            return self.select_player_by_id(player_id)

    def select_all_players(self):
        with g.db_connection.cursor() as cursor:
            cursor.execute(SQL_SELECT_ALL)
            players_list = []
            for row in cursor.fetchall():
                players_list.append(dict(zip(PLAYER_PROPERTIES, row)))
            players = player_schema.load(players_list, many=True)
            return players

    def select_player_by_id(self, player_id: int):  # To review -> what if player_id is not in database?
        with g.db_connection.cursor() as cursor:
            cursor.execute(SQL_SELECT_PLAYER.format(player_id))
            sql_result = cursor.fetchone()
            if sql_result:
                players = player_schema.load(dict(zip(PLAYER_PROPERTIES, sql_result)))
                return players
            else:
                return "Player not found"

    def update_player_score(self, parameter_dict: dict, id_player: int):
        with g.db_connection.cursor() as cursor:
            columns = []
            for parameter, value in parameter_dict.items():
                if parameter == "PlayerName" or parameter == "PlayerScore":
                    columns.append(f"{parameter} = '{value}'")
            cursor.execute(f"UPDATE Player SET {' , '.join(columns)} WHERE IdPLayer={id_player};")  # homework Study
            cursor.commit()
            logger.info("UpdatePlayerScore Successful")

    def delete_player(self, id_player: int):
        with g.db_connection.cursor() as cursor:
            cursor.execute(SQL_SELECT_PLAYER.format(id_player))
            sql_result = cursor.fetchone()
            if sql_result:
                cursor.execute(f"DELETE FROM Player WHERE IdPLayer={id_player}")
                cursor.commit()
                logger.info("DeletePlayer Successful")
                return sql_result
            else:
                logger.info("DeletePlayer Failed")
                return "Delete Player Failed"
