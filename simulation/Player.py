import random
from itertools import groupby
import operator
import numpy as np
from collections import Counter

SYMBOLS = ['♠', '♢', '♡', '♣']
SUIT = ['Hearts', 'Spades', 'Diamonds']
RANK = ['A', '2', '3', '4', '5']
RANK_VALUE = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5}
SUIT_SYMBOLS = {'Hearts': '♡', 'Spades': '♠', 'Diamonds': '♢'}

class Player:
    def __init__(self, name, character=None, bluff_prob=0.0, call_prob=None, belief_model=dict(), announce=list(), trust=dict()):
        self.stash = list()
        self.grouped_stash = None
        self.name = name
        self.character = character
        self.bluff_prob = bluff_prob
        self.call_prob = call_prob
        self.belief_model = belief_model
        self.announce = announce
        self.trust = trust
        self.announcements = []

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
                raise ValueError('ERROR: Player cannot have more than 5 cards during turn')
        except ValueError as err:
            print(err.args)

    def calculate_groupstash(self):
        self.stash.sort(key=operator.attrgetter('rank'))
        self.grouped_stash = [list(v) for k, v in groupby(self.stash, key=operator.attrgetter('rank'))]

    def choose_action(self, reset, prev_agent, announcement):
        # if new round or previous play matches agent's belief, play a card
        if reset == 0 or (not prev_agent.announce):  #new round or no announcement made by prev_agent
            return 1
        if not self.check_belief_model(prev_agent):
            return 2
        else:
            if not self.check_announcement(prev_agent, announcement):
                return 2
            return 1

    def check_announcement(self,prev_agent, announcement):
        announcement_count = Counter(announcement)
        for key,val in announcement_count.items():
            if key == prev_agent.announce[0]:
                if val>3:
                    return False
        return True

    def check_belief_model(self, prev_agent):
        rank = prev_agent.announce[0]
        num = len(prev_agent.announce)
        count_card = 0
        # count the cards of same rank in agents belief system for all agents except prev_agent.
        for key, value in self.belief_model.items():
            if key != prev_agent.name and rank == value[0]:
                count_card = count_card + len(value)
                break
        # if prev_agent has announces more cards than permitted by agent's belief system, call bluff
        if 3 - count_card < num:
            return False
        return True


    def set_belief_model(self, agent,card_known):
        cards_known = list()
        for card in card_known:
            cards_known.append(card)
        if agent.name in self.belief_model.keys():
            self.belief_model.get(agent.name).extend(card_known)
        else:
            self.belief_model.update({agent.name: cards_known})
        # print(self.name)
        # for key,val in self.belief_model.items():
        #     print(str(key)+":"+str(val))



    def call_bluff(self, game_obj, prev_agent):
        self.announcements.append("calls bluff on "+ str(prev_agent.name))
        print("Agent-"+str(self.name)+"calls bluff on Agent-"+str(prev_agent.name))
        cards=list()
        for card in game_obj.played_deck[-1]:
            cards.append(card.rank)
        if prev_agent.announce[0] != cards[-1]:
            print("Bluff caught")
            for i in game_obj.played_deck:
                if i is not None:
                    for j in i:
                        prev_agent.stash.append(j)
            for agent in game_obj.players:
                if agent.name != prev_agent.name:
                    agent.set_belief_model(prev_agent, game_obj.played_deck[-1])
                else:
                    temp=list()
                    for i in game_obj.played_deck:
                        if i is not None:
                            for c in i:
                                temp.append(c)
                    agent.set_belief_model(prev_agent,temp)
            prev_agent.calculate_groupstash()
            return 1
        else:
            for i in game_obj.played_deck:
                for j in i:
                    if j is not None:
                        self.stash.append(j)
            for agent in game_obj.players:
                if agent.name != self.name:
                    agent.set_belief_model(self, game_obj.played_deck[-1])
                else:
                    temp = list()
                    for i in game_obj.played_deck:
                        if i is not None:
                            for c in i:
                                temp.append(c)
                    agent.set_belief_model(self, temp)
            prev_agent.calculate_groupstash()
        return 0


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

    def play_allrank(self, reset, round_card):
        max_len = 0
        max_list = 0
        if reset == 0: #if new round
            for i in self.grouped_stash:  # find the rank with maximum cards
                if len(i) > max_len:
                    max_len = len(i)
                    max_list = i
        else:
            for i in self.grouped_stash:
                if round_card == i[0].rank:
                    max_list = i
                    break
        if max_list == 0:
            return 0
        for card in max_list:
            if (len(max_list) == 1):
                self.announcements.append("played " + str(len(max_list)) + ' ' + card.rank)
            else:
                self.announcements.append("played " + str(len(max_list)) + ' ' + card.rank + 's')
        return max_list


    def play_bluff(self, reset, round_card):

        if reset == 0:
            
            max_len = 0
            max_list = 0

            for i in self.grouped_stash:
                if len(i) > max_len:
                    max_len = len(i)
                    max_list = i

            if (max_len > 1):

                bluff_choice_list = [x for i, x in enumerate(self.stash) if x.rank != max_list[0].rank]

                if len(bluff_choice_list) == 0:
                    self.announce = max_list[0].rank
                    return max_list
                player_bluff_card = random.choice(bluff_choice_list)
                self.announce = max_list[0].rank

                return [player_bluff_card]

            else:

                player_bluff_card = random.choice(self.stash)
                announcement_choice_list = [x for i, x in enumerate(self.stash) if x.rank != player_bluff_card.rank]

                if len(announcement_choice_list) == 0:
                    self.announce = player_bluff_card.rank
                    return [player_bluff_card]
                self.announce = (random.choice(announcement_choice_list)).rank

                return [player_bluff_card]
        else:

            bluff_choice_list = [x for i, x in enumerate(self.stash) if x.rank != round_card]

            if (len(bluff_choice_list) == 0):
                return self.stash

            player_bluff_card = random.choice(bluff_choice_list)
            return [player_bluff_card]


