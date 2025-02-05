"""Game manager module, this module contains the main game logic."""

import sys
import time

from colorama import Fore  # type: ignore
import keyboard  # type: ignore

from chips_manager import Chips
from deck_manager import Card, Deck
from match_manager import Match
from menu_manager import MainMenu
from points_manager import PointsCalculator
from sound_manager import SoundManager
from theme_manager import Theme
from utils_manager import Utils
from match_history_manager import MatchHistory


class BlackjackGameManager:
    """
    Main game logic class.

    Args:
        Utils (class): Inherits the Utils class.
    """

    play_again = True
    bet: int = 0

    def __init__(self) -> None:
        self.chips = Chips()
        self.match_history = MatchHistory()
        self.menu = MainMenu()
        self.points = PointsCalculator()
        self.sound = SoundManager()
        self.theme = Theme()
        self.utils = Utils()

        self.match: Match

    def start_match(self) -> None:
        """Initialise a match."""

        self.sound.play_pluck()
        self.sound.play_in_game()
        self.utils.toggle_cursor()

    def deal_initial_hands(self) -> None:
        """Deal the initial hands to the dealer and player."""

        self.sound.play_game_start()

        self.match.dealer_hand = []
        self.match.player_hand = []

        self.match.deal_card(dealer=True)
        self.match.deal_card(dealer=True)

        self.match.deal_card()
        self.match.deal_card()

        self.match.print_hands(self.menu.username)

    def win(self) -> bool:
        """Logic for winning."""

        self.sound.play_game_over()

        print(self.theme.text_color + "YOU WIN!" + "\n")
        self.chips.add_or_remove_chips(self.menu.username, self.bet)

        self.match_history.add_win(self.menu.username)

        return True

    def lose(self) -> bool:
        """Logic for losing."""

        self.sound.play_game_over()

        print(self.theme.text_color + "YOU LOSE" + "\n")
        self.chips.add_or_remove_chips(self.menu.username, -self.bet)

        self.match_history.add_loss(self.menu.username)

        return True

    def hit(self) -> bool:
        """
        Handles the logic for hitting.

        Returns:
            bool: Wether or not the player busted.
        """

        self.sound.play_pluck()
        self.match.deal_card()
        self.match.print_hands(self.menu.username)

        player_points: int = self.points.calculate_points(self.match.player_hand)

        if player_points > 21:
            self.match.print_hands(self.menu.username, hide_dealer_card=False)
            print("\n" + self.theme.text_color + "BUST")

            return self.lose()

        print("\n" + self.theme.text_color + "[H]: HIT [S]: STAND")
        return False

    def stand(self) -> bool:
        """
        Handles the logic for standing.

        Returns:
            bool: Wether or not the game ended.
        """

        player_points: int = self.points.calculate_points(self.match.player_hand)
        dealer_points: int = self.points.calculate_points(self.match.dealer_hand)

        self.match.print_hands(self.menu.username, hide_dealer_card=False)

        if dealer_points > 21:
            print("\n" + self.theme.text_color + "DEALER BUST")

            return self.win()

        if player_points > dealer_points:
            print("\n" + self.theme.text_color + "YOU HAVE MORE POINTS")

            return self.win()

        if player_points < dealer_points:
            print("\n" + self.theme.text_color + "YOU HAVE LESS POINTS")

            return self.lose()

        if player_points == dealer_points:
            print("\n" + self.theme.text_color + "ITS A TIE" + "\n")

            self.match_history.add_game_played(self.menu.username)

            return True

        return False

    def hit_or_stand(self) -> None:
        """Handles game logic for hit or stand."""

        print("\n" + self.theme.text_color + "[H]: HIT [S]: STAND")

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
        self.utils.clear_term()
        self.sound.play_close_game()
        print(self.theme.text_color + "GOODBYE" + Fore.WHITE)
        time.sleep(1)
        self.utils.clear_term()
        self.utils.toggle_cursor()
        sys.exit(1)

    def game_over_prompt(self) -> None:
        """Prompts the user asking if they want to play again or close the program."""

        print(self.theme.text_color + "[ENTER]: PLAY AGAIN [ESC]: QUIT")

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

        self.menu.title_screen()
        self.menu.prompt_for_username()
        self.menu.prompt_for_new_theme()
        self.start_match()

        while self.play_again:
            deck_object = Deck()
            deck: list[Card] = deck_object.create_deck()
            self.match = Match(deck)

            self.bet: int = self.menu.prompt_for_bet()
            self.deal_initial_hands()
            self.hit_or_stand()
            self.match_history.update_winrate(self.menu.username)
            self.game_over_prompt()
