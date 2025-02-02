"""Main menu module."""

from typing import Literal
import keyboard  # type: ignore

from utils_manager import Utils
from sound_manager import SoundManager
from users_manager import UsersManager


class MainMenu:
    """
    Main menu UI class.

    Args:
        _Utils (class): Inherits the _Utils class.
        SoundManager (class): Inherits the SoundManager class.
    """

    def __init__(self) -> None:
        self.utils = Utils()
        self.snd = SoundManager()

        self.username: str | Literal[""] = ""

    def title_screen(self) -> None:
        """Clear the terminal and print the main title screen."""

        self.snd.play_menu()
        self.utils.clear_term()
        self.utils.toggle_cursor()

        print(self.utils.TEXT_COLOR + self.utils.TITLE + "\n")
        print(self.utils.TEXT_COLOR + self.utils.START_GAME_PROMPT)

        while True:
            event: keyboard.KeyboardEvent = keyboard.read_event(suppress=True)

            if event.event_type == "down":
                if event.name == "enter":
                    self.snd.play_pluck()
                    return

                continue

    def prompt_for_username(self) -> None:
        """Clear the terminal and ask the user for a username."""

        self.utils.clear_term()
        self.utils.toggle_cursor()

        users_manager = UsersManager()

        self.username = input(
            "ENTER USERNAME: ".rjust(self.utils.TEXT_PADDING // 2 + 4)
        ).upper()

        users_manager.register(self.username)

        self.snd.play_pluck()
        self.snd.stop_menu()
        self.utils.toggle_cursor()

    def prompt_for_bet(self) -> int:
        """Clear the terminal and ask the user for a bet."""

        self.utils.clear_term()
        self.utils.toggle_cursor()

        bet: int = int(input("ENTER BET: ".rjust(self.utils.TEXT_PADDING // 2 + 4)))

        self.snd.play_pluck()
        self.snd.stop_menu()
        self.utils.toggle_cursor()

        return bet
