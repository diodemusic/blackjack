"""UsersManager module."""

from typing import Any

from database import Database

database = Database()


class UsersManager:
    """Handles the user object."""

    def register(self, username: str) -> None:
        """Register a new user into users.json"""

        users: Any = database.read()

        for user in users:
            if username in user:
                return

        database.create({"username": username})
