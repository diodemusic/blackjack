"""UsersManager module."""

from database_manager import Database


class UsersManager:
    """Handles interactions with the users."""

    def __init__(self) -> None:
        self.db = Database()

    def get_user(self, username: str) -> dict[str, str | int | float]:
        """
        Get a user dict from users.json

        Args:
            username (str): Username string.

        Returns:
            dict[str, str | int | float] | None: User dict.
        """

        users: list[dict[str, str | int | float]] = self.db.read()

        for user in users:
            if user.get("username") == username:
                return user

        return {}

    def register(self, username: str) -> None:
        """Register a new user into users.json"""

        user: dict[str, str | int | float] | None = self.get_user(username)

        if user:
            return

        self.db.create(
            {
                "username": username,
                "chips": 1000,
                "wins": 0,
                "losses": 0,
                "games_played": 0,
                "winrate": 0.1,
            }
        )
