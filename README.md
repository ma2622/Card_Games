Author: Manha

Overview

This project is a Higher/Lower card game built in Python, available in both Command Line (CLI) and Graphical (GUI) versions.

The aim of the game is simple:
You’re shown a card and must guess whether the next card will be higher or lower.
The game keeps track of your score, streaks, and accuracy as you play.

I’ve focused on writing clean, readable code and building something that’s fun, extensible, and easy to understand.

What’s Included
Core Features

Standard 52-card deck (using Suits and Ranks)

Proper shuffle algorithm (Fisher–Yates)

Higher / Lower game logic with scoring

Fully working CLI version

Extra Features

Optional Jokers (2 cards, highest value)

GUI version built with tkinter

Live statistics tracking:

Score

Current streak

Best streak

Accuracy %

Cards remaining

Design Choices (Briefly Explained)
Object-Oriented Design

The code is split into clear, logical parts:

Card – represents a single card

Deck – handles shuffling and drawing cards

HigherLowerGame – contains game rules and state

CardGameGUI – manages the graphical interface

This makes the code easy to read, test, and extend.

Why Enums and Dataclasses?

Enums prevent invalid cards and improve clarity

@dataclass reduces boilerplate and keeps the Card class clean

Shuffle Algorithm

I implemented Fisher–Yates manually instead of using random.shuffle() to show:

Understanding of algorithms

Ability to write efficient O(n) solutions

Game Rules

Ties count as incorrect to keep the game challenging

Jokers have the highest value to make them special

The deck automatically reshuffles when cards run low

How to Run
CLI Version
python card_game.py

GUI Version
python card_game_gui.py

Requirements

Python 3.7+

tkinter (usually included with Python)

No external libraries

GUI Highlights

Visual card display with red/black suits

Buttons disabled during card reveal (prevents misclicks)

Clear colour feedback:

Green = correct

Red = incorrect

Live stats panel

Easy “New Game” restart option

🧪 Testing

Formal unit tests aren’t included to keep the submission focused, but the design makes testing straightforward.

Example tests I would add:

Deck size with and without Jokers

Shuffle preserving card count

Card value comparisons (including Jokers)

Possible Improvements
Short-Term

Card reveal animations

Sound effects

Difficulty levels

Persistent high scores (saved to file)

Long-Term

Multiplayer support

Additional card games (e.g. Blackjack, Poker)

Achievements and progression system

GUI themes and customisation

Why This Stands Out

Fully meets all requirements, plus extensions

Two complete interfaces (CLI + GUI)

Clean, readable, well-documented code

Thoughtful UX and gameplay decisions

Designed to be extended, not just “finished”

Final Note

This project reflects how I approach development:

Clear structure

Readable, maintainable code

Thoughtful design decisions

Focus on user experience

Thank you for taking the time to review my submission — I’d love the opportunity to bring this approach to Hawk-Eye Innovations.
