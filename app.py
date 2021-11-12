"""
Main app where we make inputs and outputs with the user, all by method calls
"""
# ---------------------------------------------------------------------------------------------------------------Imports
from flask import Flask, jsonify, request

from configuration.db_connect import init_database, database_connection_alchemy
from services.player_services import *
from services.card_services import *
from domain.schemas import PlayerSchema, CardSchema, ParameterLoadSchema
from services.audit_services import initialize_db_and_audit, finalize_db_and_audit

# ---------------------------------------------------------------------------------------------Global Variables and Cons
app = Flask(__name__)
app.debug = False  # modify to develop in debug mode

# --------------------------------------------------------------------------------------------------initializing objects
player_schema = PlayerSchema()
card_schema = CardSchema()
parameter_schema = ParameterLoadSchema()
with app.app_context():
    database_connection_alchemy()
    init_database()


# --------------------------------------------------------------------------------------------Flask Before/After Methods
@app.before_request
def before_request_func():
    print("Initializing request!")
    initialize_db_and_audit()


@app.after_request
def after_request(response):
    finalize_db_and_audit(response.status)
    print("closing request...")
    return response


@app.teardown_request
def teardown_request_func(error):
    if error:
        finalize_db_and_audit(error)
        print("closing request with server error...")


# ------------------------------------------------------------------------------------------------Player Request Methods
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
        return jsonify(player_list)
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
def _delete_player_by_id(player_id):
    player_query = delete_player_by_id(player_id)
    player = player_schema.dump(player_query)
    if player:
        return jsonify(player)
    else:
        return jsonify(player_query)


# -------------------------------------------------------------------------------------------------Cards Request methods
@app.route("/cards", methods=["POST"])
def _post_card():
    card = CardSchema(partial=('IdCard', 'CardImage')).load(request.get_json())
    card_query = create_card(card.get("CardName"), card.get("CardAttack"), card.get("CardDefense"),
                             card.get("CardImage"))
    return jsonify(card_schema.dump(card_query, many=True))


@app.route("/cards", methods=["GET"])
def _get_cards():
    card_list = get_cards()
    cards = []
    for card in card_list:
        card_to_dict = card_schema.dump(card)
        cards.append(card_to_dict)
    return jsonify(cards)


@app.route("/cards/<int:card_id>", methods=["GET"])
def _get_card_by_id(card_id):
    card_query = get_card_by_id(card_id)
    card_list = card_schema.dump(card_query)
    if card_list:
        return jsonify(card_list)
    else:
        return jsonify(card_query)


@app.route("/cards/<int:card_id>", methods=["PATCH"])
def _patch_card_by_id(card_id):
    parameters = parameter_schema.load(request.get_json(), many=True)
    card_query = patch_card(parameters, card_id)
    card = card_schema.dump(card_query)
    if card:
        return jsonify(card_schema.dump(card, many=True))
    else:
        return jsonify(card_query)


@app.route("/cards/<int:card_id>", methods=["DELETE"])
def _delete_card_by_id(card_id):
    card_query = delete_card_by_id(card_id)
    card = card_schema.dump(card_query)
    if card:
        return jsonify(card)
    else:
        return jsonify(card_query)


# -----------------------------------------------------------------------------------------------------------------Start
if __name__ == '__main__':
    app.run()
# ----------------------------------------------------------------------------------------------------------------------
