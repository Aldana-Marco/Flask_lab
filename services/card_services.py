# ----------------------------------------------------------------------------------------------------------------------
import repositories.card_repository as repository
from domain.json.schemas import CardSchema
from repositories.sql.player_sql import CARD_PROPERTIES

card_repo = repository.CardRepository()


def create_card(name: str, attack:int, defense:int, image):
    return repository.CardRepository().insert_card(name, attack,defense,image)


def get_cards():
    return repository.CardRepository().select_all_cards()


def get_card_by_id(card_id: int):
    response=repository.CardRepository().select_card_by_id(card_id)
    if response:
        return response
    else:
        return "Card not found"


def patch_card(attribute, card_id):
    new_card = {
        element["attribute"]: element["value"]
        for element in attribute
        if element["attribute"] in CARD_PROPERTIES
    }
    new_card["IdCard"] = card_id

    try:
        CardSchema().load(new_card, partial="IdCard")
    except Exception as ex:
        return "Bad Request, input data not valid... " + str(ex)

    repository.CardRepository().update_card(new_card, card_id)
    return get_card_by_id(card_id)

def delete_card_by_id(card_id: int):
    response = get_card_by_id(card_id)
    if response != "Card not found":
        card = repository.CardRepository().delete_card(card_id)
        return card,response
    else:
        return response

