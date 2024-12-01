import pytest
from defense_logic import find_pass_or_defense
@pytest.mark.parametrize(
    "hand, trump_suit, attacking_cards, expected",
    [

        (['10|H', '7|S', '9|S', '6|D', '13|C', '14|S'], 'D', ['8|S', '9|H', '10|D'], ('DEFENSE', {'8|S': '9|S', '9|H': '10|H', '10|D': None})),

        (['10|H'], 'D', ['10|S'], ('PASS ON', {'10|S': ['10|H']})),

        (['Q|H', 'Q|C', '8|C', '10|D', '9|C'], 'C', ['4|D'], ('DEFENSE', {'4|D': '10|D'})),

        (['3|C', '14|D', '10|H', '5|H',  '4|D'], 'C', ['8|S'], ('DEFENSE', {'8|S': '3|C'})),

        (['13|S','10|D'], 'D', ['10|S'], ('DEFENSE', {'10|S': '13|S'})),

        (['10|H', '10|C', '10|D', '13|D'], 'D', ['10|S'], ('PASS ON', {'10|S': ['10|H', '10|C']})),

        (['10|H', '10|D', '13|D'], 'D', ['10|S', '10|C'], ('PASS ON', {'10|S': ['10|H'], '10|C': ['10|H']})),

        (['10|H', '13|D'], 'D', ['10|S', '10|C', '10|D'], ('PASS ON', {'10|S': ['10|H'], '10|C': ['10|H'], '10|D': ['10|H']})),

        (['10|H', '10|D', '13|D'], 'D', ['10|S', '11|C'], ('DEFENSE', {'10|S': '10|D', '11|C': '13|D'})),

        (['10|H', '10|D', '13|D'], 'C', ['10|S', '11|C'], ('DEFENSE', {'10|S': None, '11|C': None})),

        (['10|C', '10|D', '13|D'], 'C', ['10|S', '11|C'], ('DEFENSE', {'10|S': '10|C', '11|C': None})),
        
        (['10|H', '7|S', '9|S', '6|D', '13|C', '14|D'], 'D', ['8|S', '9|H', '10|D'], ('DEFENSE', {'8|S': '9|S', '9|H': '10|H', '10|D': '14|D'})),

    ]
)
def test_find_defense_or_pass(hand, trump_suit, attacking_cards, expected):
    result = find_pass_or_defense(hand, trump_suit, attacking_cards)
    assert result == expected, f"Expected {expected}, but got {result}"
