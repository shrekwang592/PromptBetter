class BlackjackDeck(Deck):
    def __init__(self):
        super().__init__()
    # Design a deck of cards
    # Constraints and assumptions
    # Is this a generic deck of cards for games like poker and black jack?
    # Yes, design a generic deck then extend it to black jack
    # Can we assume the deck has 52 cards (2-10, Jack, Queen, King, Ace) and 4 suits?
    # Yes
    # Can we assume inputs are valid or do we have to validate them?
    # Assume they're valid
    # Additional methods could be added here to handle blackjack-specific rules,
    # such as calculating the value of a hand or dealing with aces.
    
    def get_card_value(self, card):
        if card.rank in ['Jack', 'Queen', 'King']:
            return 10
        elif card.rank == 'Ace':
            return 11  # Flexibility to be 1 can be determined in a hand value method
        else:
            return int(card.rank)
    
    def hand_value(self, hand):
        value = sum(self.get_card_value(card) for card in hand)
        # Adjust for aces—if the value exceeds 21, an ace can be counted as 1 instead of 11
        aces = sum(1 for card in hand if card.rank == 'Ace')
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value