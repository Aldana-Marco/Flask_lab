import logging
from repositories.sql.player_sql import SQL_SELECT_ALL, PLAYER_PROPERTIES
from domain.json.schemas import PlayerSchema
import configuration.db_connect as connect

logger = logging.getLogger("player_repository -> ")
player_schema = PlayerSchema()


class PlayerRepository:
    players = []

    def insert_player(self, name: str, score: int):
        with connect.db_connection.cursor() as cursor:
            cursor.execute("INSERT [dbo].[Player] ([PlayerName], [PlayerScore]) VALUES ('{}', {})".format(name, score))
            cursor.commit()
            logger.info("InsertPlayer Successful")

    def select_all_players(self):
        with connect.db_connection.cursor() as cursor:
            cursor.execute(SQL_SELECT_ALL)
            players_list = []
            for row in cursor.fetchall():
                debug = zip(PLAYER_PROPERTIES, row)
                debug = dict(debug)
                players_list.append(debug)
            players = player_schema.load(players_list, many=True)
            return players

    def update_player_score(self, parameter_list: list, id_player: int):
        with connect.db_connection.cursor() as cursor:
            columns = []
            for parameter in parameter_list:
                columns.append(f"{parameter.attribute}={parameter.value}")
            cursor.execute(f"UPDATE Player SET {','.join(columns)} WHERE IdPLayer={id_player};")  # homework Study
            cursor.commit()
            logger.info("UpdatePlayerScore Successful")

    def delete_player(self, id_player: int):
        with connect.db_connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM Player WHERE IdPLayer={id_player}")
            cursor.commit()
            logger.info("DeletePlayer Successful")
