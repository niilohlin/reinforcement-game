from view import View
from game import Game
from typing import Optional, Tuple


class CLIView(View):
    def __init__(self, game):
        self.game = game

    def draw(self, game: Game) -> None:
        if game.is_running:
            score = "{} - {}".format(self.game.score[self.game.players[0]], self.game.score[self.game.players[1]])
            print(score)
        else:
            print()
            print("done")


    def get_keys(self) -> Optional[Tuple]:
        return None
