from Player import CredulousPlayer
class Game:
    def __init__(self, hands):

        self.players = []
        self.played_deck = []

        for i in range(hands):
            name = "Player_" + str(i + 1)
            self.players.append(CredulousPlayer(name))

    def game_play(self):

        reset = 0
        end_game = False
        i = 0
        rounds = 0
        pass_counter = 0
        while not end_game:
            action = self.players[i].play(reset, self)
            if reset == 0:  #new round
                reset = 1
            if action == 0:
                pass_counter += 1
            if pass_counter == 3:
                rounds = rounds + 1
                print("End of round " + str(rounds))
                print("--------------------------------------------")
                reset = 0
                pass_counter = 0
            i = i + 1

            if i == len(self.players):
                i = 0

                #check for end game condition

                end_game = self.check_endgame_condition()


    def check_endgame_condition(self):

        for p in self.players:
            if (len(p.stash) == 0):
                return True
