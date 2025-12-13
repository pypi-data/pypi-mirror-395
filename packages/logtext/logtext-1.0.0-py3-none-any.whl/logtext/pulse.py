import time
from typing import Tuple

RGB = Tuple[int, int, int]

def print_pulse(text: str, color: RGB = (0, 255, 255), cycles: int = 6) -> None:
    """Smooth pulsing glow effect"""
    for i in range(cycles * 20):
        phase = (i % 20) / 19.0
        intensity = int(100 + 155 * (phase if phase < 0.5 else 1 - phase) * 2)
        r = int(color[0] * intensity / 255)
        g = int(color[1] * intensity / 255)
        b = int(color[2] * intensity / 255)
        print(f"\r\033[38;2;{r};{g};{b}m{text}\033[0m", end="", flush=True)
        time.sleep(0.05)
    print()