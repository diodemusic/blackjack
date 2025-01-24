import random

face_cards: dict = {
    "ace": 11,
    "king": 10,
    "queen": 10,
    "joker": 10,
}


suits: list = [
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


class Deck:
    def __init__(self) -> None:
        self.cards: list[Card] = []

        for suit in suits:
            for face_card, value in face_cards.items():
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

    def deal_card(
        self, user: str = "dealer", hidden: bool = False
    ) -> None:  # TODO: maybe return somthing
        card = self.deck.cards.pop(random.randrange(len(self.deck.cards)))
        if not hidden:
            print(f"Dealt a {card.name} of {card.suit} to {user}")
            return card
        print(f"Dealt a card to {user}")
        return card


class PointsCalculator:
    def __init__(self) -> None:
        self.points: int = 0

    def __repr__(self) -> str:
        return f"PointsCalculator(points={self.points})"

    def calculate_points(self, hand: list) -> int:
        points: int = 0

        for card in hand:
            if not card.name == "ace":
                points += card.points

        for card in hand:
            if card.name == "ace":
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

                    ace_points = int(ace_points)

                    if ace_points != 1 and ace_points != 11:
                        print("Please enter either 1 or 11")
                        continue

                    points += ace_points
                    break
            break
        return points


def main():
    username = "kieran"  # TODO: input("Enter username: ")

    deck = Deck()
    dealer = Dealer(deck)
    points_calculator = PointsCalculator()

    dealer_hand = []
    player_hand = []

    dealer_hand.append(dealer.deal_card())
    player_hand.append(dealer.deal_card(username))
    dealer_hand.append(dealer.deal_card(hidden=True))
    player_hand.append(dealer.deal_card(username))

    player_points = points_calculator.calculate_points(player_hand)
    print(player_points)


if __name__ == "__main__":
    main()
