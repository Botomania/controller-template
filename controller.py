import sys

from manager import Manager
from player import Player


class Controller:
    def __init__(self, players, manager, timeout, max_steps):
        self.players = []
        self.manager = Manager(players, manager["image"])
        self.state = "INITIALIZING"
        self.max_steps = max_steps

        for player in players:
            self.players.append(Player(player, timeout))

    def start(self):
        self.state = "RUNNING"

        game_state = self.manager.get_state()
        current_player = self.players[0]

        num_steps = 0

        while current_player is not None and num_steps < self.max_steps:
            num_steps += 1
            last_action = current_player.action(game_state)

            verdict = self.manager.action(current_player.to_dict(), last_action)

            print(f"---------STEP {num_steps}---------")
            print(f"Current player: {current_player.name}")
            print(f"        Action: {last_action}")
            print(f"       Verdict: {verdict}")
            print("---")

            if "error" in verdict:
                self.manager.invalid(current_player.to_dict())
                current_player.quit()

                # TODO: have a mech for deciding next player
                # ig manager should give it to me
                current_player = None
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
                next_id = verdict["next"]
                next_player = list(filter(lambda x: x.id == next_id, self.players))

                if len(next_player) == 0:
                    print(f"Got unknown player id: {next_id}")
                    sys.exit(1)

                current_player = next_player[0]

                game_state = verdict["state"]
