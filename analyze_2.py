import json
from collections import deque

class BranchAnalyzer:
    def __init__(self, branches_file: str):
        with open(branches_file, "r") as f:
            self.branches = json.load(f)

    def get_best_moves(self):
        # Start from the root branches (turn 1)
        root_branch = self._get_root_branch()
        if root_branch is None:
            print("No root branch found.")
            return
        
        self._analyze_branch(root_branch)

    def _get_root_branch(self):
        # Find the branch with turn_number 0 (root)
        for branch_id, branch_data in self.branches.items():
            if branch_data["turn_number"] == 0:
                return branch_data
        return None

    def _analyze_branch(self, branch):
        queue = deque([branch])

        while queue:
            current_branch = queue.popleft()
            
            if not current_branch["children"]:
                # If there are no more children, skip to the next branch in the queue
                continue
            
            # Analyze children branches to find the optimal path for Player 1
            best_child = self._get_best_child(current_branch["children"])
            if best_child is None:
                print("No winning path found from this branch.")
                continue
            
            # Determine who is attacking in the current turn
            attacker_id = current_branch["attacker"]["player_id"]
            turn_number = current_branch["turn_number"]
            if attacker_id == 1:
                # Player 1 is attacking
                cards_played = self._get_cards_played(current_branch, best_child)
                print(f"Turn {turn_number}: Player 1 should play {cards_played} leading to branch {best_child['branch_id']}")
            else:
                # Player 2 is attacking, Player 1 is defending
                print(f"Turn {turn_number}: Player 2 is attacking, Player 1 is defending. Branch ID: {best_child['branch_id']}")
                # Find the best defense move for Player 1
                best_defense = self._get_best_child(best_child["children"])
                if best_defense is not None:
                    cards_played = self._get_cards_played(best_child, best_defense)
                    print(f"Turn {turn_number + 1}: Player 1 should defend with {cards_played} leading to branch {best_defense['branch_id']}")
                    queue.append(best_defense)
            
            # Add the best child to the queue to ensure further exploration
            queue.append(best_child)

    def _get_best_child(self, children_ids: list):
        best_child = None
        best_score = -1

        # Iterate through children and find the best move for Player 1
        for child_id in children_ids:
            child = self.branches[child_id]
            score = self._evaluate_branch(child)
            if score > best_score:
                best_child = child
                best_score = score

        return best_child

    def _get_cards_played(self, parent_branch, child_branch):
        # Determine which cards were played by comparing the hands of Player 1 in the parent and child branches
        parent_hand = parent_branch["attacker"]["hand"] if parent_branch["attacker"]["player_id"] == 1 else parent_branch["defender"]["hand"]
        child_hand = child_branch["attacker"]["hand"] if child_branch["attacker"]["player_id"] == 1 else child_branch["defender"]["hand"]
        
        # Cards played are those that are in the parent's hand but not in the child's hand
        cards_played = [card for card in parent_hand if card not in child_hand]
        return cards_played

    def _evaluate_branch(self, branch):
        # Evaluates a branch based on the likelihood of Player 1 winning
        attacker_id = branch["attacker"]["player_id"]
        defender_id = branch["defender"]["player_id"]
        
        # If Player 1 is the attacker and has no cards, it's a win for Player 1
        if attacker_id == 1 and not branch["attacker"]["hand"]:
            return 100  # Win for Player 1
        # If Player 1 is the defender and has no cards, it's also a win for Player 1
        elif defender_id == 1 and not branch["defender"]["hand"]:
            return 100  # Win for Player 1
        
        # Otherwise, assign a score based on card counts (lower cards is better)
        player_1_cards = len(branch["attacker"]["hand"]) if attacker_id == 1 else len(branch["defender"]["hand"])
        score = 50 - player_1_cards  # The fewer cards Player 1 has, the higher the score

        return score

# Example usage
analyzer = BranchAnalyzer("branches.json")
analyzer.get_best_moves()
