
from enum import Enum


SUITS = ['H', 'C', 'S', 'D']

VALUES = [x for x in range(1, 15)]

DECK = [(value, suit) for value in VALUES for suit in SUITS]

class COMMANDS(Enum):
    ATTACK = 'attack'
    DEFEND = 'defend'
    CONSOLIDATE = 'attack'
    PICKUP = 'pickup'
    PASS = 'pass'

class State(Enum):
    OPEN = 'open'
    DEFENDED = 'defended'
    DEFENDED_OPEN = 'def-open'