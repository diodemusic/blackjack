import random
import os
import cursor
from pygame import mixer  # This is only for playing audio
from colorama import Fore
import curses

FACE_CARDS: dict[str:int] = {
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


class _Utils:
    TEXT_PADDING: int = 80
    TEXT_COLOR: str = Fore.LIGHTRED_EX
    DEALER_CARDS_COLOR: str = Fore.RED
    PLAYER_CARDS_COLOR: str = Fore.BLUE

    def __init__(self):
        self.title = """88          88                       88        88                       88         
88          88                       88        ""                       88         
88          88                       88                                 88         
88,dPPYba,  88 ,adPPYYba,  ,adPPYba, 88   ,d8  88 ,adPPYYba,  ,adPPYba, 88   ,d8   
88P'    "8a 88 ""     `Y8 a8"     "" 88 ,a8"   88 ""     `Y8 a8"     "" 88 ,a8"    
88       d8 88 ,adPPPPP88 8b         8888[     88 ,adPPPPP88 8b         8888[      
88b,   ,a8" 88 88,    ,88 "8a,   ,aa 88`"Yba,  88 88,    ,88 "8a,   ,aa 88`"Yba,   
8Y"Ybbd8"'  88 `"8bbdP"Y8  `"Ybbd8"' 88   `Y8a 88 `"8bbdP"Y8  `"Ybbd8"' 88   `Y8a  
                                              ,88                                  
                                            888P\"""".center(self.TEXT_PADDING)

        self.start_game_prompt = "PRESS [ENTER] TO PLAY...".center(self.TEXT_PADDING)
        self.username = ""
        self.cursor_off = False

    def start_menu(self):
        self.toggle_cursor()
        self.clear_term()
        print(self.TEXT_COLOR + self.title + "\n")
        print(self.TEXT_COLOR + self.start_game_prompt)
        input()

    def prompt_for_username(self) -> None:
        self.clear_term()
        print(self.title, "\n")
        self.username = input("ENTER USERNAME: ".center(self.TEXT_PADDING)).upper()

    def toggle_cursor(self) -> None:
        if not self.cursor_off:
            cursor.hide()
            self.cursor_off = True
            return
        cursor.show()
        self.cursor_off = False

    def clear_term(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")


class SoundManager:
    mixer.init()

    audio_dir = "audio\\"

    menu_path = audio_dir + "menu.mp3"
    pluck_path = audio_dir + "pluck.mp3"
    game_start_path = audio_dir + "game_start.mp3"
    in_game_path = audio_dir + "in_game.mp3"
    game_over_path = audio_dir + "game_over.mp3"

    menu = mixer.Sound(menu_path)
    pluck = mixer.Sound(pluck_path)
    game_start = mixer.Sound(game_start_path)
    in_game = mixer.Sound(in_game_path)
    game_over = mixer.Sound(game_over_path)

    def play_menu(self) -> None:
        self.menu.play(loops=-1)

    def stop_menu(self) -> None:
        self.menu.stop()

    def play_game_start(self) -> None:
        self.game_start.play()

    def play_in_game(self) -> None:
        self.in_game.play(loops=-1)

    def stop_in_game(self) -> None:
        self.in_game.stop()

    def play_pluck(self) -> None:
        self.pluck.play()

    def play_game_over(self) -> None:
        self.game_over.play()


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
|?    |
|}}:{{|
|}}:{{|
|}}:{{|
|____?|"""

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
        self.card_spacing = 0

    def deal_card(self, dealer: bool = False) -> None:
        card = self.deck.cards.pop(random.randrange(len(self.deck.cards)))

        if not dealer:
            self.player_hand.append(card)
        else:
            self.dealer_hand.append(card)

    def print_card(self, card: Card, hidden: bool = False, dealer=True) -> None:
        ascii_card = Card.get_ascii_card(card, hidden)

        if dealer:
            for line in ascii_card.splitlines():
                print(_Utils.DEALER_CARDS_COLOR + " " * self.card_spacing, line)
        else:
            for line in ascii_card.splitlines():
                print(_Utils.PLAYER_CARDS_COLOR + " " * self.card_spacing, line)

        self.card_spacing += 3

    def print_hands(self, username: str):
        self.card_spacing = 0

        print(_Utils.TEXT_COLOR + "\nDEALERS CARDS:")

        self.print_card(self.dealer_hand[0])
        self.print_card(self.dealer_hand[1], hidden=True)

        for dealer_card in self.dealer_hand[2:]:
            self.print_card(dealer_card)

        self.card_spacing = 0

        print(_Utils.TEXT_COLOR + f"\n{username} CARDS:")

        for player_card in self.player_hand:
            self.print_card(player_card, dealer=False)


class PointsCalculator:
    def __init__(self) -> None:
        self.points: int = 0

    def __repr__(self) -> str:
        return f"PointsCalculator(points={self.points})"

    def calculate_points(self, hand: list[Card]) -> int:
        self.points = 0

        for card in hand:
            self.points += card.points

        return self.points


class Match: ...  # TODO: move main logic to this Match class


def main():
    play_again = True

    deck = Deck()
    dealer = Dealer(deck)
    points_calculator = PointsCalculator()
    _utils = _Utils()
    sound = SoundManager()

    sound.play_menu()
    _utils.start_menu()
    sound.play_pluck()
    _utils.prompt_for_username()
    sound.play_pluck()

    sound.stop_menu()

    while play_again:
        _utils.clear_term()
        sound.play_game_start()
        sound.stop_in_game()
        sound.play_in_game()

        dealer.dealer_hand = []
        dealer.player_hand = []

        dealer.deal_card(dealer=True)
        dealer.deal_card(dealer=True)

        dealer.deal_card()
        dealer.deal_card()

        _utils.clear_term()
        dealer.print_hands(_utils.username)

        _utils.toggle_cursor()

        while True:
            hit_or_stand = input(_Utils.TEXT_COLOR + "\nHIT OR STAND? (H/S): ")
            sound.play_pluck()
            hit_or_stand = hit_or_stand.lower()

            if hit_or_stand != "h" and hit_or_stand != "s":
                print(_Utils.TEXT_COLOR + f"'{hit_or_stand.upper()}' IS NOT H OR S")
                continue

            if hit_or_stand == "h":
                dealer.deal_card()
                _utils.clear_term()
                dealer.print_hands(_utils.username)

                player_points = points_calculator.calculate_points(dealer.player_hand)

                print(dealer.dealer_hand)
                print(dealer.player_hand)
                print(player_points)

                if player_points > 21:
                    sound.stop_in_game()
                    sound.play_game_over()
                    print("BUST")
                    input("PRESS [ENTER] TO CONTINUE")
                    sound.play_pluck()
                    break

        while True:
            play_again_prompt = input("\nPLAY AGAIN? (Y/N): ")
            sound.play_pluck()
            play_again_prompt = play_again_prompt.lower()

            if play_again_prompt == "":
                break

            if play_again_prompt != "y" and play_again_prompt != "n":
                print(_Utils.TEXT_COLOR + f"'{play_again_prompt}' IS NOT Y OR N")
                continue

            if play_again_prompt == "y":
                play_again = True
            else:
                _utils.clear_term()
                print(_Utils.TEXT_COLOR + "GOODBYE 😈")
                print(Fore.WHITE)
                cursor.show()
                play_again = False
            break


if __name__ == "__main__":
    main()

# player_points = points_calculator.calculate_points(dealer.player_hand)
# dealer_points = points_calculator.calculate_points(dealer.dealer_hand)
