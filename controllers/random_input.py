import random
from typing import Tuple, List

from controllers.controls import Controls

class RandomInput(Controls):

    def _read_key(self, options: List[Tuple[int, int]]) -> Tuple[int, int]:
        return random.choice(options)