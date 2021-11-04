"""
Main app where we make inputs and outputs with the user, all by method calls
"""
# imports---------------------------------------------------------------------------------------------------------------
import datetime
import uuid
from flask import Flask, jsonify, request, g
from sqlalchemy.orm import Session

import services.player_services as player_service
from configuration.db_connect import database_connection_alchemy
from domain.json.schemas import PlayerSchema, CardSchema, ParameterLoadSchema
from domain.models import parameter_load
from repositories.sql.player_sql import SQL_INSERT_AUDIT, SQL_UPDATE_AUDIT_STATUS
from services import card_services

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
    # declare request details
    request_details = str(request.remote_addr) + " - " + str(request.url) + " - " + str(request.method) + " - " \
                      + str(request.get_json())
    request_details = request_details.replace("'", "''")  # to avoid errors by ' in database insert
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    g.id_session = uuid.uuid1()
    g.status = "Requested"
    # create a log in database
    g.db_connection = Session(database_connection_alchemy())
    g.db_connection.execute(SQL_INSERT_AUDIT.format(request_details, time, g.id_session, g.status))
    g.db_connection.commit()
    print("Request is running...")


@app.teardown_request
def teardown_request_func(error):
    # update status in database log
    if error:
        g.status = str(error).replace("'", "''")  # to avoid errors by ' in database insert
        print(str(error))
    else:
        g.status = "Done!"
    g.db_connection.execute(SQL_UPDATE_AUDIT_STATUS.format(g.status, g.id_session))
    g.db_connection.commit()
    print("closing database...")
    if getattr(g, "db_connection", None):
        g.db_connection.close()
        print("closing program...")


# Player Request Methods------------------------------------------------------------------------------------------------
@app.route("/users", methods=["POST"])
def _post_player():
    player = PlayerSchema(partial=('IdPlayer', 'PlayerScore')).load(request.get_json())
    player_query = player_service.create_player(player.get("PlayerName"))
    return jsonify(player_schema.dump(player_query, many=True))


@app.route("/users", methods=["GET"])
def _get_players():
    player_list = player_service.get_players()
    return jsonify(player_schema.dump(player_list, many=True))


@app.route("/users/<int:player_id>", methods=["GET"])
def _get_player_by_id(player_id):
    player_query = player_service.get_player_by_id(player_id)
    player_list = player_schema.dump(player_query)
    if player_list:
        return jsonify(player_schema.dump(player_list, many=True))
    else:
        return jsonify(player_query)


@app.route("/users/<int:player_id>", methods=["PATCH"])
def _patch_player_by_id(player_id):
    parameters = parameter_schema.load(request.get_json(), many=True)
    player_query = player_service.patch_player(parameters, player_id)
    player = player_schema.dump(player_query)
    if player:
        return jsonify(player_schema.dump(player, many=True))
    else:
        return jsonify(player_query)


@app.route("/users/<int:player_id>", methods=["DELETE"])
def _delete_player_by_id(player_id):  # pending because get_player_by_id
    player_query = player_service.delete_player_by_id(player_id)
    player = player_schema.dump(player_query)
    if player:
        return jsonify(player_schema.dump(player, many=True))
    else:
        return jsonify(player_query)


# Cards  Request methods------------------------------------------------------------------------------------------------
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
