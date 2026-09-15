from typing import List

from app.board import Board
from app.orchestrator import Orchestrator
from app.player import Player
from app.validator import Validator, ValidationStatus


class Application:
    def __init__(self, board: Board, players : List[Player]):
        self.board = board
        self.validator = Validator(self.board)
        self.orchestrator = Orchestrator(players)
        self.last_validation_result = ValidationStatus.EMPTY

    def step(self):
        next_player = self.orchestrator.next_player()
        row, col = next_player.next_move()
        self.board.set(row, col, next_player.value)
        self.last_validation_result = self.validator.validate()
        return self.last_validation_result

