from Player import CredulousPlayer, SkepticalPlayer
class Game:
    def __init__(self, hands):

        self.players = []
        self.played_deck = []

        for i in range(hands):
            name = "Player_" + str(i + 1)
            self.players.append(SkepticalPlayer(name= name))

    def game_play(self):
        reset = 0
        end_game = False
        i = 0
        rounds = 0
        round_starter = 0
        pass_counter = 0
        round_card = None
        # for player in self.players:
        #     print(player.name)
        #     for key, value in player.belief_model.items():
        #         print(key)
        #         for i in value:
        #             print(i.rank,i.suit)
        while not end_game:
            agent = (2 if i == 0 else i-1) #get previous agent who played
            action = self.players[i].choose_action(reset, self.players[agent])
            if action == 1:  #agent plays

                play = self.players[i].play(reset, self, round_card)
                if type(play) is not int:  #if agent played
                    for card in play:
                        self.players[i].stash.remove(card)  #remove played cards from agent's hand
                        self.players[i].calculate_groupstash()
                    #self.players[i].grouped_stash.remove(play)
                    self.played_deck.append(play)  #add played cards to played deck
            else:
                bluff_play = self.players[i].call_bluff(self, self.players[agent])
                print(bluff_play)
            if reset == 0:  #new round
                reset = 1
                round_starter = i
                round_card = self.players[i].announce[0]
            if play == 0:
                pass_counter += 1
                self.players[i].announce = list()
            if pass_counter == 3:
                rounds = rounds + 1
                print("End of round " + str(rounds))
                print("--------------------------------------------")
                reset = 0
                i = round_starter
                pass_counter = 0
            else:
                i = i + 1

            if i == len(self.players):
                i = 0

                #check for end game condition

            end_game = self.check_endgame_condition()


    def check_endgame_condition(self):

        for p in self.players:
            if (len(p.grouped_stash) == 0):
                print(p.name + "Wins!!")
                return True
