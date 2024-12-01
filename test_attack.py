import pytest
from attack_logic import find_attacking_cards, find_consolidations
@pytest.mark.parametrize(
    "hand, trump_suit, expected",
    [
        # Case 2: A mix of trumps and non-trumps, prioritizing non-trump cards
        (['3|S', '4|D', '4|C', '5|C', '6|D', '8|S'], 'S', ['4|D', '4|C']),

        # Case 3: Only trump cards in hand
        (['3|S', '4|S', '5|S', '6|S'], 'S', ['3|S']),

        # Case 4: Two non-trump cards of the same value
        (['6|H', '6|C', '5|C', '4|C', '3|C', '6|D'], 'C', ['6|H', '6|D']),

        # Case 5: Two different value non-trump cards, choose the lowest
        (['6|H', '6|C', '5|C', '4|C', '8|S', '7|D'], 'C', ['6|H']),

        (['10|H', '3|C', '5|H', 'A|D', '4|D'], 'C', ['4|D']),

        (['6|C', '12|S', '12|H', '12|C', '4|H', '1|S'], 'C', ['1|S'])

    ]
)
def test_find_attacking_cards(hand, trump_suit, expected):
    result = find_attacking_cards(hand, trump_suit)
    assert result == expected, f"Expected {expected}, but got {result}"

@pytest.mark.parametrize(
    "hand, trump_suit, attacking_cards, expected",
    [
        # Case 2: A mix of trumps and non-trumps, prioritizing non-trump cards
        (['3|S', '4|H', '7|C', '5|C', '6|D', '8|S'], 'S', ['4|D', '4|C'], ['4|H']),

        (['3|S', '4|H', '7|C', '5|C', '6|D', '8|S'], 'H', ['4|D', '4|C'], []),

        (['4|H', '4|S'], 'H', ['4|D', '4|C'], ['4|S']),

        (['4|H', '4|S', '4|C'], 'H', ['4|D'], ['4|S', '4|C'])

    ]
)
def test_consolidation(hand, trump_suit, attacking_cards, expected):
    result = find_consolidations(hand, trump_suit, attacking_cards)
    assert result == expected
