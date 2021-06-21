import random
from itertools import groupby
import operator

SYMBOLS = ['♠', '♢', '♡', '♣']
SUIT = ['Hearts', 'Spades', 'Diamonds']
RANK = ['A', '2', '3', '4', '5']
RANK_VALUE = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5}
SUIT_SYMBOLS = {'Hearts': '♡', 'Spades': '♠', 'Diamonds': '♢'}

class Player:
    def __init__(self, name, character=None, bluff_prob=0, call_prob=None, belief_model=dict(), announce=list()):
        self.stash = list()
        self.grouped_stash = None
        self.name = name
        self.character = character
        self.bluff_prob = bluff_prob
        self.call_prob = call_prob
        self.belief_model = belief_model
        self.announce = announce

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

    def choose_action(self, reset, prev_agent):
        # if new round or previous play matches agent's belief, play a card
        if reset == 0:
            return 1
        check = self.check_belief_model(prev_agent)
        if check is True:
            return 1
        # call bluff
        return 2

    def check_belief_model(self, prev_agent):
        rank = prev_agent.announce[0]
        num = len(prev_agent.announce)
        count_card = 0
        # count the cards of same rank in agents belief system for all agents except prev_agent.
        for key, value in self.belief_model.items():
            if key != prev_agent.name and rank == value[0]:
                count_card = len(value)
                break
        # if prev_agent has announces more cards than permitted by agent's belief system, call bluff
        if 3 - count_card > num:
            return False
        return True


    def set_belief_model(self, agent):
        card_known = list()
        for card in agent.stash:
            card_known.append(card.rank)
        if agent.name in self.belief_model.keys():
            self.belief_model.get(agent.name).append(card_known)
        else:
            self.belief_model.update({agent.name: card_known})


    def call_bluff(self, game_obj, prev_agent):
        if prev_agent.announce != game_obj.played_deck[-1]:
            print("Bluff caught")
            for agent in game_obj.players:
                agent.set_belief_model()
        print()


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
        if new_round == 0: #if new round
            for i in self.grouped_stash:  # find the rank with maximum cards
                if len(i) > max_len:
                    max_len = len(i)
                    max_list = i
        else:
            for i in self.grouped_stash:
                if game_obj.played_deck[-1][0].rank == i[0].rank:
                    max_list = i
                    break
        if max_list == 0:
            return 0
        self.grouped_stash.remove(max_list)
        game_obj.played_deck.append(max_list)
        for card in max_list:
            print(self.name + " played " + card.rank + SUIT_SYMBOLS[card.suit])
        for card in max_list:
            self.stash.remove(card)
        return max_list

class CredulousPlayer(Player):
    def __init__(self, name):
        super().__init__(name, character="Credulous")

    def play(self, round, game_obj):
        played = self.play_allrank(round, game_obj)
        if type(played) is int:  #card not found, player must pass
            print(self.name + "passed")
            return 0
        else:
            self.announce = [played[0].rank]*len(played)
            print("End of turn for " + self.name)
            print("\n")
            return 1



    # def check_belief_model(self):








