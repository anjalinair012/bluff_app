import random
from itertools import groupby
import operator
import numpy as np

SYMBOLS = ['♠', '♢', '♡', '♣']
SUIT = ['Hearts', 'Spades', 'Diamonds']
RANK = ['A', '2', '3', '4', '5']
RANK_VALUE = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5}
SUIT_SYMBOLS = {'Hearts': '♡', 'Spades': '♠', 'Diamonds': '♢'}

class Player:
    def __init__(self, name, character=None, bluff_prob=0.0, call_prob=None, trust=None, belief_model=dict(), announce=list()):
        self.stash = list()
        self.grouped_stash = None
        self.name = name
        self.character = character
        self.bluff_prob = bluff_prob
        self.call_prob = call_prob
        self.belief_model = belief_model
        self.trust = trust
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
                raise ValueError('ERROR: Player cannot have more than 5 cards during turn')
        except ValueError as err:
            print(err.args)

    def calculate_groupstash(self):
        self.stash.sort(key=operator.attrgetter('rank'))
        self.grouped_stash = [list(v) for k, v in groupby(self.stash, key=operator.attrgetter('rank'))]

    def choose_action(self, reset, prev_agent, game_obj, announcemet):
        # if new round or previous play matches agent's belief, play a card
        if reset == 0 or (not prev_agent.announce):  #new round or no announcement made by prev_agent
            return 1
        #call bluff based on trust
        if self.trust is not None:
            call_prob = random.random()
            if call_prob > self.trust[prev_agent.name]:
                return 0
        if self.character == "Credulous":
            if self.cred_check_model( prev_agent, game_obj,announcemet) == 1:
               return 1
            else:
               return 0

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
            if key == prev_agent.name:
                continue
            for card in value:
                if rank == card:
                    count_card = count_card + 1
        # if prev_agent has announces more cards than permitted by agent's belief system, call bluff
        if 3 - count_card < num:
            return False
        return True

    def set_belief_model(self, agent, card_known):
        #cards in hand updated
        cards_known = list()
        for card in card_known:
            cards_known.append(card)
        if agent in self.belief_model.keys():
            self.belief_model.get(agent.name).append(cards_known)
        else:
            self.belief_model.update({agent.name: cards_known})


    def print_belief(self):
        print("hey")
        for key,value in self.belief_model.items():
            print(key)
            for val in value:
                print(val)


    def call_bluff(self, game_obj, prev_agent, round_starter, announcement):
        print("Agent-"+str(self.name)+"calls bluff on Agent-"+str(prev_agent.name))
        if prev_agent.announce != game_obj.played_deck[-1]:
            print("Bluff caught")
            for agent in game_obj.players:
                agent.set_belief_model(prev_agent, game_obj.played_deck[-1])  #update with opened cards
                card_count = 0
                i = round_starter
                k=0
                if agent.character == "Credulous":
                    while True:
                        for pl in game_obj.players:
                            card_count = card_count + self.belief_model[pl].count(prev_agent.announce[0])
                        if card_count>3:
                            break
                        if game_obj.played_deck[k] is not None:
                            extra_cards = len(game_obj.played_deck[k]) - self.belief_model["Player"+str(i)]
                            if extra_cards>0 and extra_cards + card_count <=3:
                                self.set_belief_model(prev_agent,[prev_agent.announce[0]]*extra_cards)
                            else:
                                break
                        k+=1
                        i+=1

                else:
                    agent.agent_played(prev_agent, game_obj)
            game_obj.played_deck = []
            return 1
        else:
            print("False Bluff Called")
            for agent in game_obj.players:
                agent.set_belief_model(self, game_obj.played_deck[-1])  # update with opened cards
                agent_count = 0
                if agent.character == "Credulous":
                    for key, val in agent.belief_model.items():
                        agent_count = agent_count + val.count(prev_agent.announce[0])
                    cards_rem = 3 - agent_count
                    temp = list()
                    for cards in game_obj.played_deck:
                        if cards is not None:
                            if len(temp) >= cards_rem:
                                break
                            temp.append(prev_agent.announce[0])
                    agent.set_belief_model(self, temp)
                else:
                    agent.agent_played(self, game_obj)
            game_obj.played_deck = []
            return 0



    def removeFrom_hand(self, card):
        self.stash.remove(card)

    # def play_Player(self, previous_card):
    #     random_card = random.choice(self.stash)
    #     print(self.name + " played " + random_card.rank + SUIT_SYMBOLS[random_card.suit])
    #     self.stash.remove(random_card)
    #
    #     if (len(self.stash) == 0):
    #         return True
    #     else:
    #         return False

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
            print(self.name + " played " + card.rank + SUIT_SYMBOLS[card.suit])
        return max_list

    def play_bluff(self, reset, round_card):
        if reset == 0:
            max_len = 0
            max_list = 0
            for i in self.grouped_stash:  #Bluff for the rank agent has high
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

    def agent_played(self, prev_agent, game_obj):
        prev_agent_num = int(prev_agent.name[-1])
        agent_num = int(self.name[-1])
        agent_index = prev_agent_num - agent_num
        if agent_index < 0:
            agent_index = 3 + agent_index
        while abs(agent_index)<len(game_obj.played_deck):
            self.set_belief_model(prev_agent, game_obj.played_deck[agent_index])
            agent_index = agent_index - 3
        return


