from view import View
from game import Game
from typing import Optional, Tuple


class CLIView(View):
    def __init__(self, game):
        self.game = game
        self.episode = 0

    def draw(self, game: Game) -> None:
        self.episode += 1
        if game.is_running:
            score = "{} - {}, episode: {}".format(self.game.score[self.game.players[0]], self.game.score[self.game.players[1]], self.episode)
            print(score, end="\r")
        else:
            print()
            print("done")


    def get_keys(self) -> Optional[Tuple]:
        return None
