"""Card and Deck module."""


class Card:
    """Represents a playing card."""

    def __init__(self, name: str, points: int, suit: str) -> None:
        self.name: str = name
        self.points: int = points
        self.suit: str = suit

    def __repr__(self) -> str:
        return f"Card(name={self.name}, points={self.points}, suit={self.suit})"

    def get_ascii_card(self, hidden: bool = False) -> str:
        """
        Gets the ascii representation of the Card object.

        Args:
            hidden (bool, optional): Wether or not the ascii card should be printed face down.
            Defaults to False.

        Returns:
            str: The ascii representation of the Card object.
        """

        if hidden:
            return """ _____
|?    |
|}}:{{|
|}}:{{|
|}}:{{|
|____?|"""

        if self.name == "10":
            card_name: str = self.name[:2]
            card_top: str = f""" _____
|{card_name}   |"""
            card_bottom: str = f"|___{card_name}|"
        else:
            card_name = self.name[0].upper()
            card_top = f""" _____
|{card_name}    |"""
            card_bottom = f"|____{card_name}|"

        heart_card: str = f"""{card_top}
| ♥ ♥ |
|♥ ♥ ♥|
| ♥ ♥ |
{card_bottom}"""

        diamond_card: str = f"""{card_top}
| ♦ ♦ |
|♦ ♦ ♦|
| ♦ ♦ |
{card_bottom}"""

        spade_card: str = f"""{card_top}
| ♠ ♠ |
|♠ ♠ ♠|
| ♠ ♠ |
{card_bottom}"""

        club_card: str = f"""{card_top}
| ♣ ♣ |
|♣ ♣ ♣|
| ♣ ♣ |
{card_bottom}"""

        suits: dict[str, str] = {
            "hearts": heart_card,
            "diamonds": diamond_card,
            "spades": spade_card,
            "clubs": club_card,
        }

        return suits[self.suit]


class Deck:
    """Represents a deck of playing cards made up of Card objects"""

    FACE_CARDS: dict[str, int] = {
        "ace": 11,
        "king": 10,
        "queen": 10,
        "jack": 10,
    }
    SUITS: list[str] = [
        "hearts",
        "diamonds",
        "spades",
        "clubs",
    ]

    def create_deck(self) -> list[Card]:
        """
        Create a standard 52 deck of cards made up of Card objects.

        Returns:
            list[Card]: List of Card objects.
        """

        cards: list[Card] = []

        for suit in self.SUITS:
            for face_card, value in self.FACE_CARDS.items():
                cards.append(
                    Card(
                        name=face_card,
                        points=value,
                        suit=suit,
                    )
                )

            for i in range(2, 11):
                card = Card(name=str(i), points=i, suit=suit)
                cards.append(card)

        return cards

    def __repr__(self) -> str:
        return "Deck()"
