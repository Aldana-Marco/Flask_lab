from domain.models import Player
import repositories.player_repository as repository

player_repo = repository.PlayerRepository()


def create_player(name: str):
    if len(player_repo.players) > 0:
        last_player = player_repo.players[-1]
        player = Player(last_player.id + 1, name, 0)
    else:
        player = Player(1, name, 0)
    player_repo.players.append(player)
    return player


def get_players():
    return repository.PlayerRepository().select_all_players()


def get_player_by_id(player_id: int):
    for player in repository.PlayerRepository.players:
        if player.id == player_id:
            return player


def patch_player(attribute, player_id):
    new_player = {element.attribute: element.value for element in attribute if element.attribute == "name"
                  or element.attribute == "score"}
    for index, player in enumerate(repository.PlayerRepository.players):
        if player_id == player.id:
            repository.PlayerRepository.players[index] = Player(player.id, new_player.get("name"),
                                                                new_player.get("score"))
            new_player = get_player_by_id(player.id)
    return new_player


def delete_player(player_id: int):
    for index, player in enumerate(repository.PlayerRepository.players):
        if player.id == player_id:
            del repository.PlayerRepository.players[index]
            return player
    return 'User not found'
