import random
import os
import cursor
from pygame import mixer  # This is only for playing audio
from colorama import Fore
import time
import keyboard
import sys


class _Utils:
    TEXT_PADDING: int = 80
    TEXT_COLOR: str = Fore.LIGHTRED_EX
    CARD_COLOR: str = Fore.WHITE
    TITLE = """88          88                       88        88                       88         
88          88                       88        ""                       88         
88          88                       88                                 88         
88,dPPYba,  88 ,adPPYYba,  ,adPPYba, 88   ,d8  88 ,adPPYYba,  ,adPPYba, 88   ,d8   
88P'    "8a 88 ""     `Y8 a8"     "" 88 ,a8"   88 ""     `Y8 a8"     "" 88 ,a8"    
88       d8 88 ,adPPPPP88 8b         8888[     88 ,adPPPPP88 8b         8888[      
88b,   ,a8" 88 88,    ,88 "8a,   ,aa 88`"Yba,  88 88,    ,88 "8a,   ,aa 88`"Yba,   
8Y"Ybbd8"'  88 `"8bbdP"Y8  `"Ybbd8"' 88   `Y8a 88 `"8bbdP"Y8  `"Ybbd8"' 88   `Y8a  
                                            ,88                                  
                                        888P\"""".center(TEXT_PADDING)
    START_GAME_PROMPT = "PRESS [ENTER] TO PLAY...".center(TEXT_PADDING)

    username = ""
    cursor_off = False

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

    def __init__(self) -> None:
        self.cards: list[Card] = []

        for suit in self.SUITS:
            for face_card, value in self.FACE_CARDS.items():
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


class Match(_Utils):
    def __init__(self, deck: Deck) -> None:
        self.deck = deck
        self.dealer_hand: list[Card] = []
        self.player_hand: list[Card] = []
        self.card_spacing = 0

    def __repr__(self):
        return f"Match(deck={self.deck}, dealer_hand={self.dealer_hand}, player_hand={self.player_hand}, card_spacing={self.card_spacing})"

    def deal_card(self, dealer: bool = False) -> None:
        card = self.deck.cards.pop(random.randrange(start=0, stop=len(self.deck.cards)))

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
            if card.name != "ace":
                self.points += card.points

        for card in hand:
            if card.name == "ace":
                if self.points >= 11:
                    card.points = 1
                    self.points += card.points

        return self.points


class MainMenu(_Utils, SoundManager):
    def title_screen(self) -> None:
        self.play_menu()
        self.clear_term()
        self.toggle_cursor()

        print(self.TEXT_COLOR + self.TITLE + "\n")
        print(self.TEXT_COLOR + self.START_GAME_PROMPT)

        while True:
            event = keyboard.read_event(suppress=True)

            if event.event_type == "down":
                if event.name == "enter":
                    self.play_pluck()
                    return
                else:
                    continue

    def prompt_for_username(self) -> None:
        self.clear_term()
        self.toggle_cursor()

        self.username = input(
            "ENTER USERNAME: ".rjust(self.TEXT_PADDING // 2 + 4)
        ).upper()
        self.play_pluck()
        self.toggle_cursor()


class BlackjackGameManager(_Utils):
    play_again = True

    points_calculator = PointsCalculator()
    sound = SoundManager()
    main_menu = MainMenu()

    def start_game(self) -> None:
        self.sound.play_pluck()
        self.sound.stop_menu()
        self.sound.play_in_game()
        self.toggle_cursor()

    def deal_initial_hands(self) -> None:
        self.sound.play_game_start()

        self.match.dealer_hand = []
        self.match.player_hand = []

        self.match.deal_card(dealer=True)
        self.match.deal_card(dealer=True)

        self.match.deal_card()
        self.match.deal_card()

        self.match.print_hands(self.username)

    def hit_or_stand(self) -> None:
        print("\n" + self.TEXT_COLOR + "[H]: HIT [S]: STAND")

        while True:
            event = keyboard.read_event(suppress=True)

            if event.event_type == "down":
                if event.name == "h":
                    self.sound.play_pluck()
                    self.match.deal_card()
                    self.match.print_hands(self.username)

                    player_points = self.points_calculator.calculate_points(
                        self.match.player_hand
                    )

                    if player_points > 21:
                        self.sound.play_game_over()
                        self.match.print_hands(self.username, hide_dealer_card=False)
                        print("\n" + self.TEXT_COLOR + "BUST")
                        break
                    else:
                        print("\n" + self.TEXT_COLOR + "[H]: HIT [S]: STAND")
                        continue
                elif event.name == "s":
                    player_points = self.points_calculator.calculate_points(
                        self.match.player_hand
                    )
                    dealer_points = self.points_calculator.calculate_points(
                        self.match.dealer_hand
                    )

                    self.match.print_hands(self.username, hide_dealer_card=False)

                    if dealer_points > 21:
                        print("\n" + self.TEXT_COLOR + "DEALER BUST")
                        print(self.TEXT_COLOR + "YOU WIN!" + "\n")
                        break
                    elif player_points > dealer_points:
                        print("\n" + self.TEXT_COLOR + "YOU HAVE MORE POINTS")
                        print(self.TEXT_COLOR + "YOU WIN!" + "\n")
                        break
                    elif player_points < dealer_points:
                        self.sound.play_game_over()
                        print("\n" + self.TEXT_COLOR + "YOU HAVE LESS POINTS")
                        print(self.TEXT_COLOR + "YOU LOSE" + "\n")
                        break
                    elif player_points == dealer_points:
                        print("\n" + self.TEXT_COLOR + "ITS A TIE" + "\n")
                        break
                else:
                    continue

    def game_over(self) -> None:
        print(self.TEXT_COLOR + "[ENTER]: PLAY AGAIN [ESC]: QUIT")

        while True:
            event = keyboard.read_event(suppress=True)

            if event.event_type == "down":
                if event.name == "enter":
                    self.sound.play_pluck()
                    break
                elif event.name == "esc":
                    self.sound.stop_in_game()
                    self.clear_term()
                    self.sound.play_close_game()
                    print(_Utils.TEXT_COLOR + "GOODBYE" + Fore.WHITE)
                    time.sleep(1)
                    self.clear_term()
                    self.toggle_cursor()
                    sys.exit(1)

    def run(self) -> None:
        self.main_menu.title_screen()
        self.main_menu.prompt_for_username()
        self.start_game()

        while self.play_again:
            self.deck = Deck()
            self.match = Match(self.deck)

            self.deal_initial_hands()
            self.hit_or_stand()
            self.game_over()


if __name__ == "__main__":
    blackjack = BlackjackGameManager()
    blackjack.run()
