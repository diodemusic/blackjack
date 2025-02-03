"""Chips module."""

from database_manager import Database
from users_manager import UsersManager


class Chips:
    """Handles the users chips."""

    def __init__(self) -> None:
        self.db = Database()
        self.usrs = UsersManager()

    def get_chips(self, username: str) -> str | int | float:
        """
        Get the users chips amount.
        If the user has 0 chips, give them 1000.

        Args:
            username (str): Username.

        Returns:
            str | int | None: Chips amount.
        """

        user: dict[str, str | int | float] = self.usrs.get_user(username)

        if not user:
            return 0

        if user.get("chips", 0) == 0:
            user["chips"] = 1000

        return user.get("chips", 0)

    def add_or_remove_chips(self, username: str, amount: int) -> None:
        """
        Add chips to the users.json user.

        Args:
            username (str): Username string.
            amount (int): Amount of chips to add to the users balance.
        """

        chips_balance: str | int | float = self.get_chips(username)

        if not isinstance(chips_balance, int):
            return

        new_chips_balance: int = chips_balance + amount

        print(f"NEW BALANCE: {new_chips_balance} chips\n")

        self.db.update(username, "chips", new_chips_balance)
