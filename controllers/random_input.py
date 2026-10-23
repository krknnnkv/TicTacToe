import random
from typing import Tuple, List

from app.board import CellStatus, Board
from controllers.controls import Controls

class RandomInput(Controls):

    def _read_key(self, value: CellStatus, board: Board, options: List[Tuple[int, int]]) -> Tuple[int, int]:
        return random.choice(options)