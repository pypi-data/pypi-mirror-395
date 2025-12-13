import time
import random

def print_matrix(text: str, speed: float = 0.08) -> None:
    """Matrix-style digital rain falling effect"""
    chars = list(text.upper())
    drops = [0] * len(chars)
    lengths = [random.randint(8, 20) for _ in chars]

    for _ in range(max(lengths) + 20):
        line = [" "] * len(chars)
        for i in range(len(chars)):
            if drops[i] > 0:
                bright = max(50, 255 - (drops[i] - 1) * 15)
                if drops[i] == 1:
                    line[i] = f"\033[97;1m{chars[i]}\033[0m"  # Head
                elif drops[i] <= lengths[i]:
                    line[i] = f"\033[38;2;0;{bright};50m{chars[i]}\033[0m"
            if drops[i] == 0 and random.random() < 0.15:
                drops[i] = 1
            if drops[i] > 0:
                drops[i] += 1
        print("\r" + "".join(line), end="", flush=True)
        time.sleep(speed)
    print("\033[0m")