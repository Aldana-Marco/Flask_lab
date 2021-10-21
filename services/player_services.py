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


def update_player(list):
    count=0
    new_user = {element.attribute: element.value for element in list if element.attribute == "name"
            or element.attribute == "score"}
    for user in repository.PlayerRepository.users:
        if new_user.get("name")== user.name:
            repository.PlayerRepository.users[count] = Player(user.id, new_user.name,new_user.get("score"))
            new_user =  get_player_by_id(user.id)
        count += 1
    return new_user


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
