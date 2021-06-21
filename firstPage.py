import pygame as pg
import pygame_gui

from ui.firstPage_UI import menu_data, COLOR_INACTIVE, COLOR_ACTIVE, COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE
from utils import DropDown

from mainPage import mainPage


white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)

player_types = ['Credulous', 'Skeptic', 'Revising']


def firstPage():	

	pg.display.set_caption('Bluff simulator')
	window_surface = pg.display.set_mode((800, 600))

	background = pg.Surface((800, 800))
	background.fill(pg.Color('#ffffff'))

	clock = pg.time.Clock()
	is_running = True


	font = pg.font.SysFont(None, 25)

	text_1 = font.render('Select Mode for Player 1', True, black, white)

	textRect_1 = text_1.get_rect()

	textRect_1.center = (150, 50)

	player1_dropdown_button = DropDown(
									[COLOR_INACTIVE, COLOR_ACTIVE],
									[COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
									50, 80, 200, 50, 
									pg.font.SysFont(None, 25), 
									"Click to select", ["Credulous", "Skeptical", "Revising"])

	text_2 = font.render('Select Mode for Player 2', True, black, white)

	textRect_2 = text_2.get_rect()

	textRect_2.center = (400, 50)


	player2_dropdown_button = DropDown(
									[COLOR_INACTIVE, COLOR_ACTIVE],
									[COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
									300, 80, 200, 50, 
									pg.font.SysFont(None, 25), 
									"Click to select", ["Credulous", "Skeptical", "Revising"])

	text_3 = font.render('Select Mode for Player 3', True, black, white)

	textRect_3 = text_3.get_rect()

	textRect_3.center = (650, 50)

	player3_dropdown_button = DropDown(
									[COLOR_INACTIVE, COLOR_ACTIVE],
									[COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
									550, 80, 200, 50, 
									pg.font.SysFont(None, 25), 
									"Click to select", ["Credulous", "Skeptical", "Revising"])

	player_1_selected = False
	player_2_selected = False
	player_3_selected = False

	players_selected = []
	
	while is_running:

		clock.tick(30)

		event_list = pg.event.get()

		for event in event_list:
			if event.type == pg.QUIT:
				is_running = False

		window_surface.fill((255, 255, 255))

		player1_dropdown_button.draw(window_surface)

		player2_dropdown_button.draw(window_surface)

		player3_dropdown_button.draw(window_surface)
		

		window_surface.blit(text_1, textRect_1)

		window_surface.blit(text_2, textRect_2)

		window_surface.blit(text_3, textRect_3)

		pg.display.flip()

		selected_option_1 = player1_dropdown_button.update(event_list)

		if selected_option_1 >= 0:
			player1_dropdown_button.main = player1_dropdown_button.options[selected_option_1]
			player_1_selected = True
			player_1_type = player_types[selected_option_1]
			players_selected.append(player_1_type)

		selected_option_2 = player2_dropdown_button.update(event_list)

		if selected_option_2 >= 0:
			player2_dropdown_button.main = player2_dropdown_button.options[selected_option_2]
			player_2_selected = True
			player_2_type = player_types[selected_option_2]
			players_selected.append(player_2_type)

		selected_option_3 = player3_dropdown_button.update(event_list)

		if selected_option_3 >= 0:
			player3_dropdown_button.main = player3_dropdown_button.options[selected_option_3]
			player_3_selected = True
			player_3_type = player_types[selected_option_3]
			players_selected.append(player_3_type)



		if (player_1_selected == True) and (player_2_selected == True) and (player_3_selected == True):

			is_running = mainPage(is_running, window_surface, pg, clock, players_selected)

				
		
		

		
