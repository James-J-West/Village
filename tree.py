import random
from typing import List, Tuple, Optional, Dict, Union, FrozenSet


class TreeNode:
    """
    A class representing a node in a tree structure.

    Attributes:
        data (dict): The data stored in this node.
        children (list[TreeNode]): A list of children nodes.
        parent (Optional[TreeNode]): The parent node, if any.
        score (int): The score of the node based on the hand.
    """
    def __init__(self, data: dict):
        self.data: dict = data
        self.children: List['TreeNode'] = []
        self.parent: Optional['TreeNode'] = None
        self.score: int = self.calculate_score()

    def add_child(self, child: 'TreeNode') -> None:
        """Adds a child node to this node if it is not a duplicate."""
        if not isinstance(child, TreeNode):
            raise ValueError("Child must be an instance of TreeNode")
        if not any(existing_child.data == child.data for existing_child in self.children):
            child.parent = self
            self.children.append(child)

    def calculate_score(self) -> float:
        """Calculates the score of the node based on the hand with multiple factors."""
        hand = self.data.get('hand', [])
        trump = self.data.get('trump', None)
        rest_of_cards = self.data.get('rest_of_cards', [])

        score = 0
        # Average card assumption after a defense (average value is 7, non-trump)
        num_cards_needed = max(0, 5 - len(hand))
        assumed_drawn_cards = [(0, 7)] * num_cards_needed
        updated_hand = hand + assumed_drawn_cards

        # Penalize for having more than 5 cards, unless they are trump or high value
        if len(updated_hand) > 5:
            extra_cards = updated_hand[5:]
            for card in extra_cards:
                suit, value = card
                if suit != trump and value <= 12:
                    score -= 5  # Penalize for excess non-trump, low-value cards

        for card in updated_hand:
            suit, value = card

            # Factor 1: Card value (prefer values above 7)
            if value > 7:
                card_value_weight = 1 + ((value - 7) / 7)  # Linearly increase weight for values > 7
            else:
                card_value_weight = 1 - ((7 - value) / 7)  # Linearly decrease weight for values < 7

            # Factor 2: Trump cards are worth more
            trump_weight = 10 if suit == trump else 1.2 if value > 7 else 5  # Favor trumps more if value > 7

            # Factor 3: Multiples are good
            same_value_count = sum(1 for c in updated_hand if c[1] == value)
            multiple_weight = 2 if same_value_count >= 3 else 1.5 if same_value_count == 2 else 1

            # Factor 4: How many cards this card can beat
            if card == (0, 7):
                beatable_count = 5
            else:
                beatable_count = sum(1 for c in rest_of_cards if (c[0] == suit and c[1] < value) or (c[0] != suit and suit == trump))
            beatable_weight = (beatable_count / len(rest_of_cards) if rest_of_cards else 1) + 1  # Normalize and scale

            # Calculate weighted score for the card
            card_score = card_value_weight * trump_weight * multiple_weight * beatable_weight
            score += card_score

        return score


    def __repr__(self, level=0) -> str:
        """Provides a pretty string representation of the node."""
        indent = "    " * level
        repr_str = f"{indent}TreeNode(hand={self.data.get('hand', [])}, score={self.score}, cards_on_table={self.data.get('cards_on_table', [])})\n"
        for child in self.children:
            repr_str += child.__repr__(level + 1)
        return repr_str


class GameState:
    """
    A class for managing the state of the game.

    Attributes:
        deck (List[Tuple[int, int]]): The shuffled deck of cards.
        trump (int): The trump suit.
    """
    def __init__(self):
        self.suits = [1, 2, 3, 4]  # Suits represented by numbers
        self.values = list(range(1, 14))
        self.deck: List[Tuple[int, int]] = [(suit, value) for suit in self.suits for value in self.values]
        random.shuffle(self.deck)
        self.trump: int = random.choice(self.suits)

    def draw_cards(self, num_cards: int) -> List[Tuple[int, int]]:
        """Draws a specified number of cards from the deck."""
        drawn_cards = []
        for _ in range(num_cards):
            if self.deck:  # Ensure cards are available
                drawn_cards.append(self.deck.pop())
        return drawn_cards

    def draw_attacking_cards(self) -> List[Tuple[int, int]]:
        """Draws a random number of cards of the same value from the deck to use as attacking cards."""
        if not self.deck:
            return []
        # Randomly select a value from the rest of the deck
        selected_card = random.choice(self.deck)
        selected_value = selected_card[1]
        # Find all cards with the same value
        same_value_cards = [card for card in self.deck if card[1] == selected_value]
        # Randomly select the number of cards to draw (between 1 and the total number of cards with that value)
        num_to_draw = random.randint(1, len(same_value_cards))
        attacking_cards = random.sample(same_value_cards, num_to_draw)
        # Remove the selected cards from the deck
        for card in attacking_cards:
            self.deck.remove(card)
        return attacking_cards


