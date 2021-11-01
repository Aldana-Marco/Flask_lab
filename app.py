"""
Main app where we make inputs and outputs with the user, all by method calls
"""
#comment test
# imports---------------------------------------------------------------------------------------------------------------
from flask import Flask, jsonify, request

import services.player_services as player_service
from domain.json.schemas import PlayerSchema, CardSchema, ParameterLoadSchema
from domain.models import parameter_load
import configuration.db_connect as db_connect
from services import card_services

# Global Variables and Cons---------------------------------------------------------------------------------------------
app = Flask(__name__)
app.debug = True
player_schema = PlayerSchema()
card_schema = CardSchema()
parameter_schema = ParameterLoadSchema()


# Player Methods--------------------------------------------------------------------------------------------------------
@app.before_request
def db():
    db_connect.database_connection()


@app.route("/users", methods=["POST"])
def _post_player():
    player = PlayerSchema(partial=('IdPlayer', 'PlayerScore')).load(request.get_json())
    player = player_service.create_player(player.get("PlayerName"))
    return jsonify(player_schema.dump(player))


@app.route("/users", methods=["GET"])
def _get_players():
    player_list = player_service.get_players()
    return jsonify(player_schema.dump(player_list, many=True))


@app.route("/users/<int:player_id>", methods=["GET"])
def _get_player_by_id(player_id):  # pending
    response = player_service.get_player_by_id(player_id)
    player_list = player_schema.dump(response)
    if player_list:
        return jsonify(player_list)
    else:
        return jsonify(response)


@app.route("/users/<int:player_id>", methods=["PATCH"])
def _patch_player_by_id(player_id):
    parameters = parameter_schema.load(request.get_json(), many=True)
    response = player_service.patch_player(parameters, player_id)
    player = player_schema.dump(response)
    if player:
        return jsonify(player)
    else:
        return jsonify(response)


@app.route("/users/<int:player_id>", methods=["DELETE"])
def _delete_player_by_id(player_id):  # pending because get_player_by_id
    response = player_service.delete_player_by_id(player_id)
    player = player_schema.dump(response)
    if player:
        return jsonify(player)
    else:
        return jsonify(response)


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
    card = card_services.get_card_by_id(card_id)
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
