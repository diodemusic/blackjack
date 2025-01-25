import random

FACE_CARDS: dict[str:int] = {
    "ace": 11,
    "king": 10,
    "queen": 10,
    "joker": 10,
}


SUITS: list[str] = [
    "hearts",
    "diamonds",
    "spades",
    "clubs",
]


class Card:
    def __init__(self, name: str, points: int, suit: str) -> None:
        self.name: str = name
        self.points: int = points
        self.suit: str = suit

    def __repr__(self) -> str:
        return f"Card(name={self.name}, points={self.points}, suit={self.suit})"

    def get_ascii_card(self, hidden: bool) -> str:
        if hidden:
            return """ _____
|\\ ~ /|
|}}:{{|
|}}:{{|
|}}:{{|
|/_~_\\|"""

        card_name = self.name[0].upper()
        suits = {
            "hearts": f""" _____
|{card_name}_ _ |
|( v )|
| \\ / |
|  .  |
|____{card_name}|""",
            "diamonds": f""" _____
|{card_name} ^  |
| / \\ |
| \\ / |
|  .  |
|____{card_name}|""",
            "spades": f""" _____
|{card_name} .  |
| /.\\ |
|(_._)|
|  |  |
|____{card_name}|""",
            "clubs": f""" _____
|{card_name} _  |
| ( ) |
|(_'_)|
|  |  |
|____{card_name}|""",
        }

        return suits[self.suit]


class Deck:
    def __init__(self) -> None:
        self.cards: list[Card] = []

        for suit in SUITS:
            for face_card, value in FACE_CARDS.items():
                self.cards.append(
                    Card(
                        name=face_card,
                        points=value,
                        suit=suit,
                    )
                )

            for i in range(2, 11):
                card = Card(name=str(i), points=i, suit=suit)
                self.cards.append(card)

    def __repr__(self) -> str:
        return f"Deck(cards={self.cards})"


class Dealer:
    def __init__(self, deck: Deck) -> None:
        self.deck = deck
        self.dealer_hand: list[Card] = []
        self.player_hand: list[Card] = []

    def deal_card(
        self, hidden: bool = False, dealer: bool = False, new_line: bool = True
    ) -> None:
        card = self.deck.cards.pop(random.randrange(len(self.deck.cards)))

        if not new_line:
            print(card.get_ascii_card(hidden))
        else:
            print(card.get_ascii_card(hidden))

        if not dealer:
            self.dealer_hand.append(card)
        else:
            self.player_hand.append(card)


class PointsCalculator:
    def __init__(self) -> None:
        self.points: int = 0

    def __repr__(self) -> str:
        return f"PointsCalculator(points={self.points})"

    def calculate_points(self, hand: list[Card]) -> int:
        points: int = 0

        for card in hand:
            if not card.name == "ace":
                points += card.points
            else:
                while True:
                    try:
                        ace_points = int(
                            input(
                                f"You have an {card.name} of {card.suit}, would you like it to count as 1 or 11 points? (1/11) "
                            )
                        )
                    except ValueError as e:
                        print(f"{e}: Please enter a number")
                        continue

                    if ace_points != 1 and ace_points != 11:
                        print("Please enter either 1 or 11")
                        continue

                    points += ace_points
                    break
        return points


class Match: ...  # TODO: move main logic to this Match class


def main():
    username = "kieran"  # TODO: input("Enter username: ")

    deck = Deck()
    dealer = Dealer(deck)
    points_calculator = PointsCalculator()

    while True:
        print("\nDealers cards:")
        dealer.deal_card(dealer=True)
        dealer.deal_card(dealer=True, hidden=True)

        print(f"\n{username.title()} cards:")
        dealer.deal_card()
        dealer.deal_card()

        player_points = points_calculator.calculate_points(dealer.player_hand)
        dealer_points = points_calculator.calculate_points(dealer.dealer_hand)

        print(player_points)
        print(dealer_points)

        print(dealer.dealer_hand)
        print(dealer.player_hand)


if __name__ == "__main__":
    main()
