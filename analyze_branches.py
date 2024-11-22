import json

with open('branches.json', 'r') as file:
    data = json.load(file)
winning_nodes = 0
for node in data:
    node_data = data[node]
    if node_data['attacker']['player_id'] == 1:
        player_data = node_data['attacker']
        opp_Data = node_data['defender']
        if len(player_data['hand']) == 1:
            winning_nodes += 1

    if node_data['defender']['player_id'] == 1:
        player_data = node_data['defender']
        opp_Data = node_data['attacker']
        if len(player_data['hand']) == 1 and len(opp_Data['hand']) != 1:
            winning_nodes += 1

 

print(f'Player 1 won {winning_nodes} out of {len(data)}')
