import json
from collections import deque

with open('game_tree.json', 'r') as f:
    data = json.load(f)

def find_lowest_depth_player1_win_simplified(node):
    """
    Finds the "Player 1 WIN" result at the lowest depth using BFS and
    returns the simplified path (excluding 'children') from the root to the winning node.

    Args:
        node (dict): The root node of the game tree.

    Returns:
        list or None: A list of simplified nodes from the root to the winning node, or None if no win exists.
    """
    # Queue to store nodes and their paths
    queue = deque([(node, [])])  # Each element is (current_node, path_to_current_node)

    while queue:
        current_node, path = queue.popleft()

        # Simplify the current node by excluding 'children'
        simplified_node = {k: v for k, v in current_node.items() if k != "children"}
        current_path = path + [simplified_node]

        # Check if this node is a "Player 1 WIN"
        if current_node.get("result") == "PLAYER 1 WON!":
            return current_path

        # Add children to the queue
        for child in current_node.get("children", []):
            queue.append((child, current_path))

    # No win found
    return None

lowest_depth_win_path = find_lowest_depth_player1_win_simplified(data)

if lowest_depth_win_path:
    print("Path to the lowest depth Player 1 WIN (simplified):")
    for i, node in enumerate(lowest_depth_win_path):
        print(f"Step {i+1}:")
        print(json.dumps(node, indent=4))
else:
    print("No Player 1 WIN found.")