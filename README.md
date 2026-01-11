# Higher / Lower Card Game

## Overview
This project is a Higher/Lower card game written in Python, with both Command Line (CLI) and Graphical User Interface (GUI) versions.

Players are shown a card and must guess whether the next card will be higher or lower. The game tracks score, streaks, accuracy, and deck status throughout play. The focus of this project is clean code, solid object-oriented design, and a clear, intuitive user experience.

---

## Features

### Core Functionality
- Standard 52-card deck using Suit and Rank enums
- Fisher–Yates shuffle algorithm
- Higher / Lower game logic with scoring
- Fully functional CLI version

### Extensions
- Optional Joker support (2 Jokers with highest value)
- GUI version built using `tkinter`
- Live statistics tracking:
  - Score
  - Current streak
  - Best streak
  - Accuracy percentage
  - Cards remaining

---

## Design & Implementation

- **Object-Oriented Structure**
  - `Card`: represents individual cards
  - `Deck`: manages shuffling and drawing
  - `HigherLowerGame`: game logic and state
  - `CardGameGUI`: GUI handling  
  This separation improves readability, testability, and extensibility.

- **Enums & Dataclasses**
  - Enums prevent invalid card creation and improve clarity
  - `@dataclass` reduces boilerplate in the `Card` class

- **Shuffle Algorithm**
  - Fisher–Yates implemented manually to demonstrate algorithmic understanding and O(n) efficiency

- **Game Rules**
  - Ties count as incorrect guesses
  - Jokers have the highest value
  - Deck automatically reshuffles when cards run low
## Requirements
- Python 3.7 or later
- `tkinter` (included with most Python installations)
- No external dependencies

---

## GUI Highlights
- Visual card display with red and black suits
- Buttons disabled during card reveal to prevent misclicks
- Clear visual feedback for correct and incorrect guesses
- Live statistics panel
- Simple New Game restart option

---

## Testing
Formal unit tests are not included to keep the submission focused, but the design supports straightforward testing.

Example test cases include:
- Verifying deck size with and without Jokers
- Ensuring shuffle preserves card count
- Testing card value comparisons, including Jokers

---

## Future Improvements
- Animations and sound effects
- Difficulty levels and adaptive gameplay
- Persistent high scores
- Multiplayer support
- Additional card games (e.g. Blackjack, Poker)
- Achievements and GUI customisation

---

## Summary
This project:
- Fully meets all core requirements and includes meaningful extensions
- Provides both CLI and GUI interfaces
- Demonstrates clean, maintainable, and well-documented code
- Shows thoughtful UX and game design
- Is structured for future expansion rather than a one-off solution

---

## How to Run
### CLI
python card_game.py


