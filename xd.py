import random
from copy import deepcopy
import json

suits = ['hearts', 'diamonds', 'clubs', 'spades']
values = list(range(2, 15))  # Values from 2 to Ace (14)
deck = [(suit, value) for suit in suits for value in values]

random.shuffle(deck)

# Draw cards from the deck
def draw_cards(deck, num_cards):
    drawn_cards = []
    for _ in range(num_cards):
        if deck:
            drawn_cards.append(deck.pop())
    return drawn_cards

hand = draw_cards(deck, 5)
attacking_card = draw_cards(deck, 1)[0]

# Creating the rest_of_cards list excluding hand and attacking card
in_play_cards = hand + [attacking_card]

# Using list comprehension to remove in-play cards from deck
rest_of_cards = [card for card in deck if card not in in_play_cards]

# Choose trump suit
trump = random.choice(suits)

print("Hand:", hand)
print("Attacking Card:", attacking_card)
print("Trump Suit:", trump)
print("Rest of Cards:", len(rest_of_cards))

# Defend function
def defend(original_hand: list, attacking_card: tuple, trump: str):
    branches = []

    for card in original_hand:
        # Create a copy of the hand for this branch
        hand = original_hand.copy()
        branch = [attacking_card]
        card_suit = card[0]
        card_value = card[1]

        if card_value > attacking_card[1] and card_suit == attacking_card[0]:
            hand.remove(card)
            branch.append(card)
            branch_state = 'defended'

        elif card_suit == trump and attacking_card[0] != trump:
            hand.remove(card)
            branch.append(card)
            branch_state = 'defended'
        
        else:
            branch_state = 'lost'
            # We extend the branch with attacking_card, not the hand to avoid infinite addition
            branch.append(card)

        # Add the branch details to the branches list
        branches.append({
            'branch_state': branch_state,
            'branch_defender_cards': hand,
            'branch_cards_in_play': branch.copy(),
            'branch_total_cards': branch.copy()
        })

    return branches

# Respond to defense function
def respond_to_defence(branches: list[dict], rest_of_cards: list[tuple[str, int]]):
    for branch in branches:
        if branch['branch_state'] == 'defended':
            defended_card = branch['branch_cards_in_play'][-1]
            print('DEFENDED WITH: ', defended_card)
            active_card_values = [card[1] for card in branch['branch_cards_in_play']]
            for card in rest_of_cards:
                if card[1] in active_card_values and card[0] != trump:
                    print('RESPONSE: ', card)
                    rest_of_cards.remove(card)
                    new_branch = branch.copy()
                    new_branch['branch_cards_in_play'] = branch['branch_cards_in_play'].copy()
                    new_branch['branch_total_cards'] = branch['branch_total_cards'].copy()
                    new_branch['branch_cards_in_play'].append(card)
                    new_branch['branch_total_cards'].append(card)
                    yield new_branch
            else:
                return None
        
# Defend branch function
def defend_branch(_branch: dict):
    _branches = []
    active_hand = _branch['branch_defender_cards']
    attacking_card = _branch['branch_cards_in_play'][-1]

    # Iterate through each card in the active hand to determine defense possibilities
    for card in active_hand:
        # Create a unique copy of all_cards and cards_in_play for each branch to ensure no unintended modifications
        all_cards = _branch['branch_total_cards'].copy()
        cards_in_play = _branch['branch_cards_in_play'].copy()
        hand = active_hand.copy()  # Create a copy of the hand for this branch
        card_suit = card[0]
        card_value = card[1]

        # Condition to successfully defend the attacking card
        if (card_value > attacking_card[1] and card_suit == attacking_card[0]) or (card_suit == trump and attacking_card[0] != trump):
            hand.remove(card)
            cards_in_play.append(card)
            all_cards.append(card)  # Add only the defending card to all_cards
            branch_state = 'defended'
        else:
            branch_state = 'lost'
            # No changes to all_cards in case of lost defense

        # Avoid duplicating cards in play
        cards_in_play = list(dict.fromkeys(cards_in_play))  # Remove duplicates
        all_cards = list(dict.fromkeys(all_cards))  # Remove duplicates

        # Add the branch details to the branches list
        _branches.append({
            'branch_state': branch_state,
            'branch_defender_cards': hand,
            'branch_cards_in_play': cards_in_play,
            'branch_total_cards': all_cards
        })

    return _branches

branches = defend(hand, attacking_card, trump)

for response_branch in respond_to_defence(branches, rest_of_cards):
    b2 = defend_branch(response_branch)
    for branch in b2:
        if branch['branch_state'] == 'defended':
            print('DEFENDED THE RESPONSE')
            print('HAND: ', branch['branch_defender_cards'])
            print('CARDS ON TABLE: ', branch['branch_cards_in_play'])
            print('-')
        else:
            print('LOST')
            print('HAND BEFORE PICKUP: ', branch['branch_defender_cards'])
            print('CARDS ON TABLE: ', branch['branch_cards_in_play'])
            branch['branch_defender_cards'].extend(branch['branch_total_cards'])
            print('HAND AFTER PICKUP: ', branch['branch_defender_cards'])
            print('-')
