"""Points calculator module."""

from deck import Card


class PointsCalculator:
    """Class to calculate the dealers or players hand."""

    def __init__(self) -> None:
        self.points: int = 0

    def __repr__(self) -> str:
        return f"PointsCalculator(points={self.points})"

    def count_non_aces(self, hand: list[Card]) -> int:
        """
        Count the points of all Card instances.

        Args:
            hand (list[Card]): List of Card objects.

        Returns:
            int: Total worth of the Card objects in points.
        """

        for card in hand:
            if card.name != "ace":
                self.points += card.points

        return self.points

    def count_aces(self, hand: list[Card]) -> int:
        """
        Count all Card instances that are aces.

        Args:
            hand (list[Card]): List of Card objects.

        Returns:
            int: Total worth of the Card objects in points.
        """

        for card in hand:
            if card.name == "ace" and self.points >= 11:
                self.points += 1
            elif card.name == "ace":
                self.points += 11

        return self.points

    def calculate_points(self, hand: list[Card]) -> int:
        """
        Calculate total points of Card objects.

        Args:
            hand (list[Card]): List of Card objects.

        Returns:
            int: Total worth of the Card objects in points.
        """

        self.points = 0
        self.points = self.count_non_aces(hand)
        self.points = self.count_aces(hand)

        return self.points
