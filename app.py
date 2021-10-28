# imports---------------------------------------------------------------------------------------------------------------
from flask import Flask, jsonify, request  #

import services.player_services as player_service
from domain.json.schemas import PlayerSchema, CardSchema, ParameterLoadSchema
from domain.models import parameter_load
import services.db_connect as db_connection

# Global Variables and Cons---------------------------------------------------------------------------------------------
from services import card_services

app = Flask(__name__)
app.debug = True
db_connect = db_connection.connection()
player_schema = PlayerSchema(partial=['id', 'name', 'score'])
card_schema = CardSchema(partial=['id'])
parameter_schema = ParameterLoadSchema()


# Player Methods--------------------------------------------------------------------------------------------------------
@app.route("/users", methods=["POST"])
def _post_user():
    player = player_schema.load(request.get_json())
    user = player_service.create_player(player.get("name"))  # POST
    return jsonify(player_schema.dump(user))


@app.route("/users", methods=["GET"])
def _get_users():
    user_list = player_service.get_players()
    users = []
    for user in user_list:
        user_to_dict = player_schema.dump(user)
        users.append(user_to_dict)
    return jsonify(users)


@app.route("/users/<int:user_id>", methods=["GET"])
def _get_user(user_id):
    user = player_service.get_player_by_id(user_id)  # POST
    return jsonify(player_schema.dump(user))


@app.route("/users/<int:user_id>", methods=["PATCH"])
def _patch_user_by_id(user_id):
    parameters = parameter_schema.load(request.get_json(), many=True)
    parameter_list = []
    for parameter in parameters:
        parameter_obj = parameter_load(parameter)
        parameter_list.append(parameter_obj)
    player_service.patch_player(parameter_list, user_id)
    player = player_service.get_player_by_id(user_id)
    return jsonify(player_schema.dump(player))


@app.route("/users/<int:user_id>", methods=["DELETE"])
def _delete_user_by_id(user_id):
    user = player_service.delete_player(user_id)  # POST
    if user != 'User not found':
        return jsonify(player_schema.dump(user))
    else:
        return jsonify({"Status": "User not found"})


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
