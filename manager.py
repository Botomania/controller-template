import sys
import json
import time

import requests

import docker_helper


class Manager:
    def __init__(self, players, image):
        self.players = players
        self.port = 5000
        self.endpoint = f"http://127.0.0.1:{self.port}"

        if not docker_helper.run(image, {"5000/tcp": str(self.port)}):
            print("Couldn't start manager")
            sys.exit(1)

        success = False

        while not success:
            try:
                resp = requests.post(self.endpoint + "/init", json={"players": players})
                success = True
            except Exception:
                time.sleep(0.5)

        if resp.status_code != 200:
            print("Error in manager/init")
            sys.exit(1)

    def quit(self):
        requests.post(self.endpoint + "/quit")

        return json.dumps({"success": True})

    def get_state(self):
        resp = requests.get(self.endpoint + "/state")

        if resp.status_code != 200:
            print("Error in manager/get_state")
            sys.exit(1)

        return resp.json

    def action(self, player, action):
        payload = {"player": player, "action": action}
        resp = requests.post(self.endpoint + "/action", json=payload)

        if resp.status_code != 200:
            print("Error in manager/action")
            sys.exit(1)

        return resp.json

    def invalid(self, player):
        payload = {"player": player}
        resp = requests.post(self.endpoint + "/invalid", json=payload)

        if resp.status_code != 200:
            print("Error in manager/invalid")
            sys.exit(1)

        return resp.json
