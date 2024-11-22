from itertools import combinations
import copy

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
        if defending_card[1] >= attacking_card[1]:
            return True
    elif defending_card[0] == trump and (attacking_card[0] != trump):
        return True
    else:
        return False

class Turn:
    def __init__(self, attacker: Player, defender: Player, trump: int):
        self.attacker = copy.deepcopy(attacker)
        self.defender = copy.deepcopy(defender)
        self.trump = trump

    def get_attacks(self) -> list[list[tuple[int, int]]]:
        value_to_cards = {}
        # Group cards by their value
        for card in self.attacker.hand:
            value = card[1]
            if value not in value_to_cards:
                value_to_cards[value] = []
            value_to_cards[value].append(card)
        
        valid_attacks = []
        # Generate all possible combinations of cards with the same value
        for cards in value_to_cards.values():
            for i in range(1, len(cards) + 1):
                valid_attacks.extend(list(combinations(cards, i)))
        
        return [list(attack) for attack in valid_attacks]
    
    def get_defenses(self, attacking_cards: list[tuple[int, int]]) -> list[tuple[int, int]] | None:
        defending_cards = []
        for attacking_card in attacking_cards:
            valid_defense_found = False
            for card in self.defender.hand:
                if is_valid_defence(attacking_card, card, self.trump):
                    defending_cards.append(card)
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

# Example usage
initial_attacker = copy.deepcopy(player_1)
initial_defender = copy.deepcopy(player_2)
turn = Turn(initial_attacker, initial_defender, trump=4)
attacks = turn.get_attacks()
for attack in attacks:
    # Create deep copies of players for each branch
    attacker_copy = copy.deepcopy(player_1)
    defender_copy = copy.deepcopy(player_2)
    branch_turn = Turn(attacker_copy, defender_copy, trump=4)
    print(f"Attack: {attack}")
    defenses = branch_turn.get_defenses(attack)
    if defenses:
        print(f"Defense: {defenses}")
    else:
        print("Defense not possible")
    branch_turn.resolve_turn(attack, defenses)
    # Print Player 1 and Player 2 based on the IDs of the branch attackers and defenders
    if branch_turn.attacker.player_id == 1:
        print(f"Player 1: {branch_turn.attacker}")
        print(f"Player 2: {branch_turn.defender}")
    else:
        print(f"Player 1: {branch_turn.defender}")
        print(f"Player 2: {branch_turn.attacker}")
    print("---")
