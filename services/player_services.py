from domain.models import Player
import repositories.player_repository as repository

player_repo = repository.PlayerRepository()


def create_player(name: str):
    user = Player(len(player_repo.users) + 1, name, 0)
    player_repo.users.append(user)
    print(len(player_repo.users))
    return user
