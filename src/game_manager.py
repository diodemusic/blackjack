"""Game manager module, this module contains the main game logic."""

import sys
import time

from colorama import Fore  # type: ignore
import keyboard  # type: ignore

from utils import Utils
from calculator import PointsCalculator
from deck import Card, Deck
from match import Match
from menu import MainMenu
from sound import SoundManager


class BlackjackGameManager(Utils):
    """
    Main game logic class.

    Args:
        Utils (class): Inherits the Utils class.
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

        self.match.print_hands(self.main_menu.username)

    def hit(self) -> bool:
        """
        Handles the logic for hitting.

        Returns:
            bool: Wether or not the player busted.
        """

        self.sound.play_pluck()
        self.match.deal_card()
        self.match.print_hands(self.main_menu.username)

        player_points: int = self.points_calculator.calculate_points(
            self.match.player_hand
        )

        if player_points > 21:
            self.sound.play_game_over()
            self.match.print_hands(self.main_menu.username, hide_dealer_card=False)
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

        player_points: int = self.points_calculator.calculate_points(
            self.match.player_hand
        )
        dealer_points: int = self.points_calculator.calculate_points(
            self.match.dealer_hand
        )

        self.match.print_hands(self.main_menu.username, hide_dealer_card=False)

        if dealer_points > 21:
            print("\n" + self.TEXT_COLOR + "DEALER BUST")
            print(self.TEXT_COLOR + "YOU WIN!" + "\n")
            return True

        if player_points > dealer_points:
            print("\n" + self.TEXT_COLOR + "YOU HAVE MORE POINTS")
            print(self.TEXT_COLOR + "YOU WIN!" + "\n")
            return True

        if player_points < dealer_points:
            self.sound.play_game_over()
            print("\n" + self.TEXT_COLOR + "YOU HAVE LESS POINTS")
            print(self.TEXT_COLOR + "YOU LOSE" + "\n")
            return True

        if player_points == dealer_points:
            print("\n" + self.TEXT_COLOR + "ITS A TIE" + "\n")
            return True
        return False

    def hit_or_stand(self) -> None:
        """Handles game logic for hit or stand."""

        print("\n" + self.TEXT_COLOR + "[H]: HIT [S]: STAND")

        while True:
            event: keyboard.KeyboardEvent = keyboard.read_event(suppress=True)

            if event.event_type != "down":
                continue

            if event.name == "h" and self.hit():
                break

            if event.name == "s" and self.stand():
                break

    def exit_game(self) -> None:
        """Exits the program."""

        self.sound.stop_in_game()
        self.clear_term()
        self.sound.play_close_game()
        print(Utils.TEXT_COLOR + "GOODBYE" + Fore.WHITE)
        time.sleep(1)
        self.clear_term()
        self.toggle_cursor()
        sys.exit(1)

    def game_over_prompt(self) -> None:
        """Prompts the user asking if they want to play again or close the program."""

        print(self.TEXT_COLOR + "[ENTER]: PLAY AGAIN [ESC]: QUIT")

        while True:
            event: keyboard.KeyboardEvent = keyboard.read_event(suppress=True)

            if event.event_type == "down":
                if event.name == "enter":
                    self.sound.play_pluck()
                    break

                if event.name == "esc":
                    self.exit_game()

    def run(self) -> None:
        """Main loop."""

        self.main_menu.title_screen()
        self.main_menu.prompt_for_username()
        self.start_match()

        while self.play_again:
            deck_object = Deck()
            deck: list[Card] = deck_object.create_deck()
            self.match = Match(deck)

            self.deal_initial_hands()
            self.hit_or_stand()
            self.game_over_prompt()
