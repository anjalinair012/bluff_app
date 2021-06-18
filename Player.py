import random
from itertools import groupby
import operator

SYMBOLS = ['♠', '♢', '♡', '♣']
SUIT = ['Hearts', 'Spades', 'Diamonds']
RANK = ['A', '2', '3', '4', '5']
RANK_VALUE = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5}
SUIT_SYMBOLS = {'Hearts': '♡', 'Spades': '♠', 'Diamonds': '♢'}

class Player:
    def __init__(self, name, character="None", turn="None", bluff_prob="None", call_prob="None", belief_model="None"):
        self.stash = list()
        self.grouped_stash = None
        self.name = name
        self.character = character
        self.turn = turn
        self.bluff_prob = bluff_prob
        self.call_prob = call_prob
        self.belief_model = belief_model

    def set_bluff_prob(self, bluff_prob):
        self.bluff_prob = bluff_prob

    def set_call_prob(self, call_prob):
        self.call_prob = call_prob

    def addTo_hand(self, card):
        try:
            self.stash.append(card)
            if len(self.stash) == 5:
                self.stash.sort(key=operator.attrgetter('rank'))
                self.grouped_stash = [list(v) for k, v in groupby(self.stash, key=operator.attrgetter('rank'))]
                # self.stash.sort(key=operator.attrgetter('rank'))
            if len(self.stash) > 5:
                raise ValueError('ERROR: Player cannot have more than 14 cards during turn')
        except ValueError as err:
            print(err.args)



    def removeFrom_hand(self, card):
        self.stash.remove(card)

    def play_Player(self, previous_card):
        random_card = random.choice(self.stash)
        print(self.name + " played " + random_card.rank + SUIT_SYMBOLS[random_card.suit])
        self.stash.remove(random_card)

        if (len(self.stash) == 0):
            return True
        else:
            return False

class CredulousPlayer(Player):
    def __init__(self, name):
        super().__init__(name, character="Credulous")

    def play(self, new_round, game_obj):
        is_rank = False
        if new_round is None:  # a new round start with random card
            lastcard = random.choice(self.stash)
            print(self.name + " played " + lastcard.rank + SUIT_SYMBOLS[lastcard.suit])
            self.stash.remove(lastcard)
            game_obj.played_deck.append(lastcard)
            is_rank = True
        else:   #play depending on previous card
            for c in self.stash:
                if game_obj.played_deck[-1].rank == c.rank:
                    is_rank = True
                    print(self.name + " played " + c.rank + SUIT_SYMBOLS[c.suit])
                    self.stash.remove(c)
                    game_obj.played_deck.append(c)
        if is_rank is False:
            print(self.name + "passed")
            return 0
        else:
            print("End of turn for " + self.name)
            print("\n")
            return 1






