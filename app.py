"""
Main app where we make inputs and outputs with the user, all by method calls
"""
# imports---------------------------------------------------------------------------------------------------------------
from ast import literal_eval
import re

from flask import Flask, jsonify, request

from services.player_services import *
from services.card_services import *
from domain.json.schemas import PlayerSchema, CardSchema, ParameterLoadSchema
from domain.models import parameter_load
from services.audit_services import initialize_db_and_audit, finalize_db_and_audit

# Global Variables and Cons---------------------------------------------------------------------------------------------
app = Flask(__name__)
app.debug = True
# initializing objects--------------------------------------------------------------------------------------------------
player_schema = PlayerSchema()
card_schema = CardSchema()
parameter_schema = ParameterLoadSchema()


# Player Before/After Methods-------------------------------------------------------------------------------------------
@app.before_request
def before_request_func():
    print("Initializing request!")
    initialize_db_and_audit()


@app.teardown_request
def teardown_request_func(error):
    finalize_db_and_audit(error)
    print("closing request...")


# Player Request Methods------------------------------------------------------------------------------------------------
@app.route("/users", methods=["POST"])
def _post_player():
    player = PlayerSchema(partial=('IdPlayer', 'PlayerScore')).load(request.get_json())
    player_query = create_player(player.get("PlayerName"))
    return jsonify(player_schema.dump(player_query, many=True))


@app.route("/users", methods=["GET"])
def _get_players():
    player_list = get_players()
    return jsonify(player_schema.dump(player_list, many=True))


@app.route("/users/<int:player_id>", methods=["GET"])
def _get_player_by_id(player_id):
    player_query = get_player_by_id(player_id)
    player_list = player_schema.dump(player_query)
    if player_list:
        return jsonify(player_schema.dump(player_list, many=True))
    else:
        return jsonify(player_query)


@app.route("/users/<int:player_id>", methods=["PATCH"])
def _patch_player_by_id(player_id):
    parameters = parameter_schema.load(request.get_json(), many=True)
    player_query = patch_player(parameters, player_id)
    player = player_schema.dump(player_query)
    if player:
        return jsonify(player_schema.dump(player, many=True))
    else:
        return jsonify(player_query)


@app.route("/users/<int:player_id>", methods=["DELETE"])
def _delete_player_by_id(player_id):  # pending because get_player_by_id
    player_query = delete_player_by_id(player_id)
    player = player_schema.dump(player_query)
    if player:
        return jsonify(player_schema.dump(player, many=True))
    else:
        return jsonify(player_query)


# Cards  Request methods------------------------------------------------------------------------------------------------
@app.route("/cards", methods=["POST"])
def _post_card():
    card = CardSchema(partial=('IdCard', 'CardImage')).load(request.get_json())
    card_query = create_card(card.get("CardName"), card.get("CardAttack"), card.get("CardDefense"), card.get("CardImage"))
    return jsonify(card_schema.dump(card_query, many=True))

    # card = card_schema.load(request.get_json())
    # card = create_card(card.get("name"), card.get("attack"), card.get("defense"))
    # return jsonify(card_schema.dump(card))


@app.route("/cards", methods=["GET"])
def _get_cards():
    card_list = get_cards()
    cards = []
    for card in card_list:
        card_to_dict = card_schema.dump(card)
        cards.append(card_to_dict)
    return jsonify(cards)


@app.route("/cards/<int:card_id>", methods=["GET"])
def _get_card(card_id):
    card = get_card_by_id(card_id)
    return jsonify(card_schema.dump(card))


@app.route("/cards/<int:card_id>", methods=["PATCH"])
def _patch_card_by_id(card_id):
    parameters = parameter_schema.load(request.get_json(), many=True)
    parameter_list = []
    for parameter in parameters:
        parameter_obj = parameter_load(parameter)
        parameter_list.append(parameter_obj)
    patch_card(parameter_list, card_id)
    card = get_card_by_id(card_id)
    return jsonify(card_schema.dump(card))


@app.route("/cards/<int:card_id>", methods=["DELETE"])
def _delete_card_by_id(card_id):
    card = delete_card(card_id)
    if card != 'User not found':
        return jsonify(card_schema.dump(card))
    else:
        return jsonify({"Status": "Card not found"})


# Start-----------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run()
