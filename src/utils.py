"""Utility module."""

import os
from typing import LiteralString

from colorama import Fore  # type: ignore
import cursor  # type: ignore


class Utils:
    """Utility attributes and methods."""

    TEXT_PADDING: int = 80
    TEXT_COLOR: str = Fore.LIGHTRED_EX
    CARD_COLOR: str = Fore.WHITE
    TITLE: LiteralString = """
88          88                       88        88                       88
88          88                       88        ""                       88         
88          88                       88                                 88         
88,dPPYba,  88 ,adPPYYba,  ,adPPYba, 88   ,d8  88 ,adPPYYba,  ,adPPYba, 88   ,d8   
88P'    "8a 88 ""     `Y8 a8"     "" 88 ,a8"   88 ""     `Y8 a8"     "" 88 ,a8"    
88       d8 88 ,adPPPPP88 8b         8888[     88 ,adPPPPP88 8b         8888[      
88b,   ,a8" 88 88,    ,88 "8a,   ,aa 88`"Yba,  88 88,    ,88 "8a,   ,aa 88`"Yba,   
8Y"Ybbd8"'  88 `"8bbdP"Y8  `"Ybbd8"' 88   `Y8a 88 `"8bbdP"Y8  `"Ybbd8"' 88   `Y8a  
                                            ,88                                  
                                        888P\"""".center(TEXT_PADDING)
    START_GAME_PROMPT: LiteralString = "PRESS [ENTER] TO PLAY...".center(TEXT_PADDING)

    username: str = ""
    cursor_off = False

    def __repr__(self) -> str:
        return f"Utils(TEXT_PADDING={self.TEXT_PADDING}, )"

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
