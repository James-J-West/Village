def parse_hand(hand: list[str]) -> list[str]:
    new_hand = []
    card_values = {'J': '11', 'Q': '12', 'K': '13', 'A': '14'}
    for card in hand:
        if card.split('|')[0] in card_values:
            card = f'{card_values[card.split('|')[0]]}|{card.split('|')[1]}'
        else:
            card = card
        new_hand.append(card)
    return new_hand
        


def find_attacking_cards(hand: list[str], trump_suit: str):
    """
    Determines the attacking cards from a given hand and trump suit.

    Parameters:
    - hand (list of str): List of cards in the format "value|suit".
    - trump_suit (str): The trump suit.

    Returns:
    - list of str: The attacking cards based on the logic.
    """
    # Sort the hand based on card values and suits
    hand = parse_hand(hand)
    hand.sort(key=lambda card: int(card.split('|')[0]) if card.split('|')[0].isdigit() else {'J': 11, 'Q': 12, 'K': 13, 'A': 14}[card.split('|')[0]])



    # Count the number of cards per suit
    suit_dict = {}
    for card in hand:
        suit = card.split('|')[1]
        suit_dict[suit] = suit_dict.get(suit, 0) + 1

    # Find attacking cards
    attacking_cards = []
    non_trump_cards = [card for card in hand if card.split('|')[1] != trump_suit]
    trump_cards = [card for card in hand if card.split('|')[1] == trump_suit]

    if non_trump_cards:
        # Group non-trump cards by their values
        value_dict = {}
        for card in non_trump_cards:
            value = card.split('|')[0]
            if value in value_dict:
                value_dict[value].append(card)
            else:
                value_dict[value] = [card]

        # Special case: Only two non-trump cards with different values
        if len(value_dict) == len(non_trump_cards):
            # Pick the lowest value non-trump card
            attacking_cards.append(min(non_trump_cards, key=lambda card: int(card.split('|')[0])))
        else:
            non_trump_cards.sort(key=lambda card: int(card.split('|')[0]))
            lowest = non_trump_cards[0]
            lowest_suit = non_trump_cards[0].split('|')[1]
            if suit_dict[lowest_suit] > 1:
                attacking_cards.append(lowest)
            else:
                # Check if there are multiple non-trump cards with the same value
                for value, cards in value_dict.items():
                    if len(cards) > 1:
                        # If we play these, we will only be left with trump cards
                        attacking_cards.extend(cards)
                        break

            # If no multiple same-value cards are found, fall back to other logic
            if not attacking_cards:
                for card in non_trump_cards:
                    suit = card.split('|')[1]
                    value = card.split('|')[0]

                    # Check if there is another card of the same suit with a higher value
                    higher_cards_in_suit = [c for c in hand if c.split('|')[1] == suit and int(c.split('|')[0]) > int(value)]
                    if higher_cards_in_suit:
                        attacking_cards.append(card)

                        # Check for another card of the same value
                        same_value_cards = [c for c in hand if c.split('|')[0] == value and c != card]

                        for same_value_card in same_value_cards:
                            same_value_suit = same_value_card.split('|')[1]

                            # Check if the same-value card's suit has more cards
                            if suit_dict[same_value_suit] > 1:
                                attacking_cards.append(same_value_card)
                        break
    else:
        # If no non-trump cards are available, choose the lowest trump card
        if trump_cards:
            attacking_cards.append(trump_cards[0])

    return attacking_cards


def find_consolidations(hand: list[str], trump_suit: str, attacking_cards: list[str]):
    """
    Determines the consolidation cards from a given hand and trump suit and a set of attacking cards.

    Parameters:
    - hand (list of str): List of cards in the format "value|suit".
    - trump_suit (str): The trump suit.
    - attacking_cards (list of str): List of cards in the format "value|suit"

    Returns:
    - list of str: The consolidation cards based on the logic (Matching value but not a trump).
    """
    consolidation_cards = []
    
    # Extract the values from the attacking cards
    attacking_values = {card.split('|')[0] for card in attacking_cards}
    
    for card in hand:
        value, suit = card.split('|')
        if value in attacking_values and suit != trump_suit:
            consolidation_cards.append(card)
    
    return consolidation_cards

if __name__ == '__main__':
    hand = ['3|S', '4|D', '4|C', '5|C', '6|D', '8|S']
    trump = 'S'
    x = find_attacking_cards(hand, trump)
    print(x)

