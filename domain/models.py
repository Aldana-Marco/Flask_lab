"""
Object classes models
"""
from typing import Dict


class Card(object):
    def __init__(self, card_id: int, name: str, attack: int, defense: int):
        self.id = card_id
        self.name = name
        self.attack = attack
        self.defense = defense


class Parameter:
    def __init__(self, attribute: str, value: str):
        self.attribute = attribute
        self.value = value


def parameter_load(dictionary: dict):
    return Parameter(dictionary.get("attribute"), dictionary.get("value"))


class Player:

    def __init__(self, player_id: int, name: str, score: float):
        self.id = player_id
        self.name = name
        self.score = score

    def to_dict(self) -> Dict:
        """
        returns the representation of the object as a dictionary
        :return: Dict
        """
        return {"id": self.id, "name": self.name, "score": self.score}


class CardXPlayer:
    def __init__(self, card_id: int, player_id: int):
        self.card_id = card_id
        self.player_id = player_id
