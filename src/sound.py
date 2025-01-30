"""Sound manager module."""

from pygame import mixer


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
