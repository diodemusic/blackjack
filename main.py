import random

face_cards: dict = {
    "ace": {"is_21": 11, "is_not_21": 1},
    "king": 10,
    "queen": 10,
    "joker": 10,
}


suits: dict = [
    "hearts",
    "diamonds",
    "kings",
    "clubs",
]


class Card:
    def __init__(self, number: int, suit: str, is_face_card: bool = False) -> None:
        self.number: int | tuple = number
        self.suit: str = suit
        self.is_face_card: bool = is_face_card

    def __repr__(self) -> str:
        return f"Card(number={self.number}, suit={self.suit}, is_face_card={self.is_face_card})"


class Deck:
    def __init__(self) -> None:
        self.cards: list = []

        for suit in suits:
            for face_card, value in face_cards.items():
                self.cards.append(
                    Card(
                        number=(face_card, value),
                        suit=suit,
                        is_face_card=True,
                    )
                )

            for i in range(1, 11):
                card = Card(i, suit)
                self.cards.append(card)

    def __repr__(self) -> str:
        return f"Deck(cards={self.cards})"

    def deal_card(self, user: str, hidden: bool = False) -> list:
        card = random.choice(self.cards)
        self.cards.remove(card)
        print(self.cards)

        if not hidden:
            print(f"Dealt a {card.number} of {card.suit} to {user}")
        else:
            print(f"Dealt a card to {user}")


class Hand:
    def __init__(self, cards) -> None:
        self.cards = cards

    def __repr__(self) -> str:
        return f"Hand(cards={self.cards})"


class PointsCalculator:
    def __init__(self) -> None:
        self.points: int = 0

    def __repr__(self) -> str:
        return f"PointsCalculator(points={self.points})"

    def calculate_points(self, hand) -> int:
        pass


class Dealer:
    def __init__(self, deck: Deck) -> None:
        self.deck = deck

    def deal(self) -> None:  # TODO: maybe return somthing
        player_hand: list = []
        dealer_hand: list = []

        player_hand.append(self.deck.deal_card("player"))
        dealer_hand.append(self.deck.deal_card("dealer"))
        player_hand.append(self.deck.deal_card("player"))
        dealer_hand.append(self.deck.deal_card("dealer", hidden=True))


deck = Deck()
dealer = Dealer(deck)
dealer.deal()
