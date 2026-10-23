from typing import Protocol, Tuple, List

from app.board import Board, CellStatus


class ControlsProtocol(Protocol):
    def next_move(self, value: CellStatus, board: Board, options: List[Tuple[int, int]]) -> Tuple[int, int]:
        ...

    def game_over(self, reward: float) -> None:
        ...
