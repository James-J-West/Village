import json
import matplotlib.pyplot as plt
import networkx as nx

def load_tree(filename):
    with open(filename, 'r') as json_file:
        return json.load(json_file)

def add_edges(graph, node, parent=None):
    # Always add the current node to the graph
    node_id = id(node)
    graph.add_node(node_id, result=node.get('result', None))

    if parent is not None:
        graph.add_edge(parent, node_id)

    # Recursively add all children nodes
    for child in node['children']:
        add_edges(graph, child, node_id)

def hierarchical_layout(graph, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    pos = _hierarchical_layout(graph, root, width, vert_gap, vert_loc, xcenter)
    return pos

def _hierarchical_layout(graph, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None, parsed=[]):
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    children = list(graph.successors(root))
    if not isinstance(graph, nx.DiGraph):
        raise TypeError("cannot use hierarchy_pos on a non-directed graph")
    if not nx.is_tree(graph):
        raise TypeError("cannot use hierarchy_pos on a graph that is not a tree")
    if root not in parsed:
        parsed.append(root)
        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width / 2 - dx / 2
            for child in children:
                nextx += dx
                pos = _hierarchical_layout(graph, child, width=dx, vert_gap=vert_gap,
                                          vert_loc=vert_loc - vert_gap, xcenter=nextx,
                                          pos=pos, parent=root, parsed=parsed)
    return pos

def plot_tree(tree_data):
    graph = nx.DiGraph()
    add_edges(graph, tree_data)

    if len(graph) == 0:
        print("The graph is empty. No nodes to display.")
        return

    root_candidates = [n for n, d in graph.in_degree() if d == 0]
    if not root_candidates:
        print("No root node found in the graph.")
        return

    root = root_candidates[0]  # Find root node
    pos = hierarchical_layout(graph, root=root, width=2.0, vert_gap=0.5)  # Use hierarchical layout for top-to-bottom visualization

    plt.figure(figsize=(15, 10))
    colors = ["green" if graph.nodes[node].get('result') == 'PLAYER 1 WON!' else "red" if graph.nodes[node].get('result') == 'PLAYER 2 WON!' else "gray" for node in graph.nodes]
    nx.draw(graph, pos, with_labels=False, node_size=1000, node_color=colors, edge_color='black', linewidths=1, arrows=False)
    plt.show()

# Load the tree from the JSON file
tree_data = load_tree('game_tree.json')

# Plot the tree
plot_tree(tree_data)
