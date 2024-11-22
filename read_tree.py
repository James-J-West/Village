import json
import igraph as ig
import matplotlib.pyplot as plt

def load_branches(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        return json.load(f)

def build_graph(branches: dict, root_id: str) -> ig.Graph:
    g = ig.Graph(directed=True)
    node_indices = {}
    
    # Add root node
    root_index = g.add_vertex(name=root_id, label=f"Turn {branches[root_id]['turn_number']}").index
    node_indices[root_id] = root_index
    queue = [root_id]
    
    while queue:
        branch_id = queue.pop(0)
        branch = branches.get(branch_id, None)
        
        if branch is None:
            continue
        
        # Add edges for children
        for child_id in branch.get('children', []):
            if child_id not in node_indices:
                child_index = g.add_vertex(name=child_id, label=f"Turn {branches[child_id]['turn_number']}").index
                node_indices[child_id] = child_index
            else:
                child_index = node_indices[child_id]
            
            g.add_edge(node_indices[branch_id], child_index)
            queue.append(child_id)
    
    return g

def display_graph(g: ig.Graph):
    layout = g.layout_reingold_tilford(root=[0])
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Extract turn numbers for y-axis labeling
    turn_numbers = [int(v['label'].split()[-1]) for v in g.vs]
    max_turn = max(turn_numbers)
    
    ig.plot(
        g,
        target=ax,
        layout=layout,
        vertex_label=None,  # No labels on nodes
        vertex_size=20,
        vertex_color='lightblue',
        edge_arrow_size=0.5,
        bbox=(800, 600),
        margin=40
    )
    
    # Add y-axis ticks for turn numbers
    ax.set_yticks(range(max_turn + 1))
    ax.set_yticklabels([f"Turn {i}" for i in range(max_turn + 1)])
    ax.invert_yaxis()  # Invert y-axis to make turns go top-down
    
    plt.title("Game Tree Visualization")
    plt.show()

def main():
    # Load the branches from the JSON file
    branches = load_branches('branches.json')
    
    # Assuming the first branch in the dictionary is the root
    root_id = next(iter(branches))
    
    # Build the graph
    g = build_graph(branches, root_id)
    
    # Display the graph
    display_graph(g)

if __name__ == "__main__":
    main()
