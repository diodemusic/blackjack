"""Sound manager module."""

from dataclasses import dataclass
import os

from pygame import mixer  # This is only used to play audio.


def get_path(file_name: str) -> str:
    """
    Resolve the path from a relative directory.

    Args:
        file_name (str): Audio file name.

    Returns:
        str: Returns full relative path for the audio file.
    """
    path = os.path.join("..", "audio", file_name)

    return path


@dataclass
class PathManager:
    """Manages relative paths for the audio files."""

    def __init__(self) -> None:
        self.menu_path = get_path("menu.mp3")
        self.pluck_path = get_path("pluck.mp3")
        self.game_start_path = get_path("game_start.mp3")
        self.in_game_path = get_path("in_game.mp3")
        self.game_over_path = get_path("game_over.mp3")
        self.close_game_path = get_path("close_game.mp3")


class SoundManager(PathManager):
    """Load and play audio files."""

    mixer.init()

    def __init__(self) -> None:
        super().__init__()

        self.menu = mixer.Sound(self.menu_path)
        self.pluck = mixer.Sound(self.pluck_path)
        self.game_start = mixer.Sound(self.game_start_path)
        self.in_game = mixer.Sound(self.in_game_path)
        self.game_over = mixer.Sound(self.game_over_path)
        self.close_game = mixer.Sound(self.close_game_path)

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