class CredulousPlayer(Player):
    def __init__(self, name):
        super().__init__(name, character="Credulous")

    def play(self, reset, game_obj, round_card):
        played = self.play_allrank(reset, round_card)  #play true, all cards of a rank in player's stash
        if type(played) is int:  #card not found, player must pass
            print(self.name + "passed")
            return None
        else:
            self.announce = [played[0].rank]*len(played)
            # for player in game_obj.players:   #all player's belief system updated with card played by active player
            #     if player.name != self.name and player.character == "Credulous":
            #         player.set_belief_model(self, self.announce)
            print("End of turn for " + self.name)
            print("\n")
            return played

    def cred_check_model(self, prev_agent, game_obj, announcement):
        count_cards = 0
        for agent in game_obj.players:
            if agent.name == prev_agent.name:
                continue
            count_cards = count_cards + len(max(self.belief_model[agent.name],announcement[int(agent.name[-1])-1]))
            if count_cards > len(announcement[int(prev_agent.name[-1])-1]) or len(announcement[int(prev_agent.name[-1])-1])>3:
                return 0
            else:
                return 1


class SkepticalPlayer(Player):
    def __init__(self, name):
        super().__init__(name, character="Skeptical", bluff_prob=0.5)

    def play(self, reset, game_obj, round_card):
        prob = random.random()
        if prob > self.bluff_prob: #less than bluff_prob, player doesnt bluff
            played = self.play_allrank(reset, round_card)
            if type(played) is int:
                print(self.name + "passed")
                return None
            else:
                self.announce = [played[0].rank]*len(played)
                # for player in game_obj.players:
                #     if player.name != self.name and player.character == "Credulous":
                #         player.set_belief_model(self, self.announce)
                print("End of turn for " + self.name)
                print("\n")
                return played

        else:  #a bluff play
            
            #print (player_bluff_card[0].rank, player_bluff_card[0].suit)

            if round_card is None:
                player_bluff_card = self.play_bluff(reset, None)
                # for player in game_obj.players:
                    # if (player.name != self.name) and (player.character == "Credulous"):
                    #     player.set_belief_model(self, self.announce)
                print(self.name + " announced " + self.announce + " and played " + player_bluff_card[0].rank)
                print("End of turn for " + self.name)
                print("\n")

                return player_bluff_card

            else :
                player_bluff_card = self.play_bluff(reset, round_card)
                self.announce = round_card #playing the bluff card and announcing it as a real card
                print (self.name + " announced " + self.announce + " and played " + player_bluff_card[0].rank)
                # for player in game_obj.players:
                #     if (player.name != self.name) and (player.character == "Credulous"):
                #         player.set_belief_model(self, self.announce)
                print("End of turn for " + self.name)
                print("\n")
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
        prob = random.random()
        if prob < self.bluff_prob:  # less than bluff_prob, player doesnt bluff
            played = self.play_allrank(reset, round_card)
            if type(played) is int:
                print(self.name + "passed")
                return None
            else:
                self.announce = [played[0].rank] * len(played)
                # for player in game_obj.players:
                #     if player.name != self.name and player.character == "Credulous":
                #         player.set_belief_model(self, self.announce)
                print("End of turn for " + self.name)
                print("\n")
                return played

        else:  # a bluff play

            # print (player_bluff_card[0].rank, player_bluff_card[0].suit)

            if round_card is None:
                player_bluff_card = self.play_bluff(reset, None)
                # for player in game_obj.players:
                #     if (player.name != self.name) and (player.character == "Credulous"):
                #         player.set_belief_model(self, self.announce)
                print(self.name + " announced " + self.announce + " and played " + player_bluff_card[0].rank)
                print("End of turn for " + self.name)
                print("\n")

                return player_bluff_card

            else:
                player_bluff_card = self.play_bluff(reset, round_card)
                self.announce = round_card  # playing the bluff card and announcing it as a real card
                print(self.name + " announced " + self.announce + " and played " + player_bluff_card[0].rank)
                # for player in game_obj.players:
                #     if (player.name != self.name) and (player.character == "Credulous"):
                #         player.set_belief_model(self, self.announce)
                print("End of turn for " + self.name)
                print("\n")
                return player_bluff_card


    def call_bluff(self, game_obj, prev_agent):
        bluff = super().call_bluff(game_obj, prev_agent)
        if bluff == 1:
            self.trust[prev_agent.name] = (self.trust[prev_agent.name] - self.trust[prev_agent.name])/3
        else:
            self.trust[prev_agent.name] = (self.trust[prev_agent.name] + self.trust[prev_agent.name])/3
