"""Main menu module."""

import time
from typing import Literal

import keyboard  # type: ignore

from chips_manager import Chips
from sound_manager import SoundManager
from theme_manager import Theme
from users_manager import UsersManager
from utils_manager import Utils


class MainMenu:
    """
    Main menu UI class.

    Args:
        _Utils (class): Inherits the _Utils class.
        SoundManager (class): Inherits the SoundManager class.
    """

    def __init__(self) -> None:
        self.chips = Chips()
        self.sound = SoundManager()
        self.theme = Theme()
        self.utils = Utils()

        self.username: str | Literal[""] = ""

    def title_screen(self) -> None:
        """Clear the terminal and print the main title screen."""

        self.sound.play_menu()
        self.utils.clear_term()
        self.utils.toggle_cursor()

        print(self.theme.text_color + self.utils.TITLE + "\n")
        print(self.theme.text_color + self.utils.START_GAME_PROMPT)

        while True:
            event: keyboard.KeyboardEvent = keyboard.read_event(suppress=True)

            if event.event_type == "down":
                if event.name == "enter":
                    self.sound.play_pluck()
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

        self.sound.play_pluck()
        self.sound.stop_menu()
        self.utils.toggle_cursor()

        self.theme.set_theme(self.username, self.theme.theme_1)

    def bet_error(self, message: str) -> None:
        """
        Helper function for gracefully handling betting errors.

        Args:
            message (str): Error message to display to the user.
        """

        self.utils.toggle_cursor()
        print(
            "\n"
            + self.theme.text_color
            + message.center(self.utils.TEXT_PADDING // 2 + 37)
        )
        time.sleep(2)
        self.prompt_for_bet()

    def prompt_for_bet(self) -> int:
        """Clear the terminal and ask the user for a bet."""

        self.utils.clear_term()
        self.utils.toggle_cursor()

        current_balance: str | int | float = self.chips.get_chips(self.username)

        print(
            f"{self.theme.text_color} CURRENT BALANCE: {current_balance}\n".rjust(
                self.utils.TEXT_PADDING // 2 + 9
            )
        )

        bet_str: str = input("ENTER BET: ".rjust(self.utils.TEXT_PADDING // 2 + 4))

        try:
            bet: int = int(bet_str)
        except ValueError:
            bet = 0
            self.bet_error("BET MUST BE A NUMBER")

        if not isinstance(current_balance, int):
            return 0

        if bet > current_balance:
            self.bet_error("BET CANNOT EXCEED BALANCE.")
        if bet <= 0:
            self.bet_error("BET MUST BE GREATER THAN 0.")

        self.sound.play_pluck()
        self.sound.stop_menu()
        self.utils.toggle_cursor()

        return bet
