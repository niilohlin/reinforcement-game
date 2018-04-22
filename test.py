
import unittest
from game import Game
from player import Player
import copy

class TestCollision(unittest.TestCase):

    def test_bouncee_does_not_move(self):
        game = Game()
        old_other_player_pos = copy.deepcopy(game.players[1].frame.origin)
        game.players[0].frame.origin.x = game.players[1].frame.origin.x + 1
        game.players[0].frame.origin.y = game.players[0].frame.size.height + 1

        for i in range(10):
            game.update()

        self.assertEqual(old_other_player_pos, game.players[1].frame.origin)

    def test_reverse_bouncee_does_not_move(self):
        game = Game()
        old_other_player_pos = copy.deepcopy(game.players[0].frame.origin)
        game.players[1].frame.origin.x = game.players[0].frame.origin.x + 1
        game.players[1].frame.origin.y = game.players[1].frame.size.height + 1

        for i in range(10):
            game.update()

        self.assertEqual(old_other_player_pos, game.players[0].frame.origin)



if __name__ == '__main__':
    unittest.main()
