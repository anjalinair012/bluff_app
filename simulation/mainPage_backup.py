from ui.cards_UI import plot_players_hand, plot_players_play, ImageDB, plot_announcements
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

	rounds_font = pg.font.SysFont("Ariel", 20)

	
	

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

		rounds_display_text = rounds_font.render('Rounds: ' +  str(rounds + 1), True, green, white)
		rounds_display_textRect = rounds_display_text.get_rect()
		rounds_display_textRect.center = (600, 300)

		window_surface.blit(rounds_display_text, rounds_display_textRect)


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

		plot_players_play(window_surface, player_offsets, rounds_plays)

		if (i == 0):
			agent = 2
		else:
			agent = i -1

		action = g.players[i].choose_action(reset, g.players[agent])

		if action == 1:  #agent plays
			play = g.players[i].play(reset, g, round_card)

			if type(play) is not int:
				for card in play:
					g.players[i].stash.remove(card)
					g.players[i].calculate_groupstash()

				g.played_deck.append(play)

				rounds_plays[i] = get_player_play(play)

				plot_players_play(window_surface, player_offsets, rounds_plays)
				#plot_players_hand(window_surface, player_offsets[i], get_player_stash(g.players[i].stash))
				plot_announcements(window_surface, i, g.players[i].announcements[-1])
				
			pg.display.update()
			pg.time.wait(2000)

		else:
			bluff_play = self.players[i].call_bluff(self, self.players[agent])
			print(bluff_play)

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
			print("End of round " + str(rounds))
			print("--------------------------------------------")
			rounds_plays = defaultdict(list)
			reset = 0
			i = round_starter
			pass_counter = 0
			

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


		