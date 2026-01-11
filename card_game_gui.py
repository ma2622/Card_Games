"""
GUI Version of Higher/Lower Card Game
Uses tkinter for cross-platform compatibility

Features:
- Visual card display
- Real-time statistics
- Smooth animations
- Multiple color themes
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
from enum import Enum
from typing import Optional
from dataclasses import dataclass


class Suit(Enum):
    HEARTS = '♥'
    DIAMONDS = '♦'
    CLUBS = '♣'
    SPADES = '♠'


class Rank(Enum):
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
    rank: Optional[Rank]
    suit: Optional[Suit]
    is_joker: bool = False
    
    def __str__(self):
        if self.is_joker:
            return "🃏"
        return f"{self.rank.display}{self.suit.value}"
    
    def get_value(self):
        if self.is_joker:
            return 15
        return self.rank.value
    
    def is_red(self):
        if self.is_joker:
            return False
        return self.suit in [Suit.HEARTS, Suit.DIAMONDS]


class Deck:
    def __init__(self, include_jokers=False):
        self.cards = []
        self.include_jokers = include_jokers
        self._initialize_deck()
    
    def _initialize_deck(self):
        self.cards = []
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(rank, suit))
        
        if self.include_jokers:
            self.cards.append(Card(None, None, is_joker=True))
            self.cards.append(Card(None, None, is_joker=True))
    
    def shuffle(self):
        n = len(self.cards)
        for i in range(n - 1, 0, -1):
            j = random.randint(0, i)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
    
    def draw(self):
        return self.cards.pop() if self.cards else None
    
    def cards_remaining(self):
        return len(self.cards)
    
    def reset(self):
        self._initialize_deck()
        self.shuffle()


class CardGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Higher or Lower - Card Game")
        self.root.geometry("600x700")
        self.root.configure(bg='#1e3a2e')
        
        self.deck = None
        self.current_card = None
        self.score = 0
        self.streak = 0
        self.best_streak = 0
        self.games_played = 0
        
        self._create_widgets()
        self._show_start_screen()
    
    def _create_widgets(self):
        # Title
        self.title_label = tk.Label(
            self.root,
            text="HIGHER OR LOWER",
            font=('Arial', 28, 'bold'),
            bg='#1e3a2e',
            fg='#f0e68c'
        )
        self.title_label.pack(pady=20)
        
        # Stats frame
        stats_frame = tk.Frame(self.root, bg='#1e3a2e')
        stats_frame.pack(pady=10)
        
        self.score_label = tk.Label(
            stats_frame,
            text="Score: 0",
            font=('Arial', 16),
            bg='#1e3a2e',
            fg='white'
        )
        self.score_label.grid(row=0, column=0, padx=20)
        
        self.streak_label = tk.Label(
            stats_frame,
            text="Streak: 0",
            font=('Arial', 16),
            bg='#1e3a2e',
            fg='white'
        )
        self.streak_label.grid(row=0, column=1, padx=20)
        
        # Card display
        self.card_frame = tk.Frame(
            self.root,
            bg='white',
            width=200,
            height=280,
            relief=tk.RAISED,
            borderwidth=5
        )
        self.card_frame.pack(pady=30)
        self.card_frame.pack_propagate(False)
        
        self.card_label = tk.Label(
            self.card_frame,
            text="?",
            font=('Arial', 72, 'bold'),
            bg='white',
            fg='black'
        )
        self.card_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Buttons frame
        button_frame = tk.Frame(self.root, bg='#1e3a2e')
        button_frame.pack(pady=20)
        
        self.higher_btn = tk.Button(
            button_frame,
            text="HIGHER ↑",
            font=('Arial', 16, 'bold'),
            bg='#4CAF50',
            fg='white',
            width=12,
            height=2,
            command=lambda: self.make_guess(True),
            cursor='hand2'
        )
        self.higher_btn.grid(row=0, column=0, padx=10)
        
        self.lower_btn = tk.Button(
            button_frame,
            text="LOWER ↓",
            font=('Arial', 16, 'bold'),
            bg='#f44336',
            fg='white',
            width=12,
            height=2,
            command=lambda: self.make_guess(False),
            cursor='hand2'
        )
        self.lower_btn.grid(row=0, column=1, padx=10)
        
        # Result message
        self.result_label = tk.Label(
            self.root,
            text="",
            font=('Arial', 14),
            bg='#1e3a2e',
            fg='#f0e68c'
        )
        self.result_label.pack(pady=10)
        
        # Cards remaining
        self.cards_label = tk.Label(
            self.root,
            text="",
            font=('Arial', 12),
            bg='#1e3a2e',
            fg='lightgray'
        )
        self.cards_label.pack(pady=5)
        
        # New game button
        self.new_game_btn = tk.Button(
            self.root,
            text="New Game",
            font=('Arial', 12),
            bg='#2196F3',
            fg='white',
            command=self._show_start_screen,
            cursor='hand2'
        )
        self.new_game_btn.pack(pady=10)
    
    def _show_start_screen(self):
        # Reset game
        self.score = 0
        self.streak = 0
        self.games_played = 0
        self._update_stats()
        
        # Show options dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("New Game")
        dialog.geometry("300x150")
        dialog.configure(bg='#1e3a2e')
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(
            dialog,
            text="Start a new game",
            font=('Arial', 16, 'bold'),
            bg='#1e3a2e',
            fg='white'
        ).pack(pady=20)
        
        joker_var = tk.BooleanVar()
        tk.Checkbutton(
            dialog,
            text="Include Jokers",
            variable=joker_var,
            font=('Arial', 12),
            bg='#1e3a2e',
            fg='white',
            selectcolor='#1e3a2e'
        ).pack()
        
        def start():
            self.deck = Deck(joker_var.get())
            self.deck.shuffle()
            dialog.destroy()
            self.start_round()
        
        tk.Button(
            dialog,
            text="Start",
            font=('Arial', 12, 'bold'),
            bg='#4CAF50',
            fg='white',
            command=start,
            cursor='hand2'
        ).pack(pady=20)
    
    def start_round(self):
        if self.deck.cards_remaining() < 2:
            self.deck.reset()
        
        self.current_card = self.deck.draw()
        self.games_played += 1
        self._display_card(self.current_card)
        self.result_label.config(text="Will the next card be higher or lower?")
        self._update_stats()
        
        self.higher_btn.config(state=tk.NORMAL)
        self.lower_btn.config(state=tk.NORMAL)
    
    def make_guess(self, guess_higher):
        if not self.current_card:
            return
        
        # Disable buttons during reveal
        self.higher_btn.config(state=tk.DISABLED)
        self.lower_btn.config(state=tk.DISABLED)
        
        next_card = self.deck.draw()
        if not next_card:
            self.deck.reset()
            next_card = self.deck.draw()
        
        current_value = self.current_card.get_value()
        next_value = next_card.get_value()
        
        # Determine result
        if next_value > current_value:
            is_correct = guess_higher
            result_text = "higher"
        elif next_value < current_value:
            is_correct = not guess_higher
            result_text = "lower"
        else:
            is_correct = False
            result_text = "the same"
        
        # Update score
        if is_correct:
            self.score += 1
            self.streak += 1
            if self.streak > self.best_streak:
                self.best_streak = self.streak
            message = f"✓ Correct! It was {result_text}!"
            self.result_label.config(fg='#4CAF50')
        else:
            self.streak = 0
            message = f"✗ Wrong! It was {result_text}."
            self.result_label.config(fg='#f44336')
        
        self.result_label.config(text=message)
        self._display_card(next_card)
        self.current_card = next_card
        self._update_stats()
        
        # Re-enable buttons after delay
        self.root.after(1500, lambda: self._enable_buttons())
    
    def _enable_buttons(self):
        self.higher_btn.config(state=tk.NORMAL)
        self.lower_btn.config(state=tk.NORMAL)
        self.result_label.config(fg='#f0e68c', text="Make your next guess!")
    
    def _display_card(self, card):
        if card.is_joker:
            self.card_label.config(text="🃏", fg='purple')
        else:
            color = 'red' if card.is_red() else 'black'
            self.card_label.config(text=str(card), fg=color)
    
    def _update_stats(self):
        self.score_label.config(text=f"Score: {self.score}")
        self.streak_label.config(text=f"Streak: {self.streak} (Best: {self.best_streak})")
        if self.deck:
            self.cards_label.config(text=f"Cards remaining: {self.deck.cards_remaining()}")


def main():
    root = tk.Tk()
    app = CardGameGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
