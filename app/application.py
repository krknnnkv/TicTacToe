from typing import List

from app.action_manager import ActionManager
from app.board import Board, CellStatus
from app.orchestrator import Orchestrator
from app.player import Player
from app.validator import Validator


class Application:
    def __init__(self, board: Board, players : List[Player]):
        self.board = board
        self.validator = Validator(self.board)
        self.orchestrator = Orchestrator(players)

    def step(self):
        next_player = self.orchestrator.next_player()
        row, col = next_player.next_move()
        self.board.set(row, col, next_player.value)
        validation_result = self.validator.validate()
        return validation_result

