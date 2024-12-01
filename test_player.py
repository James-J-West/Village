import pytest
from attack_logic import find_attacking_cards
from player import Player
@pytest.mark.parametrize(
    "hand, trump_suit, expected_before, expected_after, attacking_cards",
    [
        (['10|H', '7|S', '6|S', '6|D', '13|C', '14|S'], 'H', ['10|H', '7|S', '6|S', '6|D', '13|C', '14|S'], ['10|H', '7|S', '13|C', '14|S'], ['6|S', '6|D']),
    ]
)
def test_player_attack(hand, trump_suit, expected_before, expected_after, attacking_cards):
    p = Player(trump_suit)
    p.import_hand(hand)
    assert p.hand == expected_before
    a_c = p.attack()
    assert a_c == attacking_cards
    assert p.hand == expected_after
