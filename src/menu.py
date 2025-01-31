"""Main menu module."""

import keyboard  # type: ignore

from _utils import _Utils
from sound import SoundManager


class MainMenu(_Utils, SoundManager):
    """
    Main menu UI class.

    Args:
        _Utils (class): Inherits the _Utils class.
        SoundManager (class): Inherits the SoundManager class.
    """

    def title_screen(self) -> None:
        """Clear the terminal and print the main title screen."""

        self.play_menu()
        self.clear_term()
        self.toggle_cursor()

        print(self.TEXT_COLOR + self.TITLE + "\n")
        print(self.TEXT_COLOR + self.START_GAME_PROMPT)

        while True:
            event = keyboard.read_event(suppress=True)

            if event.event_type == "down":
                if event.name == "enter":
                    self.play_pluck()
                    return

                continue

    def prompt_for_username(self) -> None:
        """Clear the terminal and ask the user for a username."""

        self.clear_term()
        self.toggle_cursor()

        self.username = input(
            "ENTER USERNAME: ".rjust(self.TEXT_PADDING // 2 + 4)
        ).upper()
        self.play_pluck()
        self.stop_menu()
        self.toggle_cursor()
