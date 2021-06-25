import os
import logging
import inspect
import pygame
from PIL import Image



def plot_players_hand(screen, offset, hand_list):

	image_db = ImageDB.get_instance()

	for i, card in enumerate(hand_list):
		image = image_db.get_image('ui\\cards\\' + card + '.png')

		screen.blit(image, (50 + i*15, offset))

def plot_players_play(screen, offset, card_dict):

	image_db = ImageDB.get_instance()

	for key in card_dict:
		for i, card in enumerate(card_dict[key]):
			image = image_db.get_image('ui\\cards\\' + card + '_blended.png')

			screen.blit(image, (290 + i*15, offset[key]))


def plot_announcements(screen, i, texts):

	font = pygame.font.SysFont("Ariel", 20)

	offset = 50

	if i == 0:

		text = font.render(texts, 1, (0, 0, 0))
		text_rect = text.get_rect()
		text_rect.center = (600, 50)
		screen.blit(text, text_rect)
		pygame.time.wait(1000)

	elif i == 1:
		text = font.render(texts, 1, (0, 0, 0))
		text_rect = text.get_rect()
		text_rect.center = (600, 120)
		screen.blit(text, text_rect)
		pygame.time.wait(1000)

	else:
		text = font.render(texts, 1, (0, 0, 0))
		text_rect = text.get_rect()
		text_rect.center = (600, 190)
		screen.blit(text, text_rect)
		pygame.time.wait(1000)

def plot_bluff_announcements(screen, texts, color):

	bluff_announcement_font = pygame.font.SysFont("Ariel", 20)

	text = bluff_announcement_font.render(texts, 1, color)
	text_rect = text.get_rect()
	text_rect.center = (300, 530)
	screen.blit(text, text_rect)
	pygame.time.wait(1000)






class ImageDB:

	instance = None

	@classmethod

	def get_instance(cls):

		if cls.instance is None:
			cls.instance = cls()
		return cls.instance


	def __init__(self):

		logging.debug(inspect.stack()[0][3] + ':' + 'enter')
		self.image_library = {}


	def get_image(self, path):

		image = self.image_library.get(path)

		if image is None:
			logging.info(inspect.stack()[0][3] + ':' + path)
			#print (path)
			image = pygame.image.load(path)
			self.image_library[path] = image

		return image






