from manager import Manager
from player import Player


class Controller:
    def __init__(self, players, manager, timeout):
        self.players = []
        self.manager = Manager(players, manager["image"])
        self.state = "INITIALIZING"

        for player in players:
            self.players.append(Player(player, timeout))

    def start(self):
        self.state = "RUNNING"
        # TODO: finish this
        pass
