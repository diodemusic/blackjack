"""Theme module."""

from colorama import Fore  # type: ignore

from users_manager import UsersManager
from database_manager import Database


class Theme:
    """Handles the console theme per user."""

    theme_1: dict[str, str] = {
        "text_color": Fore.WHITE,
        "card_color": Fore.WHITE,
        "background_color": Fore.BLACK,
    }
    theme_2: dict[str, str] = {
        "text_color": Fore.LIGHTRED_EX,
        "card_color": Fore.WHITE,
        "background_color": Fore.BLACK,
    }

    def __init__(self) -> None:
        self.database = Database()
        self.users = UsersManager()

        self.text_color: str = Fore.WHITE
        self.card_color: str = Fore.WHITE
        self.background_color: str = Fore.BLACK

    def set_theme(self, username: str, theme: dict[str, str]) -> None:
        """Set a users theme."""

        for key, value in theme.items():
            self.database.update(username, key, value)

        self.text_color = theme.get("text_color", Fore.WHITE)
        self.card_color = theme.get("card_color", Fore.WHITE)
        self.background_color = theme.get("background_color", Fore.BLACK)
