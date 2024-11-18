import random
import json

with open('scores/scores_weights.json', "r") as f:
    scores_json = json.load(f)

def calculate_score(hand: list[tuple], trump: int, deck: list[tuple]):
    score = 0
    num_trumps = sum(1 for card in hand if card[0] == trump)
    trump_bonus = scores_json.get('trump_bonus', 1.1) ** num_trumps

    for card in hand:
        value = card[1]
        suit = card[0]
        
        # Determine trump weight
        if suit == trump:
            trump_weight = scores_json['trump_weight_present']
        else:
            trump_weight = scores_json['trump_weight_not']
        
        # Duplicate value weight
        value_count = sum(1 for c in hand if c[1] == value)
        if value_count > 1:
            dupe_val_weight = scores_json['dupe_val_weight_duped']
        else:
            dupe_val_weight = scores_json['dupe_val_weight_single']
        
        # High card weight (higher value cards receive more weight)
        high_card_weight = value / max(card[1] for card in deck)  # Normalize by highest card value in the deck
        
        # Suit duplication weight
        suit_count = sum(1 for c in hand if c[0] == suit)
        if suit != trump:
            highest_same_suit = max((c[1] for c in hand if c[0] == suit and c != card), default=-1)
            if value > highest_same_suit and suit_count > 1:
                dupe_suit_weight = scores_json['dupe_suit_weight_non_trump_high_Card']
            elif suit_count > 1:
                dupe_suit_weight = scores_json['dupe_suit_weight_non_trump']
            else:
                dupe_suit_weight = scores_json['dupe_suit_weight_no_dupe']
        else:
            dupe_suit_weight = 1

        # Calculate card score using all the weights
        card_score = (
            trump_weight *
            dupe_val_weight *
            high_card_weight *
            dupe_suit_weight *
            value
        )
        
        score += card_score

    # Apply overall trump bonus to the final score
    score *= trump_bonus

    return score



def draw_cards(deck:list[tuple], num_cards: int):
    """Draws a specified number of cards from the deck."""
    drawn_cards = []
    for _ in range(num_cards):
        if deck:  # Ensure cards are available
            drawn_cards.append(deck.pop())
    return drawn_cards

if __name__ == '__main__':
    suits = [1, 2, 3, 4]  # Suits represented by numbers
    values = list(range(1, 14))
    scores = []
    for i in range(250):
        deck: list[tuple[int, int]] = [(suit, value) for suit in suits for value in values]
        random.shuffle(deck)
        trump: int = random.choice(suits)
        hand = draw_cards(deck, 5)
        # print(hand, ' | ' , trump,' | ' , calculate_score(hand, trump, deck))
        scores.append(
            {
                'hand': hand,
                'trump': trump,
                'score': calculate_score(hand, trump, deck)
            }
        )
    max_score = max([hand['score'] for hand in scores])
    for data in scores:
        if data['score'] == max_score:
            print(hand, ' | ' , trump,' | ' , calculate_score(hand, trump, deck))
