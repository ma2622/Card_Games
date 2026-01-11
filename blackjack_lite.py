"""
Blackjack Lite - Alternative Card Game
A simplified version of Blackjack to demonstrate extensibility

Rules:
- Try to get as close to 21 as possible without going over
- Face cards (J, Q, K) are worth 10
- Aces can be 1 or 11 (automatically chosen)
- Beat the dealer to win
"""

import random
from enum import Enum
from typing import List, Optional
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
    JACK = (10, 'J')
    QUEEN = (10, 'Q')
    KING = (10, 'K')
    ACE = (11, 'A')
    
    @property
    def blackjack_value(self):
        """Returns the blackjack value for this rank"""
        return self.value[0]
    
    @property
    def display(self):
        """Returns the display string"""
        return self.value[1]


@dataclass
class Card:
    rank: Rank
    suit: Suit
    
    def __str__(self):
        return f"{self.rank.display}{self.suit.value}"
    
    def get_blackjack_value(self):
        """Returns the blackjack value of the card"""
        return self.rank.blackjack_value
    
    def is_ace(self):
        return self.rank == Rank.ACE


class Deck:
    def __init__(self):
        self.cards: List[Card] = []
        self._initialize_deck()
    
    def _initialize_deck(self):
        self.cards = []
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(rank, suit))
    
    def shuffle(self):
        n = len(self.cards)
        for i in range(n - 1, 0, -1):
            j = random.randint(0, i)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
    
    def draw(self) -> Optional[Card]:
        return self.cards.pop() if self.cards else None
    
    def reset(self):
        self._initialize_deck()
        self.shuffle()


class Hand:
    def __init__(self):
        self.cards: List[Card] = []
    
    def add_card(self, card: Card):
        self.cards.append(card)
    
    def get_value(self) -> int:
        """Calculate hand value with Ace optimization"""
        value = 0
        aces = 0
        
        for card in self.cards:
            if card.is_ace():
                aces += 1
                value += 11
            else:
                value += card.get_blackjack_value()
        
        # Adjust Aces from 11 to 1 if needed
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
        
        return value
    
    def is_bust(self) -> bool:
        return self.get_value() > 21
    
    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.get_value() == 21
    
    def __str__(self):
        cards_str = ' '.join(str(card) for card in self.cards)
        return f"{cards_str} (Value: {self.get_value()})"
    
    def clear(self):
        self.cards = []


class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.wins = 0
        self.losses = 0
        self.pushes = 0
    
    def start_new_round(self):
        """Starts a new round of blackjack"""
        if len(self.deck.cards) < 15:
            self.deck.reset()
        
        self.player_hand.clear()
        self.dealer_hand.clear()
        
        # Deal initial cards
        self.player_hand.add_card(self.deck.draw())
        self.dealer_hand.add_card(self.deck.draw())
        self.player_hand.add_card(self.deck.draw())
        self.dealer_hand.add_card(self.deck.draw())
    
    def player_hit(self) -> bool:
        """Player takes a card. Returns True if player can continue."""
        card = self.deck.draw()
        self.player_hand.add_card(card)
        return not self.player_hand.is_bust()
    
    def dealer_play(self):
        """Dealer plays according to standard rules (hit on 16, stand on 17)"""
        while self.dealer_hand.get_value() < 17:
            self.dealer_hand.add_card(self.deck.draw())
    
    def determine_winner(self) -> str:
        """Determine the winner and update statistics"""
        player_value = self.player_hand.get_value()
        dealer_value = self.dealer_hand.get_value()
        
        # Player bust always loses
        if self.player_hand.is_bust():
            self.losses += 1
            return "dealer_bust_player"
        
        # Dealer bust, player wins
        if self.dealer_hand.is_bust():
            self.wins += 1
            return "player_dealer_bust"
        
        # Check for blackjacks
        if self.player_hand.is_blackjack() and not self.dealer_hand.is_blackjack():
            self.wins += 1
            return "player_blackjack"
        
        if self.dealer_hand.is_blackjack() and not self.player_hand.is_blackjack():
            self.losses += 1
            return "dealer_blackjack"
        
        # Compare values
        if player_value > dealer_value:
            self.wins += 1
            return "player_higher"
        elif dealer_value > player_value:
            self.losses += 1
            return "dealer_higher"
        else:
            self.pushes += 1
            return "push"
    
    def get_statistics(self) -> dict:
        total = self.wins + self.losses + self.pushes
        win_rate = (self.wins / total * 100) if total > 0 else 0
        return {
            'wins': self.wins,
            'losses': self.losses,
            'pushes': self.pushes,
            'total': total,
            'win_rate': win_rate
        }


def play_blackjack_cli():
    """CLI interface for Blackjack Lite"""
    print("=" * 50)
    print("  BLACKJACK LITE")
    print("=" * 50)
    print("\nTry to get as close to 21 as possible!")
    print("Face cards are worth 10, Aces are 1 or 11.")
    print("Dealer stands on 17.\n")
    
    game = BlackjackGame()
    
    while True:
        game.start_new_round()
        
        print("\n" + "=" * 50)
        print(f"Dealer shows: {game.dealer_hand.cards[0]}")
        print(f"Your hand: {game.player_hand}")
        
        # Check for player blackjack
        if game.player_hand.is_blackjack():
            game.dealer_play()
            print(f"\nDealer's hand: {game.dealer_hand}")
            result = game.determine_winner()
            if result == "player_blackjack":
                print("🎉 BLACKJACK! You win!")
            else:
                print("Push - both have blackjack")
        else:
            # Player's turn
            while True:
                action = input("\n(H)it or (S)tand? ").upper()
                
                if action == 'H':
                    can_continue = game.player_hit()
                    print(f"Your hand: {game.player_hand}")
                    
                    if not can_continue:
                        print("\n💥 BUST! You lose.")
                        game.determine_winner()
                        break
                elif action == 'S':
                    # Dealer's turn
                    print(f"\nDealer's hand: {game.dealer_hand}")
                    game.dealer_play()
                    print(f"Dealer's final hand: {game.dealer_hand}")
                    
                    # Determine winner
                    result = game.determine_winner()
                    player_val = game.player_hand.get_value()
                    dealer_val = game.dealer_hand.get_value()
                    
                    if "player" in result and "bust" not in result:
                        print(f"🎉 You win! ({player_val} vs {dealer_val})")
                    elif result == "push":
                        print(f"Push - tie at {player_val}")
                    else:
                        print(f"Dealer wins ({dealer_val} vs {player_val})")
                    break
                else:
                    print("Please enter 'H' or 'S'")
        
        # Show statistics
        stats = game.get_statistics()
        print(f"\nRecord: {stats['wins']}W - {stats['losses']}L - {stats['pushes']}P")
        print(f"Win Rate: {stats['win_rate']:.1f}%")
        
        # Continue?
        if input("\nPlay another hand? (y/n): ").lower() != 'y':
            break
    
    print("\n" + "=" * 50)
    print("  FINAL STATISTICS")
    print("=" * 50)
    stats = game.get_statistics()
    print(f"Wins: {stats['wins']}")
    print(f"Losses: {stats['losses']}")
    print(f"Pushes: {stats['pushes']}")
    print(f"Win Rate: {stats['win_rate']:.1f}%")
    print("\nThanks for playing!")


if __name__ == "__main__":
    play_blackjack_cli()
