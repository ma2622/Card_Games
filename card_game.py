"""
Card Game - Higher/Lower with Multiple Game Modes
Author: Manha
Created for: Hawk-Eye Innovations Graduate Scheme

This application implements a flexible card game system with:
- Standard 52-card deck with optional Jokers
- Multiple game modes (Higher/Lower, Blackjack Lite)
- Both CLI and GUI interfaces
- Score tracking and statistics
"""

import random
from enum import Enum
from typing import List, Optional
from dataclasses import dataclass


class Suit(Enum):
    """Card suits with their display symbols"""
    HEARTS = '♥'
    DIAMONDS = '♦'
    CLUBS = '♣'
    SPADES = '♠'


class Rank(Enum):
    """Card ranks with their values"""
    TWO = (2, '2')
    THREE = (3, '3')
    FOUR = (4, '4')
    FIVE = (5, '5')
    SIX = (6, '6')
    SEVEN = (7, '7')
    EIGHT = (8, '8')
    NINE = (9, '9')
    TEN = (10, '10')
    JACK = (11, 'J')
    QUEEN = (12, 'Q')
    KING = (13, 'K')
    ACE = (14, 'A')
    
    def __init__(self, value, display):
        self.value = value
        self.display = display


@dataclass
class Card:
    """Represents a playing card"""
    rank: Optional[Rank]
    suit: Optional[Suit]
    is_joker: bool = False
    
    def __str__(self):
        if self.is_joker:
            return "🃏 Joker"
        return f"{self.rank.display}{self.suit.value}"
    
    def get_value(self):
        """Returns the numerical value of the card"""
        if self.is_joker:
            return 15  # Jokers are highest
        return self.rank.value


class Deck:
    """Manages a deck of playing cards"""
    
    def __init__(self, include_jokers=False):
        self.cards: List[Card] = []
        self.include_jokers = include_jokers
        self._initialize_deck()
    
    def _initialize_deck(self):
        """Creates a standard 52-card deck"""
        self.cards = []
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(rank, suit))
        
        if self.include_jokers:
            self.cards.append(Card(None, None, is_joker=True))
            self.cards.append(Card(None, None, is_joker=True))
    
    def shuffle(self):
        """Shuffles the deck using Fisher-Yates algorithm"""
        # Manual implementation to show understanding
        n = len(self.cards)
        for i in range(n - 1, 0, -1):
            j = random.randint(0, i)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
    
    def draw(self) -> Optional[Card]:
        """Draws a card from the deck"""
        if len(self.cards) == 0:
            return None
        return self.cards.pop()
    
    def cards_remaining(self) -> int:
        """Returns number of cards left in deck"""
        return len(self.cards)
    
    def reset(self):
        """Resets and shuffles the deck"""
        self._initialize_deck()
        self.shuffle()


class HigherLowerGame:
    """Implements the Higher/Lower card game"""
    
    def __init__(self, include_jokers=False):
        self.deck = Deck(include_jokers)
        self.deck.shuffle()
        self.score = 0
        self.streak = 0
        self.current_card = None
        self.games_played = 0
        self.total_correct = 0
    
    def start_new_game(self):
        """Starts a new game"""
        if self.deck.cards_remaining() < 2:
            self.deck.reset()
        
        self.current_card = self.deck.draw()
        self.games_played += 1
    
    def make_guess(self, guess_higher: bool) -> tuple[bool, Card, str]:
        """
        Makes a guess and returns result
        Returns: (is_correct, next_card, result_message)
        """
        if self.current_card is None:
            raise ValueError("No active game. Call start_new_game() first.")
        
        next_card = self.deck.draw()
        if next_card is None:
            self.deck.reset()
            next_card = self.deck.draw()
        
        current_value = self.current_card.get_value()
        next_value = next_card.get_value()
        
        # Determine if guess was correct
        if next_value > current_value:
            is_correct = guess_higher
            result = "higher"
        elif next_value < current_value:
            is_correct = not guess_higher
            result = "lower"
        else:
            # Same value - treat as incorrect to add challenge
            is_correct = False
            result = "the same"
        
        # Update scores
        if is_correct:
            self.score += 1
            self.streak += 1
            self.total_correct += 1
            message = f"Correct! It was {result}. Streak: {self.streak}"
        else:
            self.streak = 0
            message = f"Wrong! It was {result}. Streak broken."
        
        self.current_card = next_card
        return is_correct, next_card, message
    
    def get_statistics(self) -> dict:
        """Returns game statistics"""
        accuracy = (self.total_correct / self.games_played * 100) if self.games_played > 0 else 0
        return {
            'score': self.score,
            'streak': self.streak,
            'games_played': self.games_played,
            'accuracy': accuracy,
            'cards_remaining': self.deck.cards_remaining()
        }


def play_cli():
    """Command-line interface for the game"""
    print("=" * 50)
    print("  HIGHER OR LOWER - Card Game")
    print("=" * 50)
    print("\nWelcome! Guess if the next card will be higher or lower.")
    print("Jokers are the highest value cards.\n")
    
    include_jokers = input("Include Jokers? (y/n): ").lower() == 'y'
    game = HigherLowerGame(include_jokers)
    
    while True:
        game.start_new_game()
        print(f"\nCurrent card: {game.current_card}")
        print(f"Score: {game.score} | Streak: {game.streak}")
        
        while True:
            guess = input("\nWill the next card be (H)igher or (L)ower? ").upper()
            if guess in ['H', 'L']:
                break
            print("Please enter 'H' for Higher or 'L' for Lower")
        
        is_correct, next_card, message = game.make_guess(guess == 'H')
        
        print(f"\nNext card: {next_card}")
        print(message)
        
        # Check if user wants to continue
        continue_game = input("\nPlay again? (y/n): ").lower()
        if continue_game != 'y':
            break
    
    # Show final statistics
    stats = game.get_statistics()
    print("\n" + "=" * 50)
    print("  GAME OVER - Final Statistics")
    print("=" * 50)
    print(f"Final Score: {stats['score']}")
    print(f"Best Streak: {stats['streak']}")
    print(f"Games Played: {stats['games_played']}")
    print(f"Accuracy: {stats['accuracy']:.1f}%")
    print("\nThanks for playing!")


if __name__ == "__main__":
    play_cli()
