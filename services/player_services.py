from domain.models import Player
import repositories.player_repository as repository

player_repo = repository.PlayerRepository()


def create_player(name: str):
    user = Player(len(player_repo.users) + 1, name, 0)
    player_repo.users.append(user)
    return user


def get_players():
    users = []
    for user in repository.PlayerRepository.users:
        user_to_dict = user.to_dict()
        users.append(user_to_dict)
    return users


def get_player_by_id(id: int):
    for user in repository.PlayerRepository.users:
        if user.to_dict()["id"] == id:
            return user.to_dict()


def update_player(id: int, name: str):
    modified_users_value = ""
    for user in repository.PlayerRepository.users:
        if user.to_dict()["id"] == id:
            repository.PlayerRepository.users[id - 1] = Player(id, name, 0)
            modified_users_value = modified_users_value + str(id) + ", "
    modified_users = {"Modified users id": modified_users_value}
    return modified_users


def delete_player(id: int):
    modified_users_value = ""
    count = 0
    for user in repository.PlayerRepository.users:
        if user.id == id:
            del repository.PlayerRepository.users[count]
            modified_users_value = modified_users_value + str(id) + ", "
        count += 1
    modified_users = {"Modified users id": modified_users_value}
    return modified_users
