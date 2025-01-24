from dataclasses import dataclass, fields


class Card:
    def __init__(self, number: int, suit: str) -> None:
        self.number = number
        self.suit = suit

    def __repr__(self):
        return f"Card(number={self.number}, suit={self.suit})"


@dataclass
class SpecialNumber:
    ace = 0
    king = 0
    queen = 0
    joker = 0


@dataclass
class Suit:
    hearts = "hearts"
    diamonds = "diamonds"
    spades = "spades"
    clubs = "clubs"


for field in fields(Suit):
    pass

ace_of_spades = Card(SpecialNumber.ace, Suit.spades)
print(ace_of_spades.__repr__())
