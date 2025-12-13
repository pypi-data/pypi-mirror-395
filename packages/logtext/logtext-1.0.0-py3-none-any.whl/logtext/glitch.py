import time
import random

def print_glitch(text: str, intensity: int = 12) -> None:
    """Cyberpunk digital glitch effect"""
    chars = "█▓▒░▲▼◆◇♪♫§¶"
    for _ in range(intensity):
        out = []
        for c in text:
            if random.random() < 0.4:
                out.append(random.choice(chars))
            else:
                hue = random.randint(0, 360)
                # Simple RGB from HSV approx
                r = random.randint(100, 255)
                g = random.randint(0, 150)
                b = random.randint(200, 255)
                out.append(f"\033[38;2;{r};{g};{b}m{c}\033[0m")
        print("\r" + "".join(out).ljust(60), end="", flush=True)
        time.sleep(0.09)
    print(f"\r\033[38;2;255;0;255m{text}\033[0m")