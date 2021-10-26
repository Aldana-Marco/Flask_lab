from flask import Flask, jsonify, request  #

import services.player_services as player_service
from domain.json.schemas import PlayerSchema
from domain.models import parameter_load

app = Flask(__name__)


@app.route("/users", methods=["POST"])
def _post_user():  # put application's code here
    body: dict = request.get_json()
    user = player_service.create_player(body.get("name", "default"))  # POST
    return jsonify(user.to_dict())


@app.route("/users", methods=["GET"])
def _get_users():
    body: dict = request.get_json()
    if body.get("id", "default") == "default":
        app.logger.info("Executing GET list of users")
        user_list = player_service.get_players()
        users = []
        player_schema = PlayerSchema()
        for user in user_list:
            user_to_dict = player_schema.dump(user)
            users.append(user_to_dict)
        return jsonify(users)
    else:
        app.logger.info("Executing GET of the user")
        user = player_service.get_player_by_id(body.get("id", "default"))  # POST
        return jsonify(user["name"].to_dict())


@app.route("/users/<int:id>", methods=["PATCH"])
def _patch_user_by_id(id):
    app.logger.info("receiving put")
    body: dict = request.get_json()
    parameter_list = []
    for parameter in body:
        parameter_obj = parameter_load(parameter)
        parameter_list.append(parameter_obj)
    player_service.patch_player(parameter_list, id)
    player = player_service.get_player_by_id(id)
    return jsonify(player.to_dict())


@app.route("/users/<int:id>", methods=["DELETE"])
def _delete_user_by_id(id):
    body: dict = request.get_json()
    user = player_service.delete_player(body.get("id", "default"))  # POST
    return jsonify(user)


if __name__ == '__main__':
    app.run(debug=True)
