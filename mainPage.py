from ui.cards_UI import plot_players_hand, plot_players_play, ImageDB, plot_announcements


white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)

def mainPage(is_running, window_surface, pg, clock, players_selected):

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

	while is_running:

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
		
		# player 1 plot
		plot_players_hand(window_surface, player_1_offset, ['5_of_clubs', '4_of_diamonds', 'ace_of_clubs', '2_of_hearts', '2_of_clubs'])
		plot_players_play(window_surface, player_1_offset, ['5_of_clubs', '4_of_diamonds'])

		
		# player 2 plot
		plot_players_hand(window_surface, player_2_offset, ['5_of_clubs', '4_of_diamonds', 'ace_of_clubs', '2_of_hearts', '2_of_clubs'])
		plot_players_play(window_surface, player_2_offset, ['5_of_clubs', '4_of_diamonds'])

		
		# player 3 plot
		plot_players_hand(window_surface, player_3_offset, ['5_of_clubs', '4_of_diamonds', 'ace_of_clubs', '2_of_hearts', '2_of_clubs'])
		plot_players_play(window_surface, player_3_offset, ['5_of_clubs', '4_of_diamonds'])
		

		plot_announcements(window_surface, ["Player 1 played asasasas", "announced asasas"])


		pg.display.update()