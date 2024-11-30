from consts import State


class Player:
    def __init__(self, Id: int):
        self.id = Id
        self.trump: str = ''

    def draw_card(self, num_cards: int, deck: list[tuple[int, str]]):
        cards: list = []
        for i in range(num_cards):
            cards.append(deck.pop())
        self.add_hand(cards)

    def extra_draw_card(self, num_cards: int, deck: list[tuple[int, str]]):
        for _ in range(num_cards):
            self.hand.append(deck.pop())

    def add_hand(self, hand: list[tuple[int, str]]):
        self.hand = hand

    def add_cards_to_hand(self, cards: list[tuple[int, str]]):
        self.hand.extend(cards)

    def decide_consolidation(self, active_cards: list[tuple[tuple[int, str], str]], trump_suit: str):
        active_cards = [card_list for card_list, state in active_cards]
        if len(self.hand) == 0:
            return None
        matching_cards = []
        hand_copy = self.hand.copy()
        for value, _ in active_cards:
            for h_value, h_suit in hand_copy:
                if h_value == value and h_suit != trump_suit:
                    hand_copy.remove((h_value, h_suit))
                    matching_cards.append((h_value, h_suit))
        if len(matching_cards) >= 1:
            print(matching_cards)
            for card in matching_cards:
                self.hand.remove(card)
                yield card
        else:
            return None
        
    def defend(self, active_cards: list[tuple[tuple[int, str], str]], trump_suit: str):
        """EXAMPLE:
        ATTACKING CARDS:  [((4, 'hearts'), State.OPEN), ((5, 'hearts'), State.OPEN)]
        HAND: [(4, 'clubs'), (6, 'hearts'), (8, 'clubs')]
        TRUMP: clubs
        
        DEFENSE: [(4, 'clubs'), (6, 'hearts')]
        HAND AFTER DEFENSE: [(8, 'clubs')]
        """
        if len(self.hand) == 0:
            return None
        
        active_cards = [card for card, state in active_cards]
        defending_cards = []
        hand_copy = self.hand.copy()

        for value, suit in active_cards:
            defended_card = None
            for h_value, h_suit in hand_copy:
                # If the suit matches and the card value is greater, defend with it
                if h_suit == suit and h_value > value:
                    defended_card = (h_value, h_suit)
                    break
            
            # If no non-trump card can defend, use a trump card if available
            if defended_card is None:
                for h_value, h_suit in hand_copy:
                    if h_suit == trump_suit and suit != trump_suit:
                        defended_card = (h_value, h_suit)
                        break
            
            if defended_card:
                defending_cards.append(defended_card)
                hand_copy.remove(defended_card)

        # Remove the defending cards from the player's hand in the correct order
        for card in defending_cards:
            if card in self.hand:
                self.hand.remove(card)
                yield card
            

    def attack(self, trump_suit: str):
        non_trump_cards = [(value, suit) for value, suit in self.hand if suit != trump_suit]
        trump_cards = [(value, suit) for value, suit in self.hand if suit == trump_suit]

        if trump_cards:
            min_value_trump = min(trump_cards, key=lambda card: card[0])[0]
        else:
            min_value_trump = None

        if not non_trump_cards and trump_cards:
            cards_to_play = [(value, suit) for value, suit in trump_cards if value == min_value_trump]
        elif non_trump_cards:
            min_value = min(non_trump_cards, key=lambda card: card[0])[0]
            cards_to_play = [(value, suit) for value, suit in non_trump_cards if value == min_value]
        else:
            cards_to_play = []

        for card in cards_to_play:
            self.hand.remove(card)
            yield card


if __name__ == '__main__':
    # Create a Player instance
    player = Player(Id=1)

    # Set the player's hand for testing
    player.hand = [(7, 'diamonds'), (5, 'clubs'), (6, 'hearts'), (8, 'clubs')]

    # Define the active cards to consolidate with
    active_cards = [((5, 'diamonds'), State.OPEN), ((5, 'hearts'), State.OPEN)]

    # Define the trump suit
    trump_suit = 'clubs'

    # Test decide_consolidation
    consolidation_generator = player.defend(active_cards, trump_suit)

    # Print the results from the generator
    print("Matching cards to consolidate:")
    for card in consolidation_generator:
        print(card)
