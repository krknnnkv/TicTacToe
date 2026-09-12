import pygame

from app import action_manager, player, application
from app.action_manager import ActionManager
from app.application import Application
from app.board import Board, CellStatus
from app.player import Player
from app.validator import ValidationStatus
from controllers.random_input import RandomInput
from render.graphic import Graphic


if __name__ == '__main__':
    pygame.init()
    board = Board()
    action_manager = ActionManager(board)
    renderer = Graphic(board)
    player = Player(action_manager, CellStatus.CROSS_FIELD, RandomInput())
    opponent = Player(action_manager, CellStatus.ZERO_FIELD, RandomInput())
    application = Application(board, [player, opponent])
    while application.step() == ValidationStatus.EMPTY:
        renderer.render()

    renderer.render()

    pygame.quit()
