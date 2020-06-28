import sys
import json
import time

import manager_client
from manager_client import ApiException

import docker_helper


class Manager:
    def __init__(self, players, image, port=5000):
        self.players = players

        conf = manager_client.Configuration(host=f"http://docker:{port}")
        api_client = manager_client.ApiClient(conf)
        self.api = manager_client.ManagerApi(api_client)

        if not docker_helper.run(image, {"5000/tcp": str(port)}):
            print("Couldn't start manager")
            sys.exit(1)

        success = False

        while not success:
            try:
                resp = self.api.init({"players": players})
                success = True
            except Exception:
                time.sleep(0.5)

        if not resp.success:
            print("Error in manager/init")
            sys.exit(1)

    def quit(self):
        self.api.quit()

    def get_state(self):
        try:
            resp = self.api.get_state()
        except ApiException as e:
            print("Error in manager/get_state", e)
            sys.exit(1)

        return resp.state

    def action(self, player, action):
        payload = {"player": player, "action": action}

        try:
            resp = self.api.evaluate(payload)
        except ApiException as e:
            print("Error in manager/action", e)
            sys.exit(1)

        return resp

    def invalid(self, player):
        payload = {"player": player}

        try:
            resp = self.api.invalidate(payload)
        except ApiException as e:
            print("Error in manager/invalid", e)
            sys.exit(1)