def find_all_valid_defenses(attacking_cards: List[Tuple[int, int]], hand: List[Tuple[int, int]], trump: int) -> List[List[Tuple[int, int]]]:
    """
    Finds all possible valid defenses for the given attacking cards.

    Args:
        attacking_cards (List[Tuple[int, int]]): The attacking cards on the table.
        hand (List[Tuple[int, int]]): The player's hand.
        trump (int): The trump suit.

    Returns:
        List[List[Tuple[int, int]]]: A list of possible defenses, where each defense is a list of cards from the hand.
    """
    all_defenses = []

    def find_defense(index: int, current_defense: List[Tuple[int, int]], used_cards: set):
        if index == len(attacking_cards):
            all_defenses.append(current_defense.copy())
            return

        attack_suit, attack_value = attacking_cards[index]
        # Adding logic for matching card values to keep all attacking cards OPEN
        matching_cards = [card for card in hand if card[1] == attack_value and card not in used_cards]
        if matching_cards:
            used_cards.add(matching_cards[0])
            current_defense.append(matching_cards[0])
            all_defenses.append(current_defense.copy())
            current_defense.pop()
            used_cards.remove(matching_cards[0])

        possible_defenses = [card for card in hand if card not in used_cards and (
            (card[0] == attack_suit and card[1] > attack_value) or
            (card[0] == trump and attack_suit != trump)
        )]

        for defense in possible_defenses:
            if defense[0] == attack_suit and defense[1] <= attack_value and defense[0] != trump:
                continue  # Skip invalid defense
            used_cards.add(defense)
            current_defense.append(defense)
            find_defense(index + 1, current_defense, used_cards)
            current_defense.pop()
            used_cards.remove(defense)

    find_defense(0, [], set())
    return all_defenses


def build_tree() -> TreeNode:
    """
    Builds the initial tree for the game state and generates possible defenses as children nodes.

    Returns:
        TreeNode: The root node of the tree.
    """
    game = GameState()
    print(game.trump)
    hand = game.draw_cards(5)
    attacking_cards = game.draw_attacking_cards()
    rest_of_cards = game.deck.copy()  # Remaining cards in the deck

    # Update attacking cards to include state (OPEN or OPEN)
    cards_on_table = [(card, 'OPEN') for card in attacking_cards]

    root_data = {
        'hand': hand,
        'cards_on_table': cards_on_table,
        'trump': game.trump,
        'rest_of_cards': rest_of_cards
    }
    root = TreeNode(root_data)

    # Create children nodes for each possible defense
    all_valid_defenses = find_all_valid_defenses(attacking_cards, hand, game.trump)
    for valid_defense in all_valid_defenses:
        updated_cards_on_table = [
            (card, 'DEFENDED') if card in attacking_cards else (card, card_state)
            for card, card_state in cards_on_table
        ]
        updated_cards_on_table += [(card, 'OPEN') for card in valid_defense if card not in attacking_cards]

        child_data = {
            'hand': [card for card in hand if card not in valid_defense],
            'cards_on_table': updated_cards_on_table,
            'trump': game.trump,
            'rest_of_cards': rest_of_cards
        }
        child_node = TreeNode(child_data)
        root.add_child(child_node)

    # Collapse the children to keep only the top 3 nodes with the best scores, without duplicates
    if root.children:
        unique_children = list({frozenset(tuple(card) for card in child.data['hand']): child for child in root.children}.values())
        top_children = sorted(unique_children, key=lambda x: x.score, reverse=True)[:3]
        root.children = top_children

    return root


if __name__ == '__main__':
    root = build_tree()
    # Main loop to iterate through the tree nodes
    current_nodes = [root]
    level = 0
    while current_nodes:
        print(f"\nLevel {level}:")
        next_nodes = []
        for node in current_nodes:
            print(node)
            next_nodes.extend(node.children)
        current_nodes = next_nodes
        level += 1
