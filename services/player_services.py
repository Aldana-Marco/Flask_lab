"""

"""
# ---------------------------------------------------------------------------------------------------------------Imports
import repositories.player_repository as repository
from domain.schemas import PlayerSchema
from repositories.db_models.sql_constants import PLAYER_PROPERTIES


# ---------------------------------------------------------------------------------------HTML Requests for PLAYERS table
def create_player(name: str):
    return repository.PlayerRepository().insert_player(name)


def get_players():
    return repository.PlayerRepository().select_all_players()


def get_player_by_id(player_id: int):
    response = repository.PlayerRepository().select_player_by_id(player_id)
    if response:
        return response
    else:
        return "Player not found"


def patch_player(attribute, player_id):
    new_player = {
        element["attribute"]: element["value"]
        for element in attribute
        if element["attribute"] in PLAYER_PROPERTIES}
    new_player["IdPlayer"] = player_id
    try:
        PlayerSchema().load(new_player, partial="IdPlayer")
    except Exception as ex:
        return "Bad Request, input data not valid... " + str(ex)
    repository.PlayerRepository().update_player_score(new_player, player_id)
    return get_player_by_id(player_id)


def delete_player_by_id(player_id: int):
    response = get_player_by_id(player_id)
    if response != "Player not found":
        player = repository.PlayerRepository().delete_player(player_id)
        return player, response
    else:
        return response
# ----------------------------------------------------------------------------------------------------------------------