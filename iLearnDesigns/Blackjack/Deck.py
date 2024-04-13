import random

class Deck:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self):
        self.cards = [Card(rank, suit) for suit in Deck.suits for rank in Deck.ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, number_of_cards):
        return [self.cards.pop() for _ in range(number_of_cards)]

    def __repr__(self):
        return f"Deck of {len(self.cards)} cards"
    
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank} of {self.suit}"