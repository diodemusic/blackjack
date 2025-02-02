"""UsersManager module."""

from database_manager import Database


class UsersManager:
    """Handles interactions with the users."""

    def __init__(self) -> None:
        self.db = Database()

    def get_user(self, username: str) -> dict[str, str | int] | None:
        """
        Get a user dict from users.json

        Args:
            username (str): Username string.

        Returns:
            dict[str, str | int] | None: User dict.
        """

        users: list[dict[str, str | int]] = self.db.read()

        for user in users:
            if user.get("username") == username:
                return user

        return None

    def register(self, username: str) -> None:
        """Register a new user into users.json"""

        user: dict[str, str | int] | None = self.get_user(username)

        if user:
            return

        self.db.create({"username": username, "chips": 1000})
