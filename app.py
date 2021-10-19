from flask import Flask, jsonify, request

import services.player_services as player_service

app = Flask(__name__)


# endpoint

@app.route('/users', methods=['GET', 'POST'])  # users and endpoints are in plural
def hello_world():  # put application's code here
    body: dict = request.get_json(force=True)
    user = player_service.create_player(body.get("name", "default"))
    return jsonify(user.to_dict())


if __name__ == '__main__':
    app.run()
