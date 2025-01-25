import random
import os

username = "kieran"  # TODO: input("Enter username: ")

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

    def get_ascii_card(self, hidden: bool = False) -> str:
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

    def deal_card(self, dealer: bool = False) -> None:
        card = self.deck.cards.pop(random.randrange(len(self.deck.cards)))

        if not dealer:
            self.player_hand.append(card)
        else:
            self.dealer_hand.append(card)

    def print_hands(self):
        os.system("cls" if os.name == "nt" else "clear")

        print("\nDealer cards:")

        print(Card.get_ascii_card(self.dealer_hand[0]))
        print(Card.get_ascii_card(self.dealer_hand[1], True))

        for card in self.dealer_hand[2:]:
            print(Card.get_ascii_card(card))

        print(f"\n{username.title()} cards:")

        for card in self.player_hand:
            print(Card.get_ascii_card(card))


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
                                f"\nYou have an {card.name} of {card.suit}, would you like it to count as 1 or 11 points? (1/11): "
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
    play_again = True

    deck = Deck()
    dealer = Dealer(deck)
    # TODO: points_calculator = PointsCalculator()

    while play_again:
        os.system("cls" if os.name == "nt" else "clear")

        dealer.dealer_hand = []
        dealer.player_hand = []

        dealer.deal_card(dealer=True)
        dealer.deal_card(dealer=True)

        dealer.deal_card()
        dealer.deal_card()

        dealer.print_hands()

        while True:
            hit_or_stand = input("\nHit or stand? (hit/stand): ")
            hit_or_stand = hit_or_stand.lower()

            if hit_or_stand != "hit" and hit_or_stand != "stand":
                print(f"'{hit_or_stand}' is not hit or stand")
                continue

            if hit_or_stand == "hit":
                dealer.deal_card()
                dealer.print_hands()

            break

        if hit_or_stand == "hit":
            dealer.deal_card()

        while True:
            play_again_prompt = input("Play again? (Y/n): ")
            play_again_prompt = play_again_prompt.lower()

            if play_again_prompt == "":
                break

            if play_again_prompt != "y" and play_again_prompt != "n":
                print(f"'{play_again_prompt}' is not y or n")
                continue

            if play_again_prompt == "y":
                play_again = True
            else:
                print("Goodbye")
                play_again = False
            break


if __name__ == "__main__":
    main()

# player_points = points_calculator.calculate_points(dealer.player_hand)
# dealer_points = points_calculator.calculate_points(dealer.dealer_hand)
