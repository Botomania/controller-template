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

        game_state = self.manager.get_state()
        current_player = 0

        while True:
            last_action = self.players[current_player].action(game_state)

            manager_resp = self.manager.action(
                self.players[current_player].to_dict(), last_action
            )

            if "error" in manager_resp:
                self.manager.invalid(self.players[current_player])
                self.players[current_player].quit()
            elif "winner" in manager_resp:
                self.state = "OVER"

                try:
                    self.manager.quit()
                except Exception:
                    pass

                for i in range(len(self.players)):
                    try:
                        self.players[i].quit()
                    except Exception:
                        pass

                break
            else:
                current_player = manager_resp["next"]
                game_state = manager_resp["state"]
