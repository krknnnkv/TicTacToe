from typing import Tuple, List

import numpy as np

from app.board import CellStatus, Matrix3x3

BOARD_SIZE = 3
ACTION_COUNT = BOARD_SIZE * BOARD_SIZE
OBSERVATION_COUNT = ACTION_COUNT * 2

def encode_obs(board: Matrix3x3, my_value: CellStatus) -> np.ndarray:
    observation = np.zeros(OBSERVATION_COUNT, dtype=np.float32)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            cell = board[row][col]
            index = get_index(row, col)
            if cell == my_value:
                observation[index] = 1.0
            elif cell != CellStatus.EMPTY_FIELD:
                observation[index + ACTION_COUNT] = 1.0
    return observation

def encode_actions(options: List[Tuple[int, int]]) -> np.ndarray:
    mask = np.zeros(BOARD_SIZE, dtype=bool)
    for row, col in options:
        mask[get_index(row, col)] = True
    return mask

def get_cell_coordinate(index: int) -> Tuple[int, int]:
    row = index // BOARD_SIZE
    col = index % BOARD_SIZE
    return row, col

def get_index(row, col):
    return row * BOARD_SIZE + col