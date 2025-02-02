"""Chips module."""

from database_manager import Database
from users_manager import UsersManager


class Chips:
    """Handles the users chips."""

    def __init__(self) -> None:
        self.db = Database()
        self.usrs = UsersManager()

    def get_chips(self, username: str) -> str | int | None:
        """
        Get the users chips amount.

        Args:
            username (str): Username.

        Returns:
            str | int | None: Chips amount.
        """

        user: dict[str, str | int] | None = self.usrs.get_user(username)

        if user:
            return user.get("chips")

        return None

    def add_or_remove_chips(self, username: str, amount: int) -> None:
        """
        Add chips to the users.json user.

        Args:
            username (str): Username string.
            amount (int): Amount of chips to add to the users balance.
        """

        chips_balance: str | int | None = self.get_chips(username)

        if not isinstance(chips_balance, int):
            return

        new_chips_balance: int = chips_balance + amount

        print(f"NEW BALANCE: {new_chips_balance} chips\n")

        self.db.update(username, "chips", new_chips_balance)
