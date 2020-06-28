import sys

import requests

import player_client

import docker_helper


class Player:
    def __init__(self, player, timeout):
        self.id = player["id"]
        self.name = player["name"]
        self.timeout = timeout

        port = 6000 + self.id
        self.endpoint = f"http://docker:{port}"

        conf = player_client.Configuration(host=f"http://docker:{port}")
        api_client = player_client.ApiClient(conf)
        self.api = player_client.PlayerApi(api_client)

        self.image = player["image"]

        if not docker_helper.run(self.image, {"5000/tcp": str(port)}):
            print(f"Couldn't start player {self.name (self.id)}")
            sys.exit(1)

    def action(self, state):
        # TODO: figure out how to use timeout with api
        try:
            resp = requests.post(self.endpoint + "/", json=state, timeout=self.timeout)
        except Exception:
            # TODO: make this helpful
            print("Error!")
            return None

        return resp.json()["action"]

    def quit(self):
        self.api.quit()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
