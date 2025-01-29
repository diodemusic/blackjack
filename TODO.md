# TODO List

## To Do

- [ ] Do not allow user to type on title screen
- [ ] Show dealers hand on player bust
- [ ] If your points total 21 (blackjack) you auto win 1.5x your bet and the game is over
- [ ] Once the dealer has gone around the table once flip up the face down card
- [ ] If the dealer has < 17 points total, the dealer hits, if >= 17, stand
- [ ] If the dealer busts, win 2x your bet and the game is over
- [ ] Change key listen input if statements to single if statements that use dictionaries
- [ ] Add a theme switcher
- [ ] Change the new game sound to something shorter and quieter
- [ ] Add __repr__() to classes
- [ ] ctrl+f "=" and add type hints to all vars
- [ ] ctrl+f ")" and add type hints adn return hints to all methods
- [ ] Write docstrings and generate docs from them
- [ ] Move print hands to _Utils class
- [ ] Draw cards horizontally
- [ ] Dont allow blank username
- [ ] Set charcter limit on username
- [ ] Only allow A-Z a-z chars
- [ ] ENTER -> new game/load an existing save -> enter username if new game -> play
- [ ] Implement betting system
- [ ] Implement a method to display your current chips
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

- [ ] Add end game screen music after a bust
- [ ] Add more sounds; bust, win

## Done

- [x] Fix deck not resetting after game
- [x] Ensure the dealer object attributes are reset on new match
- [x] Toggle cursor off except when capturing user input with input()
- [x] Handle having 2 aces and rewrite player ace prompt
- [x] Count aces as 1 or 11 dynamically
- [x] Add key up functionality to user input so prompts dont get spammed by pressing any key
- [x] Add stand functionality
- [x] make user input just pressing keys instead of using commands, then write something like h: hit s: stand
- [x] Fix user being prompted for the dealers ace(s)
- [x] Move main logic to the `Match` class
- [x] Replace hardcoded username with user input
- [x] Create a graphical user interface (GUI)
