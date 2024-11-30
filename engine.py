import random
import logging
from consts import DECK, State, SUITS
from player import Player

class Game:
    def __init__(self, num_players: int = 5):
        self.players: list[Player] = [Player(id) for id in range(num_players)]
        self.active_cards: list[tuple[tuple[int, str], str]] = []
        self.current_attacker_index = 0
        self.trump = None
        logging.basicConfig(filename='game_log.log', level=logging.INFO, format='%(asctime)s - %(message)s')

    def setup_game(self):
        self.deck = DECK
        random.shuffle(self.deck)
        self.trump = random.choice(SUITS)

        for player in self.players:
            player.draw_card(6, self.deck)
            player.trump = self.trump

        logging.info(f"Trump suit is: {self.trump}")
        print(f"Trump suit is: {self.trump}")

    def remove_player(self, player: Player):
        if len(player.hand) == 0:
            logging.info(f'Player {player.id} IS OUT')
            print(f'Player {player.id} IS OUT')
            self.players.remove(player)

    def check_game_active(self) -> bool:
        return len([player for player in self.players if len(player.hand) > 0]) > 1

    def run(self):
        while self.check_game_active():
            if len(self.players) == 0:
                break

            attacker = self.players[self.current_attacker_index]
            defender_index = (self.current_attacker_index + 1) % len(self.players)
            defender = self.players[defender_index]

            if len(attacker.hand) == 0:
                self.remove_player(attacker)
                if len(self.players) == 0:
                    break
                self.current_attacker_index = self.current_attacker_index % len(self.players)
                continue

            logging.info(f"\nPlayer {attacker.id} is attacking Player {defender.id}")
            print(f"\nPlayer {attacker.id} is attacking Player {defender.id}")

            # Attacking phase
            self.active_cards.clear()
            for card in attacker.attack(self.trump):
                self.active_cards.append((card, State.OPEN))

            logging.info(f"Attacker {attacker.id} played: {self.active_cards}")

            # Defensive phase
            defending_cards = list(defender.defend(self.active_cards, self.trump))
            if defending_cards:
                logging.info(f"Player {defender.id} successfully defended with: {defending_cards}")
                print(f"Player {defender.id} successfully defended with: {defending_cards}")
                # Update active cards to show defense status
                self.active_cards = [(card, State.DEFENDED) for card, _ in self.active_cards]
            else:
                logging.info(f"Player {defender.id} failed to defend and picks up the cards.")
                print(f"Player {defender.id} failed to defend and picks up the cards.")
                defender.add_cards_to_hand([card for card, _ in self.active_cards])
                self.active_cards.clear()

            if len(self.deck) > 0:
                for player in self.players:
                    if len(player.hand) <  6:
                        num_to_add = 6 - len(player.hand)
                        player.extra_draw_card(num_to_add, self.deck)

            # Remove players with empty hands
            self.remove_player(attacker)
            self.remove_player(defender)

            if len(self.players) == 0:
                break

            # Move to the next attacker
            self.current_attacker_index = (self.current_attacker_index + 1) % len(self.players)

            # Log and print current hands for all players
            for player in self.players:
                logging.info(f"Player {player.id} hand: {player.hand}")
                print(f"Player {player.id} hand: {player.hand}")

        logging.info("\nGame over!")
        print("\nGame over!")
        if len(self.players) == 1:
            logging.info(f"Player {self.players[0].id} is the winner!")
            print(f"Player {self.players[0].id} is the winner!")
        else:
            logging.info("No winner, all players are out of cards.")
            print("No winner, all players are out of cards.")

if __name__ == '__main__':
    game = Game(num_players=5)
    game.setup_game()
    game.run()
