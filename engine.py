import random
from consts import DECK, State, SUITS
from player import Player

class Game:
    def __init__(self, num_players: int = 5):

        self.players: list[Player] = []
        for id in range(num_players):
            self.players.append(Player(id))

        

        self.active_cards: list[tuple[tuple[int, str], str]] = []


    def setup_game(self):
        self.deck = DECK
        random.shuffle(self.deck)
        self.trump = random.choice(SUITS)

        for player in self.players:
            player.draw_card(6, self.deck)
            player.trump = self.trump

    def remove_player(self, player:Player):
        if len(player.hand) == 0:
            print(f'Player {player.id} IS OUT')
            self.players.remove(player)

    def check_game_active(self) -> bool:
        non_empty_hands = []
        for player in self.players:
            if len(player.hand) != 0:
                non_empty_hands.append(player)

        if len(non_empty_hands) > 1:
            return True
        return False

    def run(self):
        while self.check_game_active():
            for index, attacking_player in enumerate(self.players):
                consolidation_players = self.players.copy()
                consolidation_players.remove(attacking_player)
                consolidation_players.remove(self.players[index+1])

                for card in attacking_player.attack():
                     self.active_cards.append((card, State.OPEN))


                for cons_player in consolidation_players:
                    if cons_player.decide_consolidation(self.active_cards):
                        for card in cons_player.decide_consolidation(self.active_cards):
                            self.active_cards.append((card, State.OPEN))
                
                defending_player = self.players[index + 1]

                if defending_player.defend():
                    new_active: list[tuple[tuple[int, str], str]] = []
                    for card, state in self.active_cards:
                        new_active.append((card, State.DEFENDED))
                    for card in defending_player.defend(self.active_cards):
                        new_active.append((card, State.DEFENDED_OPEN))

                
                    






    

if __name__ == '__main__':
    game = Game(num_players=5)

    game.setup_game()






        
