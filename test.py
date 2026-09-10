from app.board import Board, CROSS_FIELD, EMPTY_FIELD, ZERO_FIELD
from app.validator import Validator

board = Board()
validator = Validator(board)
board.board = [
    [ZERO_FIELD, ZERO_FIELD, ZERO_FIELD],
    [EMPTY_FIELD, EMPTY_FIELD, EMPTY_FIELD],
    [EMPTY_FIELD, EMPTY_FIELD, EMPTY_FIELD],
]
print(validator.validate())