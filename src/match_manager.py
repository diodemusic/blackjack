"""Match module."""

import random

from deck_manager import Card
from theme_manager import Theme
from utils_manager import Utils


class Match:
    """
    Contains the game logic for dealing cards and printing them.

    Args:
        _Utils (class): Inherits the _Utils class.
    """

    def __init__(self, deck: list[Card]) -> None:
        self.theme = Theme()
        self.utils = Utils()

        self.card_spacing: int = 0
        self.deck: list[Card] = deck
        self.dealer_hand: list[Card] = []
        self.player_hand: list[Card] = []

    def __repr__(self) -> str:
        # pylint: disable=locally-disabled line-too-long

        return f"Match(deck={self.deck}, dealer_hand={self.dealer_hand}, player_hand={self.player_hand}, card_spacing={self.card_spacing})"

    def deal_card(self, dealer: bool = False) -> None:
        """
        Append a card to the dealer or players hand list.

        Args:
            dealer (bool, optional): Wether to deal to the dealer or the player.
            Defaults to False.
        """

        card: Card = self.deck.pop(random.randrange(start=0, stop=len(self.deck)))

        if not dealer:
            self.player_hand.append(card)
            return

        self.dealer_hand.append(card)

    def print_card(self, card: Card, hidden: bool = False) -> None:
        """
        Print the ascii representation of the Card object.

        Args:
            card (Card): The Card object to print.
            hidden (bool, optional): Wether or not the card should be face down.
            Defaults to False.
        """

        ascii_card: str = card.get_ascii_card(hidden)

        for line in ascii_card.splitlines():
            print(self.theme.card_color + " " * self.card_spacing, line)

        self.card_spacing += 3

    def print_hands(self, username: str, hide_dealer_card: bool = True) -> None:
        """
        Clear the terminal and print both the dealers and players hands.

        Args:
            username (str): The users username
            hide_dealer_card (bool, optional): Wether or not to hide the dealers 2nd card.
            Defaults to True.
        """

        self.card_spacing = 0

        self.utils.clear_term()
        print(self.theme.text_color + "\nDEALERS CARDS:")

        self.print_card(self.dealer_hand[0])
        self.print_card(self.dealer_hand[1], hidden=hide_dealer_card)

        for dealer_card in self.dealer_hand[2:]:
            self.print_card(dealer_card)

        self.card_spacing = 0

        print(self.theme.text_color + f"\n{username} CARDS:")

        for player_card in self.player_hand:
            self.print_card(player_card)
