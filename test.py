from app.board import Board, CROSS_FIELD, EMPTY_FIELD, ZERO_FIELD
from app.validator import Validator

board = Board()
validator = Validator(board)
board.board = [
    [EMPTY_FIELD, EMPTY_FIELD, ZERO_FIELD],
    [EMPTY_FIELD, EMPTY_FIELD, ZERO_FIELD],
    [EMPTY_FIELD, EMPTY_FIELD, ZERO_FIELD],
]

a = [1, 2, 3]

b = ['one', 'two', 'three']

print(list(zip(a, b)))
#print(validator.validate())
#print(list(zip(*board.board)))
#print(*board.board)