from app.board import Board, CellStatus
from app.validator import Validator

board = Board()
validator = Validator(board)
board.board = [
    [CellStatus.EMPTY_FIELD, CellStatus.EMPTY_FIELD, CellStatus.ZERO_FIELD],
    [CellStatus.EMPTY_FIELD, CellStatus.EMPTY_FIELD, CellStatus.ZERO_FIELD],
    [CellStatus.EMPTY_FIELD, CellStatus.EMPTY_FIELD, CellStatus.ZERO_FIELD],
]

a = [1, 2, 3]

b = ['one', 'two', 'three']

print(list(zip(a, b)))
print(validator.validate())
#print(list(zip(*board.board)))
#print(*board.board)