from itertools import chain, combinations
from collections import defaultdict
import copy
import json

TRUMP_SUIT = 1  # Define trump suit

class Node:
    def __init__(self, player_1_hand, player_2_hand, next_to_attack, parent=None):
        self.player_1_hand = player_1_hand
        self.player_2_hand = player_2_hand
        self.next_to_attack = next_to_attack
        self.children = []
        self.parent = parent

    def add_child(self, child_node):
        self.children.append(child_node)

    def print_tree(self, level=0):
        indent = "    " * level
        print('\n')
        print(f"{indent}Player 1 hand: {self.player_1_hand}")
        print(f"{indent}Player 2 hand: {self.player_2_hand}")
        if not self.player_1_hand and not self.player_2_hand:
            if self.parent and self.parent.next_to_attack == "Player 1":
                print(f"{indent}PLAYER 2 WON!")
            else:
                print(f"{indent}PLAYER 1 WON!")
        elif not self.player_1_hand:
            print(f"{indent}PLAYER 1 WON!")
        elif not self.player_2_hand:
            print(f"{indent}PLAYER 2 WON!")
        else:
            print(f"{indent}Next to attack: {self.next_to_attack}")
        for child in self.children:
            child.print_tree(level + 1)

    def to_dict(self):
        node_dict = {
            "player_1_hand": self.player_1_hand,
            "player_2_hand": self.player_2_hand,
            "next_to_attack": self.next_to_attack,
            "children": [child.to_dict() for child in self.children]
        }
        if not self.player_1_hand and not self.player_2_hand:
            if self.parent and self.parent.next_to_attack == "Player 1":
                node_dict["result"] = "PLAYER 2 WON!"
            else:
                node_dict["result"] = "PLAYER 1 WON!"
        elif not self.player_1_hand:
            node_dict["result"] = "PLAYER 1 WON!"
        elif not self.player_2_hand:
            node_dict["result"] = "PLAYER 2 WON!"
        return node_dict

def generate_attacks(hand, defender_hand_size):
    # Group cards by their values
    grouped_cards = defaultdict(list)
    for card in hand:
        value, suit = card
        grouped_cards[value].append(card)

    # Function to get all subsets of a given list with a maximum size of defender_hand_size
    def all_subsets(cards):
        return chain(*[combinations(cards, r) for r in range(1, min(len(cards), defender_hand_size) + 1)])

    # Get all subsets of cards with the same value, limited by the number of cards in defender's hand
    attacks = []
    for value, cards in grouped_cards.items():
        for subset in all_subsets(cards):
            attacks.append(list(subset))
    
    return attacks

def can_defend(attack, defender_hand):
    for attack_card in attack:
        attack_value, attack_suit = attack_card
        # Check if there is a defending card in defender's hand
        for defender_card in defender_hand:
            defender_value, defender_suit = defender_card
            if defender_suit == attack_suit and defender_value > attack_value:
                return defender_card
            elif defender_suit == TRUMP_SUIT and (attack_suit != TRUMP_SUIT or defender_value > attack_value):
                # Trump card beats any non-trump or lower-value trump
                return defender_card
    return None

def resolve_attack(player_1_hand, player_2_hand, attack):
    # Make copies of the hands to avoid modifying during iteration
    player_1_hand_copy = copy.deepcopy(player_1_hand)
    player_2_hand_copy = copy.deepcopy(player_2_hand)

    defending_cards = []
    for card in attack:
        defending_card = can_defend([card], player_2_hand_copy)
        if defending_card:
            defending_cards.append(defending_card)
            player_2_hand_copy.remove(defending_card)
        else:
            # Unsuccessful defense: player 2 picks up the attacking cards
            for attack_card in attack:
                if attack_card in player_1_hand_copy:
                    player_1_hand_copy.remove(attack_card)
                    player_2_hand_copy.append(attack_card)
            print(f"Defense unsuccessful. Player 1 loses {attack}. Player 2 picks up the attacking cards.")
            return player_1_hand_copy, player_2_hand_copy, "Player 1"

    # Successful defense: both players lose the cards involved
    for card in attack:
        if card in player_1_hand_copy:
            player_1_hand_copy.remove(card)
    print(f"Defense successful. Player 1 loses {attack}. Player 2 loses the defending cards {defending_cards}.")
    return player_1_hand_copy, player_2_hand_copy, "Player 2"

def expand_node(node, depth_limit, current_depth=0):
    # Stop expanding if the depth limit is reached or if there is a result
    if current_depth >= depth_limit or not node.player_1_hand or not node.player_2_hand:
        return
    
    if node.next_to_attack == "Player 1":
        attacks = generate_attacks(node.player_1_hand, len(node.player_2_hand))
    else:
        attacks = generate_attacks(node.player_2_hand, len(node.player_1_hand))

    for attack in attacks:
        player_1_hand = copy.deepcopy(node.player_1_hand)
        player_2_hand = copy.deepcopy(node.player_2_hand)

        if node.next_to_attack == "Player 1":
            player_1_hand, player_2_hand, next_to_attack = resolve_attack(player_1_hand, player_2_hand, attack)
        else:
            player_2_hand, player_1_hand, next_to_attack = resolve_attack(player_2_hand, player_1_hand, attack)

        # Create a new node for each possible outcome
        child_node = Node(player_1_hand, player_2_hand, next_to_attack=next_to_attack, parent=node)
        node.add_child(child_node)
        # Recursively expand the newly created child node with depth limit
        expand_node(child_node, depth_limit, current_depth + 1)

# Example usage
initial_player_1_hand = [
    (4, 1),
    (4, 2),
    (4, 3),
    (10, 1),
    (13, 3),
    (11, 2),
    (4, 4),
]
    

initial_player_2_hand = [
    (14, 3),
]

# Create the root of the tree
root = Node(initial_player_1_hand, initial_player_2_hand, next_to_attack="Player 1")

# Expand the tree starting from the root node with a depth limit
expand_node(root, depth_limit=10)

# Write the tree to a JSON file
with open('game_tree.json', 'w') as json_file:
    json.dump(root.to_dict(), json_file, indent=4)
