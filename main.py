import json
import sys
import threading

from flask import Flask, request, jsonify

import config
from controller import Controller

app = Flask(__name__)

c = None  # the controller
t = None  # thread var


@app.route("/init", methods=["POST"])
def init():
    """
    Expected input:
    players: [
        {
            "id": 1,
            "name": "test",
            "image": "test-player"
        },
        {
            "id": 2,
            "name": "test2",
            "image": "test-player"
        }
    ]

    manager: {
        "image": "test-manager"
    }
    """
    global c

    players = request.json["players"]
    manager = request.json["manager"]

    c = Controller(players, manager, config.timeout, config.max_steps)

    return json.dumps({"success": True})


@app.route("/begin", methods=["POST"])
def begin():
    if c is None:
        return json.dumps({"error": "initialize this first"})

    global t

    t = threading.Thread(target=c.start)
    t.daemon = True
    t.start()

    return json.dumps({"success": True})


@app.route("/status", methods=["GET"])
def stat():
    if c is None:
        status = "INITIALIZING"
    else:
        status = c.state

    return json.dumps({"status": status})


@app.route("/reset", methods=["POST"])
def reset():
    global c

    if c is None:
        return jsonify({"success": True})

    c.reset()
    c = None

    return jsonify({"success": True})


if __name__ == "__main__":
    app.run("0.0.0.0", 3000)
