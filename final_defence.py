from itertools import combinations
import copy
import json
import uuid

class Player:
    def __init__(self, player_id: int, hand: list[tuple[int, int]], role: str):
        self.player_id = player_id
        self.hand = hand
        self.role = role

    def __str__(self):
        return f"Player(id={self.player_id}, role={self.role}, hand={self.hand})"

player_1 = Player(1, [(1, 4), (2, 4), (3, 4), (4, 4), (4, 10), (2, 11), (3, 13)], role="attacking")
player_2 = Player(2, [(3, 14)], role="defending")

def is_valid_defence(attacking_card: tuple[int, int], defending_card: tuple[int, int], trump: int) -> bool:
    if defending_card[0] == attacking_card[0]:
        if defending_card[1] > attacking_card[1]:  # Changed to strictly greater than
            return True
    elif defending_card[0] == trump and (attacking_card[0] != trump):
        return True
    else:
        return False

class Turn:
    def __init__(self, attacker: Player, defender: Player, trump: int, parent=None, turn_number=0):
        self.attacker = copy.deepcopy(attacker)
        self.defender = copy.deepcopy(defender)
        self.trump = trump
        self.parent = parent
        self.children = []
        self.branch_id = str(uuid.uuid4())
        self.turn_number = turn_number

    def get_attacks(self) -> list[list[tuple[int, int]]]:
        # Separate non-trump and trump cards, prioritize non-trump cards unless forced to use trump
        non_trump_cards = [card for card in self.attacker.hand if card[0] != self.trump]
        trump_cards = [card for card in self.attacker.hand if card[0] == self.trump]
        
        value_to_cards = {}
        # Group non-trump cards by their value
        for card in non_trump_cards:
            value = card[1]
            if value not in value_to_cards:
                value_to_cards[value] = []
            value_to_cards[value].append(card)
        
        valid_attacks = []
        # Generate all possible combinations of non-trump cards with the same value
        for cards in value_to_cards.values():
            for i in range(1, len(cards) + 1):
                valid_attacks.extend(list(combinations(cards, i)))
        
        # Generate all possible combinations of trump cards with the same value if needed
                for i in range(1, len(cards) + 1):
                    valid_attacks.extend(list(combinations(cards, i)))
        
        return [list(attack) for attack in valid_attacks]
    
    def get_defenses(self, attacking_cards: list[tuple[int, int]]) -> list[tuple[int, int]] | None:
        used_defending_cards = set()
        defending_cards = []
        for attacking_card in attacking_cards:
            valid_defense_found = False
            for card in self.defender.hand:
                if card not in used_defending_cards and is_valid_defence(attacking_card, card, self.trump):
                    defending_cards.append(card)
                    used_defending_cards.add(card)
                    valid_defense_found = True
                    break
            if not valid_defense_found:
                return None
        return defending_cards

    def resolve_turn(self, attack: list[tuple[int, int]], defense: list[tuple[int, int]] | None):
        if defense:
            # Remove the defending cards from the defender's hand
            self.defender.hand = [card for card in self.defender.hand if card not in defense]
            # Remove the attacking cards from the attacker's hand
            self.attacker.hand = [card for card in self.attacker.hand if card not in attack]
            # Swap roles
            self.attacker.role, self.defender.role = "defending", "attacking"
            self.attacker, self.defender = self.defender, self.attacker
        else:
            # If defense is not possible, add the attacking cards to the defender's hand
            self.defender.hand.extend(attack)
            # Remove the attacking cards from the attacker's hand
            self.attacker.hand = [card for card in self.attacker.hand if card not in attack]

    def process_next_branch(self, all_branches: dict):
        # Stop processing if either player has no cards left
        if (self.attacker.player_id == 1 and not self.attacker.hand) or (self.defender.player_id == 1 and not self.defender.hand):
            print("Player 1 wins. Game over.")
            # Add branch to collection if Player 1 wins
            all_branches[self.branch_id] = self.to_dict()
            return
        elif (self.attacker.player_id == 2 and not self.attacker.hand) or (self.defender.player_id == 2 and not self.defender.hand):
            print("Player 2 wins. Branch pruned.")
            return
        
        # Add the current branch to the collection
        all_branches[self.branch_id] = self.to_dict()
        
        # Add the current branch to the collection
        all_branches[self.branch_id] = self.to_dict()
        
        attacks = self.get_attacks()
        for attack in attacks:
            # Create deep copies of players for each branch
            attacker_copy = copy.deepcopy(self.attacker)
            defender_copy = copy.deepcopy(self.defender)
            branch_turn = Turn(attacker_copy, defender_copy, self.trump, parent=self, turn_number=self.turn_number + 1)
            print(f"Attack: {attack}")
            defenses = branch_turn.get_defenses(attack)
            if defenses:
                print(f"Defense: {defenses}")
            else:
                print("Defense not possible")
            branch_turn.resolve_turn(attack, defenses)
            # Store only the branch ID of the child instead of the full child
            if branch_turn.attacker.hand and branch_turn.defender.hand:
                self.children.append(branch_turn.branch_id)
                # Add the child branch to the collection
                all_branches[branch_turn.branch_id] = branch_turn.to_dict()
                # Print Player 1 and Player 2 based on the IDs of the branch attackers and defenders
                if branch_turn.attacker.player_id == 1:
                    print(f"Player 1: {branch_turn.attacker}")
                    print(f"Player 2: {branch_turn.defender}")
                else:
                    print(f"Player 1: {branch_turn.defender}")
                    print(f"Player 2: {branch_turn.attacker}")
                print("---")
                # Recursively process the next branches
                branch_turn.process_next_branch(all_branches)

    def to_dict(self):
        return {
            "branch_id": self.branch_id,
            "turn_number": self.turn_number,
            "attacker": {
                "player_id": self.attacker.player_id,
                "hand": self.attacker.hand,
                "role": self.attacker.role
            },
            "defender": {
                "player_id": self.defender.player_id,
                "hand": self.defender.hand,
                "role": self.defender.role
            },
            "children": self.children  # Store only the branch IDs of the children
        }

# Example usage
initial_attacker = copy.deepcopy(player_1)
initial_defender = copy.deepcopy(player_2)
turn = Turn(initial_attacker, initial_defender, trump=4)
all_branches = {}
turn.process_next_branch(all_branches)

# Save the branches to a JSON file
with open("branches.json", "w") as f:
    json.dump(all_branches, f, indent=2)
