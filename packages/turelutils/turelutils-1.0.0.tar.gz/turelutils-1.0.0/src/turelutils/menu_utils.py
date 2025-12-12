import os
import sys
from typing import Any
from type_utils import take_input

def clear_screen():
    """Clear the terminal screen.

    Works on both Windows (cls) and Unix-like systems (clear).
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def arrow_menu(options: list[Any]) -> Any:
    """Display an interactive menu with arrow key navigation.

    Args:
        options: A list of menu options to display.

    Returns:
        The selected option from the list.
    """
    # Get a single keypress cross-platform
    if os.name == 'nt':
        import msvcrt
        def get_key():
            while True:
                key = msvcrt.getch()
                if key == b'\xe0' or key == b'\x00':  # Arrow key prefix
                    key2 = msvcrt.getch()
                    return key + key2
                else:
                    return key
    else:
        import tty
        import termios

        def get_key():
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                key = sys.stdin.read(1)
                if key == '\x1b':  # Arrow key
                    key += sys.stdin.read(2)
                return key.encode()
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    current = 0
    while True:
        clear_screen()
        print("Use UP/DOWN arrows and ENTER to select:\n")
        for i, option in enumerate(options):
            if i == current:
                # Highlight with inverted colors
                print(f"\033[7m{option}\033[0m")
            else:
                print(option)

        key = get_key()

        # Windows arrow keys
        if os.name == 'nt':
            if key == b'\xe0H':  # UP
                current = max(0, current - 1)
            elif key == b'\xe0P':  # DOWN
                current = min(len(options) - 1, current + 1)
            elif key == b'\r':  # ENTER
                clear_screen()
                return options[current]
        else:
            # Unix arrow keys
            if key == b'\x1b[A':  # UP
                current = max(0, current - 1)
            elif key == b'\x1b[B':  # DOWN
                current = min(len(options) - 1, current + 1)
            elif key == b'\r':  # ENTER
                clear_screen()
                return options[current]

def choose_menu(options: list[Any]) -> Any:
    """Display a numbered menu and prompt the user to select an action.

    Args:
        options: A list of option strings to choose from.
    Returns:
        The selected option string from the list.
    """
    # Print the options with numbers
    for i, option in enumerate(iterable=options, start=1):
        print(f"{i}: {option}")

    # Ask the user for a choice
    while True:
        try:    
            choice: int = take_input(prompt="Choose an option by number: ", expected_type=int)
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(options)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")