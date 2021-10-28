from domain.models import Player
import repositories.player_repository as repository

player_repo = repository.PlayerRepository()


def create_player(name: str):
    user = Player(1, "", 0)
    if len(player_repo.users) > 0:
        last_player = player_repo.users[-1]
        user = Player(last_player.id + 1, name, 0)
    else:
        user = Player(1, name, 0)
    player_repo.users.append(user)
    return user


def get_players():
    return repository.PlayerRepository.users


def get_player_by_id(player_id: int):
    for player in repository.PlayerRepository.users:
        if player.id == player_id:
            return player


def patch_player(attribute, id):
    new_user = {element.attribute: element.value for element in attribute if element.attribute == "name"
                or element.attribute == "score"}
    for index, user in enumerate(repository.PlayerRepository.users):
        if id == user.id:
            repository.PlayerRepository.users[index] = Player(user.id, new_user.get("name"), new_user.get("score"))
            new_user = get_player_by_id(user.id)
    return new_user


def delete_player(id: int):
    for index, player in enumerate(repository.PlayerRepository.users):
        if player.id == id:
            del repository.PlayerRepository.users[index]
            return player
    return 'User not found'
