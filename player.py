from attack_logic import find_attacking_cards, find_consolidations
from defense_logic import find_pass_or_defense

class Player:
    def __init__(self, trump: str):
        self.hand: list[str] = []
        self.trump = trump

    def import_hand(self, hand: list[str]):
        self.hand = hand

    def draw_cards(self, num_cards: int, deck: list[str]):
        for i in range(num_cards):
            self.hand.append(deck.pop())

    def attack(self):
        attacking_cards = find_attacking_cards(self.hand, self.trump)
        for card in attacking_cards:
            self.hand.remove(card)
        return attacking_cards
    
    def consolidate(self, active_cards):
        consol_cards = find_consolidations(self.hand, self.trump, active_cards)
        for card in consol_cards:
            self.hand.remove(card)
        return consol_cards
    
    def defend(self, attacking_cards: list[str]):
        type, defense_response = find_pass_or_defense(self.hand, self.trump, attacking_cards)
        defenses = [defense for attack, defense in defense_response.items()]
        if None in defenses:
            self.hand.extend(attacking_cards)
            return
            
        for attack, defense in defense_response.items():
            if isinstance(defense, str):
                self.hand.remove(defense)
            else:
                for card in defense:
                    if card in self.hand:
                        self.hand.remove(card)
        return type, defense_response
    


            


if __name__ == '__main__':
    p = Player('H')
    hand = ['10|H', '7|S', '6|S', '6|D', '13|C', '14|S']
    p.import_hand(hand)