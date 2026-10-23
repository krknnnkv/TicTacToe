from typing import List, Optional

from app.board import Board
from app.orchestrator import Orchestrator
from app.player import Player
from app.validator import Validator, ValidationStatus


class Application:
    def __init__(self, board: Board, players : List[Player], first_player: Optional[int] = None):
        self.board = board
        self.validator = Validator(self.board)
        self.players = players
        self.orchestrator = Orchestrator(players, first_player)
        self.last_validation_result = ValidationStatus.EMPTY

    def step(self):
        next_player = self.orchestrator.next_player()
        row, col = next_player.next_move()
        self.board.set(row, col, next_player.value)
        self.last_validation_result = self.validator.validate()
        if self.last_validation_result != ValidationStatus.EMPTY:
            for player in self.players:
                player.game_over(self.last_validation_result)
        return self.last_validation_result

