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

            verdict = self.manager.action(
                self.players[current_player].to_dict(), last_action
            )

            print("---")
            print(f"Current player: {self.players[current_player].name}")
            print(f"        Action: {last_action}")
            print(f"       Verdict: {verdict}")
            print("---")

            if "error" in verdict:
                self.manager.invalid(self.players[current_player])
                self.players[current_player].quit()
            elif "winner" in verdict:
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
                current_player = verdict["next"]
                game_state = verdict["state"]
