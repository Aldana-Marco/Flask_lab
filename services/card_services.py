# ----------------------------------------------------------------------------------------------------------------------
from domain.models import Card
import repositories.card_repository as repository

card_repo = repository.CardRepository()


def create_card(name: str, attack: int, defense: int):
    card = Card(1, "", 0, 0)
    if len(card_repo.cards) > 0:
        last_card = card_repo.cards[-1]
        card = Card(last_card.id + 1, name, attack, defense)
    else:
        card = Card(1, name, attack, defense)
    card_repo.cards.append(card)
    return card



def get_cards():
    return repository.CardRepository.cards


def get_card_by_id(card_id: int):
    for card in repository.CardRepository.cards:
        if card_id == card.id:
            return card


def patch_card(attribute, id):
    new_card = {element.attribute: element.value for element in attribute if element.attribute == "name"
                or element.attribute == "attack" or element.attribute == "defense"}
    for index, card in enumerate(repository.CardRepository.cards):
        if id == card.id:
            repository.CardRepository.cards[index] = Card(card.id, new_card.get("name"), new_card.get("attack"),
                                                          new_card.get("defense"))
            new_card = get_card_by_id(id)
    return new_card


def delete_card(card_id: int):
    for index, card in enumerate(repository.CardRepository.cards):
        if card.id == card_id:
            del repository.CardRepository.cards[index]
            return card
    return 'User not found'

