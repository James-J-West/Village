import random


def calculate_score(hand: list[tuple], trump: int, deck: list[tuple]):
    score = 0
    for card in hand:
        value = card[1]
        suit = card[0]
        hand_copy = hand.copy()
        hand_copy.pop(hand_copy.index(card))
        if suit == trump:
            trump_weight = 10
        else:
            trump_weight = 2

        hand_copy_vals = sorted([val for suit, val in hand_copy])
        hand_copy_suits = [suit for suit, val in hand_copy]
        
        if value in hand_copy_vals:
            dupe_val_weight = 10
        else:
            dupe_val_weight = 2

        if suit != trump:
            if value > hand_copy_vals[0] and suit in hand_copy_suits:
                dupe_suit_weight = 10
            elif suit in hand_copy_suits:
                dupe_suit_weight = 5
            else:
                dupe_suit_weight = 2
        else:
                dupe_suit_weight = 2

        card_score = dupe_suit_weight * dupe_val_weight * trump_weight * value
        
        score += card_score

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
