from domain.models import Player
import repositories.player_repository as repository

player_repo = repository.PlayerRepository()


def create_player(name: str):
    user = Player(len(player_repo.users) + 1, name, 0)
    player_repo.users.append(user)
    return user

def get_players():
    return player_repo.users