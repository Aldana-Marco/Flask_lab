from domain.models import Player
import repositories.player_repository as repository

player_repo = repository.PlayerRepository()


def create_player(name: str):
    user = Player(len(player_repo.users) + 1, name, 0)
    player_repo.users.append(user)
    return user


def get_players():
    #users = []
    #for user in repository.PlayerRepository.users:
    #    user_to_dict = user
    #    users.append(user_to_dict)
    return repository.PlayerRepository.users


def get_player_by_id(player_id: int):
    for user in repository.PlayerRepository.users:
        if user.id == player_id:
            return user


def patch_player(attribute, id):
    new_user = {element.attribute: element.value for element in attribute if element.attribute == "name"
                or element.attribute == "score"}
    for index, user in enumerate(repository.PlayerRepository.users):
        if id == user.id:
            repository.PlayerRepository.users[index] = Player(user.id, new_user.get("name"), new_user.get("score"))
            new_user = get_player_by_id(user.id)
    return new_user


def delete_player(player_id: int):
    modified_users_value = ""
    count = 0
    for user in repository.PlayerRepository.users:
        if user.id == player_id:
            del repository.PlayerRepository.users[count]
            modified_users_value = modified_users_value + str(player_id) + ", "
        count += 1
    modified_users = {"Modified users id": modified_users_value}
    return modified_users
