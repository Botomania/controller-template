import sys
import json

import requests

import docker_helper


class Player:
    def __init__(self, player, timeout):
        self.id = player["id"]
        self.name = player["name"]
        self.port = 6000 + self.id
        self.endpoint = f"http://127.0.0.1:{self.port}"
        self.timeout = timeout

        self.image = player["image"]

        if not docker_helper.run(self.image, {"5000/tcp": str(self.port)}):
            print(f"Couldn't start player {self.name (self.id)}")
            sys.exit(1)

    def action(self, state):
        resp = requests.post(self.endpoint + "/", json=state, timeout=self.timeout)

        if resp.status_code != 200:
            # TODO: make this helpful
            print("Error!")
            return None

        return resp.json

    def quit(self):
        requests.post(self.endpoint + "/quit")

        return json.dumps({"success": True})
