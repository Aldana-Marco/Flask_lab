"""

"""
# ---------------------------------------------------------------------------------------------------------------Imports
from flask import g
from sqlalchemy import text, select
from sqlalchemy.orm import Session

# --------------------------------------------------------------------------------------------------Initializing objects
from repositories.db_models.models import cards_table
from repositories.db_models.sql_constants import *
from domain.schemas import CardSchema


# -----------------------------------------------------------------------------------Class card for interactions with DB
class CardRepository:
    # ------------Generic method for SQL CRUD...Parameters(sql query,bool to commit or not,bool to return values or not)
    def _query(self, sql_request: str, commit_required: bool, return_required: bool):
        with g.engine.begin() as connection:  # connection with db
            sql_result = connection.execute(sql_request)  # send sql query
            if commit_required:  # Execute if we need commit
                session = Session(g.engine)
                session.commit()
                session.close()
            cards_list = []
            if return_required:  # Execute if we need a return value
                for row in sql_result.fetchall():
                    cards_list.append(dict(zip(CARD_PROPERTIES, row)))
                cards = CardSchema().load(cards_list, many=True)
                return cards

    # -----------------------------------------------------------------------------methods for each query cards sentence
    def insert_card(self, name: str, attack: int, defense: int, image):
        orm_query = cards_table.insert().values(CardName=name, CardAttack=attack, CardDefense=defense)
        self._query(orm_query, True, False)
        orm_query = cards_table.select().where(text("IdCard=(SELECT MAX(IdCard) FROM Cards)"))
        return self._query(orm_query, False, True)

    def select_all_cards(self):
        orm_query = cards_table.select()
        cards = self._query(orm_query, False, True)
        return cards

    def select_card_by_id(self, card_id: int):
        orm_query = select([cards_table]).where(cards_table.c.IdCard == card_id)
        return self._query(orm_query, False, True)

    def update_card(self, parameter_dict: dict, id_card: int):
        orm_query = cards_table.update(). \
            where(cards_table.c.IdCard == id_card). \
            values(parameter_dict)
        self._query(orm_query, True, False)
        return self.select_card_by_id(id_card)

    def delete_card(self, id_card: int):
        orm_query = cards_table.delete().where(cards_table.c.IdCard == id_card)
        self._query(orm_query, True, False)
        return "Card deleted:"
# ----------------------------------------------------------------------------------------------------------------------
