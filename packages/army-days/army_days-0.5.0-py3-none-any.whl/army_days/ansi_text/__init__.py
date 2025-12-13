# ANSI escape codes
RESET = "\033[0m"
UNDERLINE = "\033[4m"


def rgb_background(r, g, b):
    return f"\033[48;2;{r};{g};{b}m"


def rgb_foreground(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"
