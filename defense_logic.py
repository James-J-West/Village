def parse_card(card):
    """Parse a card string into its value and suit."""
    card_values = {'J': '11', 'Q': '12', 'K': '13', 'A': '14'}
    value, suit = card.split('|')
    if value in card_values:
        value = card_values[value]
    return int(value), suit

def find_pass_or_defense(hand, trump_suit, attacking_cards):
    """
    Prioritize passing on (playing all valid cards of the same value as the attacking cards)
    over defending. Ensure cards used for defense are not reused for subsequent attacks.
    
    Parameters:
        hand: List of strings representing cards in hand (e.g., '5|S').
        trump_suit: String representing the trump suit (e.g., 'S').
        attacking_cards: List of strings representing attacking cards (e.g., '8|H').
    
    Returns:
        Tuple where:
        - First element is 'PASS ON' if passing on is possible,
          otherwise 'DEFENSE'.
        - Second element is a dictionary mapping attacking cards to their response cards
          (a list of cards for 'PASS ON', or a single card for 'DEFENSE').
    """
    pass_on_options = {}
    defense_options = {}
    used_cards = set()  # Track cards that have been used for defense
    can_pass_on = True  # Track if passing on is possible for all attacking cards

    for attack_card in attacking_cards:
        attack_value, attack_suit = parse_card(attack_card)
        pass_on_candidates = [
            card for card in hand if parse_card(card)[0] == attack_value and parse_card(card)[1] != trump_suit
        ]
        
        # Collect all valid pass-on candidates
        pass_on_options[attack_card] = pass_on_candidates
        if not pass_on_candidates:
            can_pass_on = False

    # If passing on is possible for all attacking cards, prioritize it
    if can_pass_on:
        return 'PASS ON', pass_on_options

    # Otherwise, find the lowest valid defense for each attacking card
    for attack_card in attacking_cards:
        attack_value, attack_suit = parse_card(attack_card)
        same_suit_defenses = []
        trump_defenses = []

        for card in hand:
            if card in used_cards:  # Skip cards already used for defense
                continue
            card_value, card_suit = parse_card(card)
            if card_suit == attack_suit and card_value > attack_value:
                same_suit_defenses.append(card)  # Higher card of the same suit
            elif card_suit == trump_suit:
                if attack_suit != trump_suit or (attack_suit == trump_suit and card_value > attack_value):
                    trump_defenses.append(card)  # Valid trump card

        # Determine the lowest valid defense
        if same_suit_defenses:
            chosen_card = min(same_suit_defenses, key=lambda c: parse_card(c)[0])
            defense_options[attack_card] = chosen_card
            used_cards.add(chosen_card)
        elif trump_defenses:
            chosen_card = min(trump_defenses, key=lambda c: parse_card(c)[0])
            defense_options[attack_card] = chosen_card
            used_cards.add(chosen_card)
        else:
            defense_options[attack_card] = None

    return 'DEFENSE', defense_options