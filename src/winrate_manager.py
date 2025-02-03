"""Chips module."""

from database_manager import Database
from users_manager import UsersManager


class WinRate:
    """Handles the users chips."""

    def __init__(self) -> None:
        self.db = Database()
        self.usrs = UsersManager()

    def add_win(self, username: str) -> None:
        """
        Add Win to the users.json user.

        Args:
            username (str): Username string.
        """

        user: dict[str, str | int | float] | None = self.usrs.get_user(username)

        if not user:
            return

        wins: str | int | float = user.get("wins", 0)

        if not isinstance(wins, int):
            return

        self.db.update(username, "wins", wins + 1)

    def add_loss(self, username: str) -> None:
        """
        Add Loss to the users.json user.

        Args:
            username (str): Username string.
        """

        user: dict[str, str | int | float] | None = self.usrs.get_user(username)

        if not user:
            return

        losses: str | int | float = user.get("losses", 0)

        if not isinstance(losses, int):
            return

        self.db.update(username, "losses", losses + 1)

    def add_game_played(self, username: str) -> None:
        """
        Add game played to the users.json user.

        Args:
            username (str): Username string.
        """

        user: dict[str, str | int | float] | None = self.usrs.get_user(username)

        if not user:
            return

        games_played: str | int | float = user.get("games_played", 0)

        if not isinstance(games_played, int):
            return

        self.db.update(username, "games_played", games_played + 1)

    def update_winrate(self, username: str) -> None:
        """
        Add game played to the users.json user.

        Args:
            username (str): Username string.
        """

        user: dict[str, str | int | float] | None = self.usrs.get_user(username)

        if not user:
            return

        wins: str | int | float = user.get("wins", 0)
        games_played: str | int | float = user.get("games_played", 0)

        winrate: float = int(wins) / int(games_played)

        if not isinstance(winrate, float):
            return

        self.db.update(username, "winrate", winrate * 100)
