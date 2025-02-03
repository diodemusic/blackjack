# TODO List

## To Do

- [ ] Check for player blackjack
- [ ] A player blackjack wins immediately unless the dealer also has one, in which case the hand is a push. If the dealer is dealt blackjack, all players who do not have a blackjack lose.
- [ ] If your points total 21 (blackjack) you auto win 1.5x your bet and the game is over
- [ ] Once the dealer has gone around the table once flip up the face down card
- [ ] If the dealer has < 17 points total, the dealer hits, if >= 17, stand
- [ ] If the dealer busts, win 2x your bet and the game is over
- [ ] Change key listen input if statements to single if statements that use dictionaries
- [ ] Change the new game sound to something shorter and quieter
- [ ] Add more sounds; bust, win
- [ ] Move print hands to _Utils class
- [ ] Draw cards horizontally
- [ ] Dont allow blank username
- [ ] Add __repr__() to all classes and add single quotes to strings
- [ ] Set charcter limit on username
- [ ] Only allow A-Z a-z chars
- [ ] ENTER -> new game/load an existing save -> enter username if new game -> play
- [ ] Add a feature to save and load game state
- [ ] Add Q: Save and quit
- [ ] Implement unit tests for all classes and methods
- [ ] Add logging for debugging and tracking game progress
- [ ] Add animations for dealing cards (if GUI is implemented)
- [ ] Implement a feature to track player statistics across games
- [ ] Add a leaderboard based on most chips/games played/most wins
- [ ] Add wins losses winrate games played and chips to the load save screen
- [ ] Add a rules page accesible from the main menu

## In Progress

- [ ] Implement a method to display your current chips
- [ ] Show dealers hand on player bust
- [ ] Add a theme switcher
- [ ] Store themes on a per user basis

## Done

- [x] Store wins, losse,s winrate, and games played in database
- [x] If a user has 0 chips, give them 1000
- [x] Ensure bet is an integer
- [x] Do not allow chips to go under 0
- [x] Check that a user has enough chips for their bet
- [x] Show current balance on bet screen
- [x] Fix users database directory creation
- [x] Implement betting system
- [x] Display chip amount after a win or loss
- [x] Store users chips in user database entrys
- [x] Store usernames in database
- [x] Create database for users
- [x] Fix menu sound not stopping
- [x] Modularize codebase
- [x] Add type hints to all vars
- [x] Add type hints and return values to all methods
- [x] Write docstrings for all classes and methods and generate docs from them
- [x] Move main menu logic to Menu class
- [x] Do not allow user to type on title screen
- [x] Fix deck not resetting after game
- [x] Ensure the deck and dealer object attributes are reset on new match
- [x] Toggle cursor off except when capturing user input with input()
- [x] Handle having 2 aces and rewrite player ace prompt
- [x] Count aces as 1 or 11 dynamically
- [x] Add key up functionality to user input so prompts dont get spammed by pressing any key
- [x] Add stand functionality
- [x] make user input just pressing keys instead of using commands, then write something like h: hit s: stand
- [x] Fix user being prompted for the dealers ace(s)
- [x] Move main logic to the `BlackjackGameManager` class
- [x] Replace hardcoded username with user input
- [x] Create a graphical user interface (GUI)
