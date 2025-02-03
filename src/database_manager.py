"""Database module."""

import io
import json
import os


class Database:
    """Handles creating database entries"""

    FILE_NAME: str = "users.json"
    PATH: str = os.path.join("..", "users", FILE_NAME)
    ENCODING: str = "utf-8"
    JSON_INDENT = 4

    def __init__(self) -> None:
        self.create_json()

        self.users_list: list[dict[str, str | int | float]] = self.read()

    def create_json(self) -> None:
        """Creates a users.json file in users\\ if it doesn't already exist."""

        if not os.path.exists("..\\users"):
            os.makedirs("..\\users")

        if not os.path.isfile(self.PATH) and not os.access(self.PATH, os.R_OK):
            with io.open(self.PATH, "w", encoding=self.ENCODING) as db_f:
                db_f.write(json.dumps([], indent=self.JSON_INDENT))

    def read(self) -> list[dict[str, str | int | float]]:
        """
        Read users.json file.

        Returns:
            Any: Returns the output of the json.load() method.
        """

        with open(self.PATH, "r", encoding=self.ENCODING) as f:
            user_database: list[dict[str, str | int | float]] = json.load(f)

        return user_database

    def create(self, content: dict[str, str | int | float]) -> None:
        """
        Write dict content to users file.

        Args:
            content (dict): The user dict to write to users.json
        """

        with open(self.PATH, "w", encoding=self.ENCODING) as f:
            self.users_list.append(content)
            json.dump(self.users_list, f, indent=self.JSON_INDENT)

    def update(self, username: str, key: str, value: str | int | float) -> None:
        """
        Update a dict in the users.json list.

        Args:
            username (str): Username string.
            key (str): Dict key of the value you want to change.
            value (str | int): The new value.
        """

        users: list[dict[str, str | int | float]] = self.read()

        for user in users:
            if user.get("username", "username") == username:
                user[key] = value

        with open(self.PATH, "w", encoding=self.ENCODING) as f:
            json.dump(users, f, indent=self.JSON_INDENT)
