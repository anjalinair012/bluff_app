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

    def play_allrank(self, new_round, game_obj):
        max_len = 0
        max_list = 0
        if new_round == 0:
            for i in self.grouped_stash:  # find the rank with maximum cards
                # for j in i:
                #     print(j.rank,j.suit)
                if len(i) > max_len:
                    max_len = len(i)
                    max_list = i
            self.grouped_stash.remove(max_list)
        else:
            for i in self.grouped_stash:
                if game_obj.played_deck[-1][0].rank == i[0].rank:
                    self.grouped_stash.remove(i)
                    max_list = i
        if max_list == 0:
            return 0
        game_obj.played_deck.append(max_list)
        for card in max_list:
            print(self.name + " played " + card.rank + SUIT_SYMBOLS[card.suit])
        while max_list[0] in self.stash:
            self.stash.remove(max_list[0])
        return 1

class CredulousPlayer(Player):
    def __init__(self, name):
        super().__init__(name, character="Credulous")

    def play(self, new_round, game_obj):
        played = self.play_allrank(new_round, game_obj)
        if played == 0:  #card not found, player must pass
            print(self.name + "passed")
            return 0
        else:
            print("End of turn for " + self.name)
            print("\n")
            return 1






