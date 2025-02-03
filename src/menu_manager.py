"""Main menu module."""

import time
from typing import Literal

import keyboard  # type: ignore

from chips_manager import Chips
from sound_manager import SoundManager
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
        self.utils = Utils()
        self.snd = SoundManager()
        self.chps = Chips()

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

    def bet_error(self, message: str) -> None:
        """
        Helper function for gracefully handling betting errors.

        Args:
            message (str): Error message to display to the user.
        """

        self.utils.toggle_cursor()
        print("\n" + message.center(self.utils.TEXT_PADDING // 2 + 37))
        time.sleep(2)
        self.prompt_for_bet()

    def prompt_for_bet(self) -> int | None:
        """Clear the terminal and ask the user for a bet."""

        self.utils.clear_term()
        self.utils.toggle_cursor()

        current_balance: str | int | None = self.chps.get_chips(self.username)

        print(
            f"CURRENT BALANCE: {current_balance}\n".rjust(
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
            return None

        if bet > current_balance:
            self.bet_error("BET CANNOT EXCEED BALANCE.")
        if bet <= 0:
            self.bet_error("BET MUST BE GREATER THAN 0.")

        self.snd.play_pluck()
        self.snd.stop_menu()
        self.utils.toggle_cursor()

        return bet
