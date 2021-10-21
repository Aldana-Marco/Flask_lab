from typing import Dict


class Card(object):
    def __init__(self, attack: int, defense: int):
        self.attack = attack
        self.defense = defense


class Parameter():

    def __init__(self, attribute: str, value: str):
        self.attribute = attribute
        self.value = value


def parameter_load(dictionary: dict):
    x = 0
    if dictionary.get("attribute", "") != "" and dictionary.get("value", "") != "":
        return Parameter(dictionary.get("attribute"), dictionary.get("value"))
    else:
        raise Exception()


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
