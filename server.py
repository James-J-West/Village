import socket
import threading
import random

# Server settings
HOST = '127.0.0.1'
PORT = 12345

# Game state
players = {}
player_order = []
hands = {}
turn_index = 0
game_running = True

# Sample deck
DECK = [f"C{i}" for i in range(1, 37)]  # Example: Cards C1 to C36

def deal_cards():
    """Distribute cards to players."""
    random.shuffle(DECK)
    return {player: DECK[i * 6:(i + 1) * 6] for i, player in enumerate(player_order)}

def broadcast(message):
    """Send a message to all players."""
    for conn in players.values():
        conn.sendall(message.encode())

def handle_player(conn, addr, player_id):
    """Handle player actions."""
    global turn_index, game_running

    conn.sendall(f"Welcome {player_id}! Waiting for all players...\n".encode())

    while game_running:
        # Check if it's the player's turn
        if player_order[turn_index] == player_id:
            conn.sendall(f"It's your turn! Your hand: {', '.join(hands[player_id])}\n".encode())
            conn.sendall("Enter your command (e.g., attack <CardID>):\n".encode())
            command = conn.recv(1024).decode().strip()
            if not command:
                continue

            # Parse the command
            parts = command.split()
            if len(parts) == 2 and parts[0].lower() == "attack":
                card = parts[1]
                if card in hands[player_id]:
                    attacked_player = player_order[(turn_index + 1) % len(player_order)]
                    hands[player_id].remove(card)
                    broadcast(f"{player_id} attacks {attacked_player} with {card}!\n")

                    # Notify the defender
                    players[attacked_player].sendall(
                        f"You are being attacked with {card}! Your hand: {', '.join(hands[attacked_player])}\n".encode()
                    )
                    players[attacked_player].sendall("Enter your command (e.g., defend <CardID>):\n".encode())

                    # Wait for defender response
                    defend_command = players[attacked_player].recv(1024).decode().strip()
                    defend_parts = defend_command.split()
                    if len(defend_parts) == 2 and defend_parts[0].lower() == "defend":
                        defend_card = defend_parts[1]
                        if defend_card in hands[attacked_player]:
                            hands[attacked_player].remove(defend_card)
                            broadcast(f"{attacked_player} defends with {defend_card}!\n")
                        else:
                            broadcast(f"{attacked_player} failed to defend! {attacked_player} takes the card.\n")
                            hands[attacked_player].append(card)
                    else:
                        broadcast(f"{attacked_player} failed to defend! {attacked_player} takes the card.\n")
                        hands[attacked_player].append(card)

                    # Move to the next turn
                    turn_index = (turn_index + 1) % len(player_order)
                else:
                    conn.sendall(f"You don't have {card} in your hand. Try again.\n".encode())
            else:
                conn.sendall("Invalid command. Try again.\n".encode())
        else:
            conn.sendall("Wait for your turn...\n".encode())

    conn.sendall("Game has ended. Disconnecting...\n".encode())
    conn.close()

def start_server():
    """Starts the game engine."""
    global game_running, hands

    print("Starting the game engine...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(5)
        print("Server is listening for players...")

        # Accept up to 5 players
        while len(players) < 5:
            conn, addr = server.accept()
            player_id = f"Player-{len(players) + 1}"
            players[player_id] = conn
            player_order.append(player_id)
            print(f"{player_id} connected from {addr}")

        print("All players connected! Dealing cards and starting the game.")
        hands = deal_cards()
        broadcast("All players connected! Let the game begin.\n")

        # Start game threads
        for player_id, conn in players.items():
            threading.Thread(target=handle_player, args=(conn, None, player_id)).start()

        # Wait until the game ends
        while game_running:
            pass

        print("Shutting down the server.")


if __name__ == "__main__":
    start_server()
