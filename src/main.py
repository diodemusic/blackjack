"""Simple python blackjack game! :)"""

import random
import os
import time
import sys

import cursor  # type: ignore
from pygame import mixer  # This is only for playing audio
from colorama import Fore  # type: ignore
import keyboard  # type: ignore


class _Utils:
    """Utility attributes and methods for internal use."""

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
        """Toggles on and off the terminal cursor."""

        if not self.cursor_off:
            cursor.hide()
            self.cursor_off = True
            return
        cursor.show()
        self.cursor_off = False

    def clear_term(self) -> None:
        """Clear all text from the terminal."""

        os.system("cls" if os.name == "nt" else "clear")


class SoundManager:
    """Load and play audio files."""

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
        """Plays the menu music audio file: menu.mp3"""

        self.menu.play(loops=-1)

    def stop_menu(self) -> None:
        """Stops the menu music audio file: menu.mp3"""

        self.menu.stop()

    def play_game_start(self) -> None:
        """Plays the game start audio file: game_start.mp3"""

        self.game_start.play()

    def play_in_game(self) -> None:
        """Plays the in game music audio file: in_game.mp3"""

        self.in_game.play(loops=-1)

    def stop_in_game(self) -> None:
        """Stops the in game music audio file: in_game.mp3"""

        self.in_game.stop()

    def play_pluck(self) -> None:
        """Plays the pluck audio file: pluck.mp3"""

        self.pluck.play()

    def play_game_over(self) -> None:
        """Plays the game over audio file: game_over.mp3"""

        self.game_over.play()

    def play_close_game(self) -> None:
        """Plays the close game audio file: close_game.mp3"""

        self.close_game.play()


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


class Match(_Utils):
    """
    Contains the game logic for dealing cards and printing them.

    Args:
        _Utils (class): Inherits the _Utils class.
    """

    def __init__(self, deck: list[Card]) -> None:
        self.deck = deck
        self.dealer_hand: list[Card] = []
        self.player_hand: list[Card] = []
        self.card_spacing = 0

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

        card = self.deck.pop(random.randrange(start=0, stop=len(self.deck)))

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

        ascii_card = Card.get_ascii_card(card, hidden)

        for line in ascii_card.splitlines():
            print(_Utils.CARD_COLOR + " " * self.card_spacing, line)

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
    """Class to calculate the dealers or players hand."""

    def __init__(self) -> None:
        self.points: int = 0

    def __repr__(self) -> str:
        return f"PointsCalculator(points={self.points})"

    def count_non_aces(self, hand: list[Card]) -> int:
        """
        Count the points of all Card instances.

        Args:
            hand (list[Card]): List of Card objects.

        Returns:
            int: Total worth of the Card objects in points.
        """

        for card in hand:
            if card.name != "ace":
                self.points += card.points

        return self.points

    def count_aces(self, hand: list[Card]) -> int:
        """
        Count all Card instances that are aces.

        Args:
            hand (list[Card]): List of Card objects.

        Returns:
            int: Total worth of the Card objects in points.
        """

        for card in hand:
            if card.name == "ace" and self.points >= 11:
                self.points += 1
            elif card.name == "ace":
                self.points += 11

        return self.points

    def calculate_points(self, hand: list[Card]) -> int:
        """
        Calculate total points of Card objects.

        Args:
            hand (list[Card]): List of Card objects.

        Returns:
            int: Total worth of the Card objects in points.
        """

        self.points = 0
        self.points = self.count_non_aces(hand)
        self.points = self.count_aces(hand)

        return self.points


class MainMenu(_Utils, SoundManager):
    """
    Main menu UI class.

    Args:
        _Utils (class): Inherits the _Utils class.
        SoundManager (class): Inherits the SoundManager class.
    """

    def title_screen(self) -> None:
        """Clear the terminal and print the main title screen."""

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
                continue

    def prompt_for_username(self) -> None:
        """Clear the terminal and ask the user for a username."""

        self.clear_term()
        self.toggle_cursor()

        self.username = input(
            "ENTER USERNAME: ".rjust(self.TEXT_PADDING // 2 + 4)
        ).upper()
        self.play_pluck()
        self.toggle_cursor()


class BlackjackGameManager(_Utils):
    """
    Main game logic class.

    Args:
        _Utils (class): Inherits the _Utils class.
    """

    play_again = True

    points_calculator = PointsCalculator()
    sound = SoundManager()
    main_menu = MainMenu()

    def __init__(self) -> None:
        self.match: Match

    def start_match(self) -> None:
        """Initialise a match."""

        self.sound.play_pluck()
        self.sound.stop_menu()
        self.sound.play_in_game()
        self.toggle_cursor()

    def deal_initial_hands(self) -> None:
        """Deal the initial hands to the dealer and player."""

        self.sound.play_game_start()

        self.match.dealer_hand = []
        self.match.player_hand = []

        self.match.deal_card(dealer=True)
        self.match.deal_card(dealer=True)

        self.match.deal_card()
        self.match.deal_card()

        self.match.print_hands(self.username)

    def hit(self) -> bool:
        """
        Handles the logic for hitting.

        Returns:
            bool: Wether or not the player busted.
        """

        self.sound.play_pluck()
        self.match.deal_card()
        self.match.print_hands(self.username)

        player_points = self.points_calculator.calculate_points(self.match.player_hand)

        if player_points > 21:
            self.sound.play_game_over()
            self.match.print_hands(self.username, hide_dealer_card=False)
            print("\n" + self.TEXT_COLOR + "BUST")
            return True
        print("\n" + self.TEXT_COLOR + "[H]: HIT [S]: STAND")
        return False

    def stand(self) -> bool:
        """
        Handles the logic for standing.

        Returns:
            bool: Wether or not the game ended.
        """

        player_points = self.points_calculator.calculate_points(self.match.player_hand)
        dealer_points = self.points_calculator.calculate_points(self.match.dealer_hand)

        self.match.print_hands(self.username, hide_dealer_card=False)
        print(player_points)

        if dealer_points > 21:
            print("\n" + self.TEXT_COLOR + "DEALER BUST")
            print(self.TEXT_COLOR + "YOU WIN!" + "\n")
            return True
        elif player_points > dealer_points:
            print("\n" + self.TEXT_COLOR + "YOU HAVE MORE POINTS")
            print(self.TEXT_COLOR + "YOU WIN!" + "\n")
            return True
        elif player_points < dealer_points:
            self.sound.play_game_over()
            print("\n" + self.TEXT_COLOR + "YOU HAVE LESS POINTS")
            print(self.TEXT_COLOR + "YOU LOSE" + "\n")
            return True
        elif player_points == dealer_points:
            print("\n" + self.TEXT_COLOR + "ITS A TIE" + "\n")
            return True
        else:
            return False

    def hit_or_stand(self) -> None:
        """Handles game logic for hit or stand."""

        print("\n" + self.TEXT_COLOR + "[H]: HIT [S]: STAND")

        while True:
            event = keyboard.read_event(suppress=True)

            if event.event_type != "down":
                continue

            if event.name == "h" and self.hit():
                break
            if event.name == "s" and self.stand():
                break

    def game_over(self) -> None:
        """Prompts the user asking if they want to play again or close the program."""

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
        """Main loop."""

        self.main_menu.title_screen()
        self.main_menu.prompt_for_username()
        self.start_match()

        while self.play_again:
            deck_object = Deck()
            deck = deck_object.create_deck()
            self.match = Match(deck)

            self.deal_initial_hands()
            self.hit_or_stand()
            self.game_over()


if __name__ == "__main__":
    blackjack = BlackjackGameManager()
    blackjack.run()
