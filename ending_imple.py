# Sample idea on how we can do the ending

from os import get_terminal_size, system, name
from time import sleep
from rich.console import Console
from rich.text import Text
from wcwidth import wcswidth
import sys

TERMINAL_WIDTH = get_terminal_size().columns
TERMINAL_LENGTH = get_terminal_size().lines

console = Console(width=TERMINAL_WIDTH)

listahan = ["この世にあって欲しい物があるよ", 
                "There are things I want in this world", 
                "ずっと自然に年を取りたいです", 
                "I want to naturally grow older forever",
                "この人生は夢だらけ",
                "This life is full of dreams"]

# Stylize text depending on num parity
def stylize_text(list, num):
    text = Text(list[num])
    text.stylize("bold red on white" if num % 2 == 0 else "italic")
    return text

# Clear screen to show only up to two phrases
def clear_screen_if_needed(num):
    if num % 2 == 0:
        system('cls' if name == 'nt' else 'clear')

# Check the display width
def check_display_width(list_text, num):
    display_width = wcswidth(list_text[num])
    # For more information check out this link
    # https://wcwidth.readthedocs.io/en/latest/intro.html#wcwidth-wcswidth
    if display_width < 0:
        return len(list_text[num])
    else:
        return display_width
    
# Print horizontal padding
def print_horizontal_padding(num, padding_h):
    if num % 2 == 0:
        print('\n' * padding_h)

# Add a typewriter effect
def typewriter_effect(list_text):
    padding_h = (TERMINAL_LENGTH - 2) // 2

    for num in range(len(listahan)):
        clear_screen_if_needed(num)
        print_horizontal_padding(num, padding_h)

        padding_v = (TERMINAL_WIDTH - check_display_width(listahan, num)) // 2

        text_in_list = stylize_text(listahan, num)
        sys.stdout.write(" " * padding_v)
        sys.stdout.flush()

        for char in text_in_list:
            console.print(char, end="")
            sys.stdout.flush()
            if num % 2 == 0:
                sleep(0.15)
            else:
                sleep(0.1)
        print()

        sleep(1)

typewriter_effect(listahan)
system('cls')