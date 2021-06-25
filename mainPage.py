from ui.cards_UI import plot_players_hand, plot_players_play, ImageDB, plot_announcements, plot_bluff_announcements
from utils import get_player_stash, get_player_play
from collections import defaultdict


white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)

def mainPage(is_running, window_surface, pg, clock, players_selected, g):

	font = pg.font.SysFont(None, 23)

	player_text_1 = font.render('Player 1 (' + players_selected[0] + ')', True, black, white)
	player_textRect_1 = player_text_1.get_rect()
	player_textRect_1.center = (80, 30)
	player_1_offset = 50

	player_text_2 = font.render('Player 2 (' + players_selected[1] + ')', True, black, white)
	player_textRect_2 = player_text_2.get_rect()
	player_textRect_2.center = (80, 200)
	player_2_offset = 220

	player_text_3 = font.render('Player 3 (' + players_selected[2] + ')', True, black, white)
	player_textRect_3 = player_text_3.get_rect()
	player_textRect_3.center = (80, 370)
	player_3_offset = 390

	player_offsets = [50, 220, 390]

	announcement_font = pg.font.SysFont("Ariel", 20)

	player_announcement_text_1 = announcement_font.render('Player 1:', True, black, white)
	player_announcement_textRect_1 = player_announcement_text_1.get_rect()
	player_announcement_textRect_1.center = (600, 30)

	player_announcement_text_2 = announcement_font.render('Player 2:', True, black, white)
	player_announcement_textRect_2 = player_announcement_text_2.get_rect()
	player_announcement_textRect_2.center = (600, 100)

	player_announcement_text_3 = announcement_font.render('Player 3:', True, black, white)
	player_announcement_textRect_3 = player_announcement_text_3.get_rect()
	player_announcement_textRect_3.center = (600, 170)


	# game simulation variables

	reset = 0
	end_game = False
	i = 0
	rounds = 0
	round_starter = 0
	pass_counter = 0
	round_card = None
	announcement = list()
	bluff_play = -1

	rounds_plays = defaultdict(list)

	while (is_running) and (not end_game):

		clock.tick(30)

		event_list = pg.event.get()

		for event in event_list:
			if event.type == pg.QUIT:
				is_running = False
				return is_running

		window_surface.fill(pg.Color('#ffffff'))

		window_surface.blit(player_text_1, player_textRect_1)
		window_surface.blit(player_text_2, player_textRect_2)
		window_surface.blit(player_text_3, player_textRect_3)

		window_surface.blit(player_announcement_text_1, player_announcement_textRect_1)
		window_surface.blit(player_announcement_text_2, player_announcement_textRect_2)
		window_surface.blit(player_announcement_text_3, player_announcement_textRect_3)

		rounds_font = pg.font.SysFont("Ariel", 20)
		rounds_display_text = rounds_font.render('Rounds: ' +  str(rounds + 1), True, green, white)
		rounds_display_textRect = rounds_display_text.get_rect()
		rounds_display_textRect.center = (600, 300)

		window_surface.blit(rounds_display_text, rounds_display_textRect)


		

		plot_players_play(window_surface, player_offsets, rounds_plays)


		for j, player in enumerate(g.players):

			player_stash = []

			for card in player.stash:
				player_stash.append(card.rank + '_of_' + (card.suit).lower())

			if (j == 0):
				plot_players_hand(window_surface, player_1_offset, player_stash)
				#plot_players_play(window_surface, player_1_offset, ['5_of_clubs', '4_of_diamonds'])
			elif (j == 1):
				plot_players_hand(window_surface, player_2_offset, player_stash)
				#plot_players_play(window_surface, player_2_offset, ['5_of_clubs', '4_of_diamonds'])
			else:
				plot_players_hand(window_surface, player_3_offset, player_stash)
				#plot_players_play(window_surface, player_3_offset, ['5_of_clubs', '4_of_diamonds'])

		pg.display.update()

		if (i == 0):
			agent = 2
		else:
			agent = i -1

		action = g.players[i].choose_action(reset, g.players[agent], announcement)

		if action == 1:  #agent plays
			play = g.players[i].play(reset, g, round_card)

			if type(play) is not int:
				for card in play:
					g.players[i].stash.remove(card)
					g.players[i].calculate_groupstash()
					try:
						g.players[i].belief_model[g.players[i].name].remove(card)
					except:
						pass

				g.played_deck.append(play)

				for k in play:
					announcement.append(g.players[i].announce[0])

				rounds_plays[i] = get_player_play(play)

				plot_players_play(window_surface, player_offsets, rounds_plays)
				plot_players_hand(window_surface, player_offsets[i], get_player_stash(g.players[i].stash))
				print (g.players[i].announcements)
				plot_announcements(window_surface, i, g.players[i].announcements[-1])
				
			pg.display.update()
			pg.time.wait(2000)

		else:
			bluff_play = g.players[i].call_bluff(g, g.players[agent])
			plot_announcements(window_surface, i, g.players[i].announcements[-1])
			pg.time.wait(2000)

			if (bluff_play == 0):
				plot_bluff_announcements(window_surface, "False Bluff call, " + g.players[i].name + " picks up the deck", (0, 255, 0))
			else:
				plot_bluff_announcements(window_surface, "Bluff spotted, " + g.players[agent].name + " picks up the deck", (255, 0, 0))

			pass_counter = 3 # End the round

		if reset == 0:  #new round

			reset = 1
			round_starter = i
			round_card = g.players[i].announce[0]

			
			plot_players_play(window_surface, player_offsets, rounds_plays)
			#plot_players_hand(window_surface, player_offsets[i], get_player_stash(g.players[i].stash))

			pg.display.update()

			pg.time.wait(2000)

		if play == 0:

			print (rounds_plays)

			plot_announcements(window_surface, i, g.players[i].announcements[-1])

			plot_players_play(window_surface, player_offsets, rounds_plays)
			#plot_players_hand(window_surface, player_offsets[i], get_player_stash(g.players[i].stash))

			pg.display.update()

			pg.time.wait(2000)

			pass_counter += 1
			g.players[i].announce = list()

			

		if pass_counter == 3:

			plot_players_play(window_surface, player_offsets, rounds_plays)
			plot_players_hand(window_surface, player_offsets[i], get_player_stash(g.players[i].stash))

			pg.display.update()

			pg.time.wait(2000)

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
			g.played_deck=[]
			rounds_plays = defaultdict(list)
			

		else:		

			#plot_players_hand(window_surface, player_offsets[i], get_player_stash(g.players[i].stash))
			plot_players_play(window_surface, player_offsets, rounds_plays)

			pg.display.update()

			i = i + 1

		if i == len(g.players):
			i = 0

		end_game = g.check_endgame_condition()
		

		#plot_announcements(window_surface, ["Player 1 played asasasas", "announced asasas"])
		#pg.display.update()


		