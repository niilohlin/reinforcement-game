
import pygame
import sys
import time
import os
import random
from game import *
from keyboard_controller import KeyboardController
from random_controller import RandomController
from heuristic_controller import HeuristicController
from pygame_view import PygameView
from runner import Runner, LearningRunner
from controller import Controller

def start() -> None:
    # game = Game()
    # keyboard_controller: Controller = KeyboardController(game.players[0])
    # heuristic_controller: Controller = HeuristicController(game.players[1])
    # controllers = [heuristic_controller, keyboard_controller]
    # view = PygameView(game)
    # runner = Runner(game, controllers, view)
    # runner.run()
    runner = LearningRunner()
    runner.run()


if __name__ == '__main__':
    start()
