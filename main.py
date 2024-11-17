import random
from copy import deepcopy

# Define suits and values for the deck
suits = [1, 2, 3, 4]  # Suits represented by numbers 1 to 4
values = list(range(1, 14))

# Create and shuffle the deck
deck = [(suit, value) for suit in suits for value in values]
random.shuffle(deck)

# Function to draw cards from the deck
def draw_cards(num_cards):
    drawn_cards = []
    for _ in range(num_cards):
        if deck:
            drawn_cards.append(deck.pop())
    return drawn_cards

# Draw initial hand and attacking cards
hand = draw_cards(5)
attacking_cards = draw_cards(2)

# Randomly select a trump suit
trump = random.choice(suits)

# Helper function to determine if a card can defend against an attacking card
def can_defend(defending_card, attacking_card, trump_suit):
    # Same suit and higher value, or defending card is trump and attacking card is not trump,
    # or both are trump and defending card has a higher value
    return (
        (defending_card[0] == attacking_card[0] and defending_card[1] > attacking_card[1]) or
        (defending_card[0] == trump_suit and attacking_card[0] != trump_suit) or
        (defending_card[0] == trump_suit and attacking_card[0] == trump_suit and defending_card[1] > attacking_card[1])
    )

# Helper function to determine possible consolidation attacks
def possible_consolidations(active_pool, attacking_cards):
    consolidations = []
    used_cards = set(attacking_cards)  # Track used cards to prevent duplicates
    for card in active_pool:
        if card in used_cards:
            continue
        for attacking_card in attacking_cards:
            if card[1] == attacking_card[1]:
                consolidations.append(card)
                used_cards.add(card)
    return consolidations

# Recursive function to find all possible defense combinations, including consolidations
def defense(hand, attacking_cards, current_defense=[], active_pool=[], depth=0, max_depth=10, level=0):
    indent = "  " * level
    if depth > max_depth:
        print(indent + "Max recursion depth reached, stopping recursion.")
        return

    if not attacking_cards:
        # All attacking cards have been successfully defended
        print(indent + "ORIGINAL: Successful defense:")
        for defense_pair in current_defense:
            print(indent + f"  {defense_pair}")
        return

    current_attacking_card = attacking_cards[0]
    remaining_attacking_cards = attacking_cards[1:]

    defended = False
    for i, card in enumerate(hand):
        if can_defend(card, current_attacking_card, trump):
            # Defending card found, create a new hand without the used card
            new_hand = hand[:i] + hand[i+1:]
            new_current_defense = current_defense + [(current_attacking_card, card)]

            # Recur to defend against the remaining attacking cards
            updated_active_pool = [c for c in deck if c not in new_hand and c not in attacking_cards]
            defense(new_hand, remaining_attacking_cards, new_current_defense, updated_active_pool + [current_attacking_card], depth + 1, max_depth, level + 1)
            defended = True

    if not defended:
        print(indent + "No valid defense for:", current_attacking_card)
    else:
        # Check for possible consolidations and attempt to defend against them
        consolidations = possible_consolidations(active_pool, attacking_cards)
        if consolidations:
            print(indent + "CONSOLIDATION: Attempting consolidations for", attacking_cards)
            for consolidation in consolidations:
                new_attacking_cards = remaining_attacking_cards + [consolidation]
                full_attacking_cards = attacking_cards + [consolidation]
                new_active_pool = [c for c in active_pool if c != consolidation]
                print(indent + f"  Active attacking cards: {full_attacking_cards}")
                defense(hand, new_attacking_cards, current_defense + [("Consolidation", consolidation)], new_active_pool, depth + 1, max_depth, level + 1)

# Output initial state
print("Hand:", hand)
print("Attacking Cards:", attacking_cards)
print("Trump Suit:", trump)

# Call the defense function
defense(hand, attacking_cards)
