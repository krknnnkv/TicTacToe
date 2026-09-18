import pygame

from app import action_manager, player, application
from app.action_manager import ActionManager
from app.application import Application
from app.board import Board, CellStatus
from app.player import Player
from app.validator import ValidationStatus
from controllers import keyboard_input
from controllers.keyboard_input import KeyboardInput
from controllers.random_input import RandomInput
from render.graphic import Graphic

def wait_for_restart() -> bool:
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                return True

if __name__ == '__main__':
    pygame.init()
    board = Board()
    action_manager = ActionManager(board)
    renderer = Graphic(board)
    player = Player(action_manager, CellStatus.CROSS_FIELD, RandomInput())
    opponent = Player(action_manager, CellStatus.ZERO_FIELD, KeyboardInput(renderer))
    application = Application(board, [player, opponent])
    while True:
        while application.step() == ValidationStatus.EMPTY:
            renderer.render()
        renderer.render(last_validation_result=application.last_validation_result)

        if not wait_for_restart():
            break
        board.reset()
        application.last_validation_result = ValidationStatus.EMPTY

    pygame.quit()
