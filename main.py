import random
import os
import cursor
from pygame import mixer  # This is only for playing audio
from colorama import Fore
import time
import keyboard

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
    CARD_COLOR: str = Fore.WHITE

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
        self.clear_term()
        print(self.TEXT_COLOR + self.title + "\n")
        print(self.TEXT_COLOR + self.start_game_prompt)
        input()

    def prompt_for_username(self) -> None:
        self.clear_term()

        print(self.title, "\n")
        self.username = input(
            "ENTER USERNAME: ".rjust(self.TEXT_PADDING // 2 + 4)
        ).upper()

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
    close_game_path = audio_dir + "close_game.mp3"

    menu = mixer.Sound(menu_path)
    pluck = mixer.Sound(pluck_path)
    game_start = mixer.Sound(game_start_path)
    in_game = mixer.Sound(in_game_path)
    game_over = mixer.Sound(game_over_path)
    close_game = mixer.Sound(close_game_path)

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

    def play_close_game(self) -> None:
        self.close_game.play()


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

        if self.name == "10":
            card_name = self.name[:2]
            card_top = f""" _____
|{card_name}   |"""
            card_bottom = f"|___{card_name}|"
        else:
            card_name = self.name[0].upper()
            card_top = f""" _____
|{card_name}    |"""
            card_bottom = f"|____{card_name}|"

        heart_card = f"""{card_top}
| ♥ ♥ |
|♥ ♥ ♥|
| ♥ ♥ |
{card_bottom}"""

        diamond_card = f"""{card_top}
| ♦ ♦ |
|♦ ♦ ♦|
| ♦ ♦ |
{card_bottom}"""

        spade_card = f"""{card_top}
| ♠ ♠ |
|♠ ♠ ♠|
| ♠ ♠ |
{card_bottom}"""

        club_card = f"""{card_top}
| ♣ ♣ |
|♣ ♣ ♣|
| ♣ ♣ |
{card_bottom}"""

        suits: dict[str:str] = {
            "hearts": heart_card,
            "diamonds": diamond_card,
            "spades": spade_card,
            "clubs": club_card,
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


class Dealer(_Utils):
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

    def print_card(self, card: Card, hidden: bool = False) -> None:
        ascii_card = Card.get_ascii_card(card, hidden)

        for line in ascii_card.splitlines():
            print(_Utils.CARD_COLOR + " " * self.card_spacing, line)

        self.card_spacing += 3

    def print_hands(self, username: str, hide_dealer_card: bool = True):
        self.card_spacing = 0

        self.clear_term()
        print(_Utils.TEXT_COLOR + "\nDEALERS CARDS:")

        self.print_card(self.dealer_hand[0])
        self.print_card(self.dealer_hand[1], hidden=hide_dealer_card)

        for dealer_card in self.dealer_hand[2:]:
            self.print_card(dealer_card)

        self.card_spacing = 0

        print(_Utils.TEXT_COLOR + f"\n{username} CARDS:")

        for player_card in self.player_hand:
            self.print_card(player_card)


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


class MainMenu:
    pass


class BlackjackGameManager:
    play_again = True
    play_again_key_pressed = False

    deck = Deck()
    dealer = Dealer(deck)
    points_calculator = PointsCalculator()
    _utils = _Utils()
    sound = SoundManager()

    def init_game(self) -> None:
        self.sound.play_menu()
        self._utils.start_menu()
        self.sound.play_pluck()
        self._utils.prompt_for_username()

    def start_game(self) -> None:
        self.sound.play_pluck()
        self.sound.stop_menu()
        self.sound.play_in_game()

    def deal_initial_hands(self) -> None:
        self.sound.play_game_start()

        self.dealer.dealer_hand = []
        self.dealer.player_hand = []

        self.dealer.deal_card(dealer=True)
        self.dealer.deal_card(dealer=True)

        self.dealer.deal_card()
        self.dealer.deal_card()

        self.dealer.print_hands(self._utils.username)

    def hit_or_stand(self) -> None:
        print("\n" + self._utils.TEXT_COLOR + "[H]: HIT [S]: STAND")

        while True:
            event = keyboard.read_event(suppress=True)

            if event.event_type == "down":
                if event.name == "h":
                    self.sound.play_pluck()
                    self.dealer.deal_card()
                    self.dealer.print_hands(self._utils.username)

                    player_points = self.points_calculator.calculate_points(
                        self.dealer.player_hand
                    )

                    if player_points > 21:
                        self.sound.play_game_over()
                        print("\n" + self._utils.TEXT_COLOR + "BUST")
                        break
                    else:
                        print("\n" + self._utils.TEXT_COLOR + "[H]: HIT [S]: STAND")
                        continue
                elif event.name == "s":
                    player_points = self.points_calculator.calculate_points(
                        self.dealer.player_hand
                    )
                    dealer_points = self.points_calculator.calculate_points(
                        self.dealer.dealer_hand
                    )

                    self.dealer.print_hands(
                        self._utils.username, hide_dealer_card=False
                    )

                    if dealer_points > 21:
                        print("\n" + self._utils.TEXT_COLOR + "DEALER BUST")
                        print(self._utils.TEXT_COLOR + "YOU WIN!" + "\n")
                        break
                    elif player_points > dealer_points:
                        print("\n" + self._utils.TEXT_COLOR + "YOU HAVE MORE POINTS")
                        print(self._utils.TEXT_COLOR + "YOU WIN!" + "\n")
                        break
                    elif player_points < dealer_points:
                        self.sound.play_game_over()
                        print("\n" + self._utils.TEXT_COLOR + "YOU HAVE LESS POINTS")
                        print(self._utils.TEXT_COLOR + "YOU LOSE" + "\n")
                        break
                    elif player_points == dealer_points:
                        print("\n" + self._utils.TEXT_COLOR + "ITS A TIE" + "\n")
                        break
                else:
                    continue

    def game_over(self) -> None:
        print(self._utils.TEXT_COLOR + "[ENTER]: PLAY AGAIN [ESC]: QUIT")

        while True:
            event = keyboard.read_event(suppress=True)

            if event.event_type == "down":
                if event.name == "enter":
                    self.sound.play_pluck()
                    break
                elif event.name == "esc":
                    self.sound.stop_in_game()
                    self._utils.clear_term()
                    self.sound.play_close_game()
                    print(_Utils.TEXT_COLOR + "GOODBYE" + Fore.WHITE)
                    time.sleep(1)
                    quit()

    def play(self) -> None:
        self.init_game()
        self.start_game()

        while self.play_again:
            self.deal_initial_hands()
            self.hit_or_stand()
            self.game_over()


if __name__ == "__main__":
    blackjack = BlackjackGameManager()
    blackjack.play()
