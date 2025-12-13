import time
import random
from typing import Tuple

RGB = Tuple[int, int, int]

def print_fire(text: str, speed: float = 0.05) -> None:
    """Burning fire text effect"""
    colors = [(255, 0, 0), (255, 69, 0), (255, 140, 0), (255, 215, 0), (255, 165, 0)]
    for _ in range(len(text) + 15):
        line = ""
        for char in text:
            r, g, b = random.choice(colors)
            line += f"\033[38;2;{r};{g};{b}m{char}\033[0m"
        print("\r" + line.center(80), end="", flush=True)
        time.sleep(speed)
    print("\033[0m")