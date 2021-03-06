from simulation.Player import CredulousPlayer, SkepticalPlayer, RevisingPlayer
class Game:
	def __init__(self, hands):

		self.players = []
		self.played_deck = []
		self.hands = hands

		

	def init_game_players(self, player_list):

		print (player_list)

		for i in range(self.hands):

			name = "Player_" + str(i + 1)

			if (player_list[i] == "Credulous"):
				self.players.append(CredulousPlayer(name= name))
			elif (player_list[i] == "Skeptic"):
				self.players.append(SkepticalPlayer(name= name))
			else:
				self.players.append(RevisingPlayer(name= name))


	def game_play(self):

		reset = 0
		end_game = False
		i = 0
		rounds = 0
		round_starter = 0
		pass_counter = 0
		round_card = None
		announcement=list()
		bluff_play=-1

		while not end_game:
			agent = (2 if i == 0 else i-1) #get previous agent who played
			action = self.players[i].choose_action(reset, self.players[agent], announcement)
			if action == 1:  #agent plays
				play = self.players[i].play(reset, self, round_card)
				if type(play) is not int:  #if agent played
					for card in play:
						self.players[i].stash.remove(card)  #remove played cards from agent's hand
						self.players[i].calculate_groupstash()
						try:
							self.players[i].belief_model[self.players[i].name].remove(card)
						except:
							pass
					self.played_deck.append(play)  #add played cards to played deck
					for k in play:
						announcement.append(self.players[i].announce[0])
			else:
				bluff_play = self.players[i].call_bluff(self, self.players[agent])
				pass_counter = 3 #ending round
			if reset == 0:  #new round
				reset = 1
				round_starter = i
				round_card = self.players[i].announce[0]
			if play == 0:
				pass_counter += 1
				self.players[i].announce = list()
			if pass_counter == 3:
				rounds = rounds + 1
				if bluff_play == 1:
					i = i - 1
				elif bluff_play == 0:
					i = i - 2
				else:
					i = round_starter
				print("End of round " + str(rounds))
				print("--------------------------------------------")
				reset = 0
				pass_counter = 0
				announcement=list()
				self.played_deck=[]
			else:
				i = i + 1
			
			if i == len(self.players):
				i = 0
				
			end_game = self.check_endgame_condition()

	def check_endgame_condition(self):

		for p in self.players:
			if (len(p.grouped_stash) == 0):
				print(p.name + "Wins!!")
				return True