class CredulousPlayer(Player):
    def __init__(self, name):
        super().__init__(name, character="Credulous")

    def play(self, reset, game_obj, round_card):
        played = self.play_allrank(reset, round_card)  #play true, all cards of a rank in player's stash
        if type(played) is int:  #card not found, player must pass
            self.announcements.append("pass")
            print(self.name + "passed")
            return 0
        else:
            self.announce = [played[0].rank]*len(played)
            print("End of turn for " + self.name)
            print("\n")
            return played



    # def check_belief_model(self):

class SkepticalPlayer(Player):
    def __init__(self, name):
        super().__init__(name, character="Skeptical", bluff_prob=0.5)

    def choose_action(self, reset, prev_agent, announcement):

        # if new round or previous play matches agent's belief, play a card
        if reset == 0 or (not prev_agent.announce):  # new round or no announcement made by prev_agent
            return 1
        if not self.check_belief_model(prev_agent):
            return 2
        else:
            return 1

    def play(self, reset, game_obj, round_card):
        player_bluff_probability = np.random.choice([0, 1], p = [self.bluff_prob, (1 - self.bluff_prob)])
        if player_bluff_probability == 0: #bluff_probability < 0.5, player doesnt bluff
            played = self.play_allrank(reset, round_card)
            if type(played) is int:
                self.announcements.append("pass")
                print(self.name + "passed")
                return 0
            else:
                self.announce = [played[0].rank]*len(played)
                print("End of turn for " + self.name)
                print("\n")
                return played
        else:
            #print (player_bluff_card[0].rank, player_bluff_card[0].suit)

            if round_card is None:
                player_bluff_card = self.play_bluff(reset, None)
                self.announcements.append(" announced " + self.announce + " and played " + player_bluff_card[0].rank)
                print (self.name + " announced " + self.announce + " and played " + player_bluff_card[0].rank)
                print ("End of turn for " + self.name)
                print ("\n")

                return player_bluff_card

            else:
                player_bluff_card = self.play_bluff(reset, round_card)
                self.announce = round_card #playing the bluff card and announcing it as a real card
                self.announcements.append(" announced " + self.announce + " and played " + player_bluff_card[0].rank)
                print (self.name + " announced " + self.announce + " and played " + player_bluff_card[0].rank)
                print ("End of turn for " + self.name)
                print ("\n")
                return player_bluff_card


class RevisingPlayer(Player):
    def __init__(self, name):
        trust = dict()
        for num in range(1, 4):
            player_name = "Player_"+str(num)
            if player_name != name:
                trust[player_name] = 0.5
        super().__init__(name, character="Revising", bluff_prob=0.5, trust=trust)

    def play(self, reset, game_obj, round_card):
        player_bluff_probability = np.random.choice([0, 1], p=[self.bluff_prob, (1 - self.bluff_prob)])
        if player_bluff_probability == 0:  # bluff_probability < 0.5, player doesnt bluff
            played = self.play_allrank(reset, round_card)
            if type(played) is int:
                self.announcements.append("passed")
                print(self.name + "passed")
                return 0
            else:
                self.announce = [played[0].rank] * len(played)
                print("End of turn for " + self.name)
                print("\n")
                return played
        else:
            # print (player_bluff_card[0].rank, player_bluff_card[0].suit)

            if round_card is None:
                player_bluff_card = self.play_bluff(reset, None)
                print(self.name + " announced " + self.announce + " and played " + player_bluff_card[0].rank)
                print("End of turn for " + self.name)
                print("\n")

                return player_bluff_card

            else:
                player_bluff_card = self.play_bluff(reset, round_card)
                self.announce = round_card  # playing the bluff card and announcing it as a real card
                print(self.name + " announced " + self.announce + " and played " + player_bluff_card[0].rank)
                self.announcements.append("announced " + self.announce + " and played " + player_bluff_card[0].rank)
                print("End of turn for " + self.name)
                print("\n")
                return player_bluff_card

    def choose_action(self, reset, prev_agent, announcement):
        # if new round or previous play matches agent's belief, play a card
        if reset == 0 or (not prev_agent.announce):  # new round or no announcement made by prev_agent
            return 1
        if not self.check_belief_model(prev_agent):
            return 2
        else:
            if random.random()>self.trust[prev_agent.name]:
                return 2
            return 1

    def call_bluff(self, game_obj, prev_agent):
        bluff = super().call_bluff(game_obj, prev_agent)
        if bluff == 1:
            self.trust[prev_agent] = self.trust[prev_agent.name]-self.trust[prev_agent.name]/3
        else:
            self.trust[prev_agent] = self.trust[prev_agent.name] + self.trust[prev_agent.name]/3