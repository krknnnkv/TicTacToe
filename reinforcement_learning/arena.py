from typing import Tuple

from app.action_manager import ActionManager
from app.application import Application
from app.board import CellStatus, Board
from app.player import Player
from app.validator import ValidationStatus
from controllers.minimax_input import MinimaxInput
from controllers.random_input import RandomInput
from protocols.controls_protocol import ControlsProtocol


def play(agent: ControlsProtocol, opponent: ControlsProtocol, n_games: int) -> Tuple[int, int, int]:
    wins, draws, defeats = 0, 0, 0
    for i in range(n_games):
        agent_first_step = i % 2 == 0
        result, agent_value = play_one_game(agent, opponent, agent_first_step)
        if result == ValidationStatus.DRAW:
            draws += 1
        elif is_win_for(result, agent_value):
            wins += 1
        else:
            defeats += 1
    return wins, draws, defeats

def is_win_for(result: ValidationStatus, value: CellStatus) -> bool:
    if result == ValidationStatus.ZEROS_WIN and value == CellStatus.ZERO_FIELD:
        return True

    if result == ValidationStatus.CROSS_WIN and value == CellStatus.CROSS_FIELD:
        return True

    return False

def play_one_game(agent: ControlsProtocol, opponent: ControlsProtocol, agent_first_step: bool) -> Tuple[ValidationStatus, CellStatus]:
    board = Board()
    action_manager = ActionManager(board)
    if agent_first_step:
        agent_value = CellStatus.CROSS_FIELD
        opponent_value = CellStatus.ZERO_FIELD
    else:
        agent_value = CellStatus.ZERO_FIELD
        opponent_value = CellStatus.CROSS_FIELD
    agent_player = Player(action_manager, agent_value, agent)
    opponent_player = Player(action_manager, opponent_value, opponent)
    if agent_first_step:
        players = [agent_player, opponent_player]
    else:
        players = [opponent_player, agent_player]
    application = Application(board, players, first_player = 0)
    result = ValidationStatus.EMPTY
    while result == ValidationStatus.EMPTY:
        result = application.step()
    return result, agent_value

def report(title: str, wins: int, draws: int, defeats: int) -> None:
    total = wins + draws + defeats
    print(
        f"{title}: "
        f"победы {wins} ({100 * wins / total:.1f}%), "
        f"ничьи {draws} ({100 * draws / total:.1f}%), "
        f"поражения {defeats} ({100 * defeats / total:.1f}%)"
    )

n = 10
wins, draws, defeats = play(RandomInput(), MinimaxInput(), n)
report("random vs minimax", wins, draws, defeats)
wins, draws, defeats = play(MinimaxInput(), MinimaxInput(), n)
report("minimax vs minimax", wins, draws, defeats)
wins, draws, defeats = play(RandomInput(), RandomInput(), n)
report("random vs random", wins, draws, defeats)

