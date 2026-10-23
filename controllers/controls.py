from typing import List, Tuple

from app.board import Board, CellStatus
from protocols.controls_protocol import ControlsProtocol


class Controls(ControlsProtocol):

    def _read_key(self, value: CellStatus, board: Board, options: List[Tuple[int, int]]) -> Tuple[int, int]:
        raise NotImplementedError

    def next_move(self, value: CellStatus, board: Board, options: List[Tuple[int, int]]) -> Tuple[int, int]:
        return self._read_key(value, board, options)

    def game_over(self, reward: float):
        pass