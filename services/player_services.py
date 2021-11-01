"""

"""
import repositories.player_repository as repository

player_repo = repository.PlayerRepository()


def create_player(name: str):
    player = repository.PlayerRepository().insert_player(name, 0)
    return player


def get_players():
    return repository.PlayerRepository().select_all_players()


def get_player_by_id(player_id: int):
    return repository.PlayerRepository().select_player_by_id(player_id)


def patch_player(attribute, player_id):
    # To review -> data validation, what if the attributes aren´t PlayerName or PlayerScore?
    # dict comprehension
    new_player = {
        element["attribute"]: element["value"]
        for element in attribute
        if element["attribute"] == "PlayerName"
           or element["attribute"] == "PlayerScore"
    }
    repository.PlayerRepository().update_player_score(new_player, player_id)
    return get_player_by_id(player_id)


def delete_player_by_id(player_id: int):
    player = get_player_by_id(player_id)
    if player:
        repository.PlayerRepository().delete_player(player_id)
    return player
