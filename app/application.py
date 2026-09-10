from app.action_manager import ActionManager
from app.board import Board, CROSS_FIELD, ZERO_FIELD
from app.orchestrator import Orchestrator
from app.player import Player
from app.validator import Validator


class Application:
    def __init__(self):
        self.board = Board()
        action_manager = ActionManager(self.board)
        self.player = Player(action_manager, CROSS_FIELD)
        self.opponent = Player(action_manager, ZERO_FIELD)
        self.validator = Validator(self.board)
        self.orchestrator = Orchestrator([self.player, self.opponent])

    def step(self):
        next_player = self.orchestrator.next_player()
        row, col = next_player.next_move()
        self.board.set(row, col, next_player.value)
        validation_result = self.validator.validate()
        return validation_result

