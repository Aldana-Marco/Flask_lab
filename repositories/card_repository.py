import codecs

from flask import g

from repositories.sql.player_sql import *
from domain.json.schemas import CardSchema
import os.path


class CardRepository:
    cards = []

    def _query(self, sql_request: str, commit_required: bool, return_required: bool):
        sql_result = g.db_connection.execute(sql_request)
        if commit_required:  # Execute only when we need to insert or modify a value in Database
            g.db_connection.commit()
        cards_list = []
        if return_required:  # Execute if we need a return value
            for row in sql_result.fetchall():
                cards_list.append(dict(zip(CARD_PROPERTIES, row)))
            cards = CardSchema().load(cards_list, many=True)
            return cards

    def insert_card(self, name: str, attack: int, defense: int, image):
        x=SQL_INSERT_CARD.format(name, attack, defense, 5)
        self._query(SQL_INSERT_CARD.format(name, attack, defense, ), True, False)
        return "Done!"
        # return self._query(SQL_SELECT_MAX_ID_CARD, False, True)

    def select_all_players(self):
        return self._query(SQL_SELECT_ALL, False, True)

    def select_player_by_id(self, player_id: int):
        return self._query(SQL_SELECT_PLAYER.format(player_id), False, True)

    def update_player_score(self, parameter_dict: dict, id_player: int):
        new_player_parameters = []
        for parameter, value in parameter_dict.items():
            if parameter == "PlayerName" or parameter == "PlayerScore":
                new_player_parameters.append(f"{parameter} = '{value}'")
        self._query(f"UPDATE Players SET {' , '.join(new_player_parameters)} WHERE IdPLayer={id_player};", True, False)
        return self.select_player_by_id(id_player)

    def delete_player(self, id_player: int):
        query_player_found = self.select_player_by_id(id_player)
        if query_player_found:
            self._query(SQL_DELETE_PLAYER.format(id_player), True, False)
            return query_player_found
        else:
            return "Player not found"
