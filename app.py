# imports---------------------------------------------------------------------------------------------------------------
from flask import Flask, jsonify, request  #

import services.player_services as player_service
from domain.json.schemas import PlayerSchema, CardSchema, ParameterLoadSchema
from domain.models import parameter_load
import configuration.db_connect as db_connect
from services import card_services

# Global Variables and Cons---------------------------------------------------------------------------------------------
db_connect.database_connection()
app = Flask(__name__)

app.debug = True
player_schema = PlayerSchema(partial=['id', 'name', 'score'])  #
card_schema = CardSchema(partial=['id'])
parameter_schema = ParameterLoadSchema()


# Player Methods--------------------------------------------------------------------------------------------------------
@app.route("/users", methods=["POST"])
def _post_player():
    player = player_schema.load(request.get_json())
    player = player_service.create_player(player.get("name"))  # POST
    return jsonify(player_schema.dump(player))


@app.route("/users", methods=["GET"])
def _get_players():
    player_list = player_service.get_players()  # homework multi/many dump // schema = UserSchema(many=True)
    player_to_dict = player_schema.dump(player_list, many=True)
    return jsonify(player_to_dict)


@app.route("/users/<int:player_id>", methods=["GET"])
def _get_player(player_id):
    player = player_service.get_player_by_id(player_id)
    return jsonify(player_schema.dump(player))


@app.route("/users/<int:player_id>", methods=["PATCH"])
def _patch_player_by_id(player_id):
    parameters = parameter_schema.load(request.get_json(), many=True)
    parameter_list = []
    for parameter in parameters:
        parameter_obj = parameter_load(parameter)  # do validation in json without create an object
        parameter_list.append(parameter_obj)
    player_service.patch_player(parameter_list, player_id)
    player = player_service.get_player_by_id(player_id)  # homework should be in player method
    return jsonify(player_schema.dump(player))


@app.route("/users/<int:player_id>", methods=["DELETE"])
def _delete_player_by_id(player_id):
    player = player_service.delete_player(player_id)
    if player != 'Player not found':
        return jsonify(player_schema.dump(player))
    else:
        return jsonify({"Status": "Player not found"})


# Cards methods---------------------------------------------------------------------------------------------------------
@app.route("/cards", methods=["POST"])
def _post_card():
    card = card_schema.load(request.get_json())
    card = card_services.create_card(card.get("name"), card.get("attack"), card.get("defense"))
    return jsonify(card_schema.dump(card))


@app.route("/cards", methods=["GET"])
def _get_cards():
    card_list = card_services.get_cards()
    cards = []
    for card in card_list:
        card_to_dict = card_schema.dump(card)
        cards.append(card_to_dict)
    return jsonify(cards)


@app.route("/cards/<int:card_id>", methods=["GET"])
def _get_card(card_id):
    card = card_services.get_card_by_id(card_id)  # POST
    return jsonify(card_schema.dump(card))


@app.route("/cards/<int:card_id>", methods=["PATCH"])
def _patch_card_by_id(card_id):
    parameters = parameter_schema.load(request.get_json(), many=True)
    parameter_list = []
    for parameter in parameters:
        parameter_obj = parameter_load(parameter)
        parameter_list.append(parameter_obj)
    card_services.patch_card(parameter_list, card_id)
    card = card_services.get_card_by_id(card_id)
    return jsonify(card_schema.dump(card))


@app.route("/cards/<int:card_id>", methods=["DELETE"])
def _delete_card_by_id(card_id):
    card = card_services.delete_card(card_id)
    if card != 'User not found':
        return jsonify(card_schema.dump(card))
    else:
        return jsonify({"Status": "Card not found"})


# Start-----------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run()
