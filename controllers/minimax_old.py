import random
from typing import Dict, List, Tuple

from app.board import Board, CellStatus
from app.validator import Validator, ValidationStatus
from controllers.controls import Controls

# Оценки позиции с точки зрения того, за кого мы считаем ("me").
WIN_SCORE = 1
DRAW_SCORE = 0
LOSE_SCORE = -1

# Ключ кэша: (доска как кортеж кортежей, чей сейчас ход, за кого считаем).
# Кортежи, а не списки, потому что ключом словаря может быть только неизменяемый объект.
CacheKey = Tuple[Tuple[Tuple[int, ...], ...], int, int]


class MinimaxInput(Controls):
    """
    Идеальный игрок: перебирает ВСЕ возможные продолжения партии до конца и выбирает
    ход, который гарантирует лучший исход при лучшей игре соперника.

    Идея минимакса:
      - когда ходим мы — выбираем ход с МАКСИМАЛЬНОЙ оценкой (хотим выиграть);
      - когда ходит соперник — считаем, что он выберет ход с МИНИМАЛЬНОЙ для нас
        оценкой (он тоже хочет выиграть, то есть чтобы мы проиграли);
      - в конце партии оценка известна точно: +1 победа, 0 ничья, -1 поражение.
    Рекурсивно спускаемся до конца партии и «поднимаем» оценки наверх.

    Для крестиков-ноликов дерево небольшое (меньше 550 тысяч партий, а с кэшем —
    всего несколько тысяч уникальных позиций), поэтому полный перебор занимает доли секунды.

    Зачем он нужен в RL-проекте: это эталон. Идеальный игрок никогда не проигрывает,
    значит, обученный агент готов тогда, когда у него 0 поражений против минимакса.
    """

    def __init__(self) -> None:
        # Кэш уже посчитанных позиций (мемоизация): одна и та же позиция достижима
        # разными порядками ходов, нет смысла считать её повторно.
        self._cache: Dict[CacheKey, int] = {}
        # Свой служебный Board, чтобы переиспользовать Validator для проверки конца партии.
        # В него мы подставляем «пробные» доски во время перебора.
        self._scratch_board = Board()
        self._validator = Validator(self._scratch_board)

    def _read_key(self, board: Board, value: int, options: List[Tuple[int, int]]) -> Tuple[int, int]:
        # Работаем на КОПИИ доски: во время перебора мы ставим и убираем фигуры,
        # а настоящую доску трогать нельзя.
        cells = _copy_cells(board.board)
        opponent = _other(value)

        best_score = LOSE_SCORE - 1  # заведомо хуже любого возможного результата
        best_moves: List[Tuple[int, int]] = []

        for row, col in options:
            # Пробуем ход...
            cells[row][col] = value
            # ...смотрим, чем всё закончится, если дальше ходит соперник...
            score = self._minimax(cells, opponent, value)
            # ...и откатываем ход, чтобы попробовать следующий.
            cells[row][col] = CellStatus.EMPTY_FIELD

            if score > best_score:
                best_score = score
                best_moves = [(row, col)]
            elif score == best_score:
                best_moves.append((row, col))

        # Среди равноценных ходов выбираем случайный — иначе минимакс всегда играет
        # одну и ту же партию, и оценивать против него было бы скучно и нечестно.
        return random.choice(best_moves)

    def _minimax(self, cells: List[List[int]], current: int, me: int) -> int:
        """
        Оценить позицию `cells`, в которой сейчас ходит `current`, с точки зрения игрока `me`.

        cells   — доска (список списков), которую мы модифицируем на месте и откатываем.
        current — чей сейчас ход (CROSS_FIELD или ZERO_FIELD).
        me      — за кого считаем оценку.
        """
        key = (_to_key(cells), current, me)
        if key in self._cache:
            return self._cache[key]

        # 1. Партия закончилась? Тогда оценка известна точно.
        result = self._validate(cells)
        if result != ValidationStatus.EMPTY:
            score = _score(result, me)
            self._cache[key] = score
            return score

        # 2. Партия идёт — перебираем все свободные клетки.
        opponent = _other(current)

        if current == me:
            # Наш ход: ищем МАКСИМУМ.
            best = LOSE_SCORE - 1
            for row in range(3):
                for col in range(3):
                    if cells[row][col] == CellStatus.EMPTY_FIELD:
                        cells[row][col] = current
                        score = self._minimax(cells, opponent, me)
                        cells[row][col] =  CellStatus.EMPTY_FIELD
                        if score > best:
                            best = score
        else:
            # Ход соперника: он выберет худшее для нас, ищем МИНИМУМ.
            best = WIN_SCORE + 1
            for row in range(3):
                for col in range(3):
                    if cells[row][col] == CellStatus.EMPTY_FIELD:
                        cells[row][col] = current
                        score = self._minimax(cells, opponent, me)
                        cells[row][col] = CellStatus.EMPTY_FIELD
                        if score < best:
                            best = score

        self._cache[key] = best
        return best

    def _validate(self, cells: List[List[int]]) -> ValidationStatus:
        # Подставляем пробную доску в служебный Board и спрашиваем у Validator результат.
        self._scratch_board.board = cells
        return self._validator.validate()


def _other(value: int) -> CellStatus:
    """Знак соперника: для крестика — нолик, для нолика — крестик."""
    if value == CellStatus.CROSS_FIELD:
        return CellStatus.ZERO_FIELD
    return CellStatus.CROSS_FIELD


def _score(result: int, me: int) -> int:
    """Перевести результат Validator в оценку с точки зрения игрока `me`."""
    if result == ValidationStatus.DRAW:
        return DRAW_SCORE
    if result == ValidationStatus.CROSS_WIN and me == CellStatus.CROSS_FIELD:
        return WIN_SCORE
    if result == ValidationStatus.ZEROS_WIN and me == CellStatus.ZERO_FIELD:
        return WIN_SCORE
    return LOSE_SCORE


def _copy_cells(cells: List[List[int]]) -> List[List[int]]:
    """Глубокая копия доски: копируем каждую строку, а не только внешний список."""
    copied = []
    for row in cells:
        copied.append(list(row))
    return copied


def _to_key(cells: List[List[int]]) -> Tuple[Tuple[int, ...], ...]:
    """Доска → кортеж кортежей, чтобы можно было использовать как ключ словаря."""
    rows = []
    for row in cells:
        rows.append(tuple(row))
    return tuple(rows)