from typing import Dict


class Player:

    def __init__(self, id: int, name: str, score: float):
        self.id = id
        self.name = name
        self.score = score

    def to_dict(self) -> Dict:
        """
        returns the representation of the object as a dictionary
        :return: Dict
        """
        return {"id": self.id, "name": self.name, "score": self.score}


class Card(object):
    def __init__(self, attack: int, defense: int):
        self.attack = attack
        self.defense = defense
