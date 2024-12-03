import random
from player import Player

SUITS = ['H', 'C', 'D', 'S']
VALUES = [str(i) for i in range(1, 15)]
DECK = [f'{val}|{suit}' for val in VALUES for suit in SUITS]

class Game:
    def __init__(self):
        self.players: list[Player] = []
        self.deck = DECK
        random.shuffle(self.deck)
        self.trump_card = self.deck[-1]
        self.trump_suit = self.trump_card.split('|')[1]
        self.active_cards: list[str] = []

    def setup(self):
        for i in range(5):
            self.players.append(Player(self.trump_suit))

        for p in self.players:
            p.draw_cards(6, self.deck)

    def run_turn(self, attacking_player: Player, defending_player: Player):
        a_c = attacking_player.attack()
        self.active_cards.extend(a_c)
        rest_of_players = self.players.copy()
        rest_of_players.remove(attacking_player)
        rest_of_players.remove(defending_player)
        for p in rest_of_players:
            c_cards = p.consolidate(self.active_cards)
            self.active_cards.extend(c_cards)
            a_c.extend(c_cards)
        
        defense = defending_player.defend(a_c)
        while defense:
            type = defense[0]
            def_response = defense[1]
            print(type, def_response)
            if type == 'DEFENSE':
                def_cards = list(def_response.values())
                self.active_cards.extend(def_cards)
                # Loop for other players to consolidate after defense
                for p in rest_of_players:
                    c_cards = p.consolidate(def_cards)
                    self.active_cards.extend(c_cards)
                    def_cards.extend(c_cards)
                # Defending player needs to defend again after consolidation
                defense = defending_player.defend(def_cards)
            elif type == 'PASS ON':
                def_card = list(def_response.values())[0]
                self.active_cards.extend(def_card)
                break
        
        print(self.active_cards)
        

if __name__ == '__main__':
    g = Game()
    g.setup()
    for p in g.players:
        print(p.hand)
    g.run_turn(g.players[0], g.players[1])
    print('-----------------------------')
    for p in g.players:
        print(p.hand)
