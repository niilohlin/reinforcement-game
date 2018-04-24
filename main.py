
import pygame
import sys
import time
import os
import random
from game import *
from keyboard_controller import KeyboardController
from random_controller import RandomController
from pygame_view import PygameView

def start():
    pygame.init()
    game = Game()
    keyboardController = KeyboardController(game.players[0])
    randomController = RandomController(game.players[1])
    view = PygameView(game, [keyboardController, randomController])
    view.run()


if __name__ == '__main__':
    start()
