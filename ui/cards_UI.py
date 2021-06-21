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

def plot_players_play(screen, offset, card_list):

	image_db = ImageDB.get_instance()

	for i, card in enumerate(card_list):
		image = image_db.get_image('ui\\cards\\' + card + '_blended.png')

		screen.blit(image, (220 + i*15, offset))


def plot_announcements(screen, texts):

	font = pygame.font.SysFont("Ariel", 20)

	offset = 50

	for n, line in enumerate(texts):
		text = font.render(line, 1, (0, 0, 0))
		text_rect = text.get_rect()
		text_rect.center = (600, offset*(n+1))
		screen.blit(text, text_rect)


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
			print (path)
			image = pygame.image.load(path)
			self.image_library[path] = image

		return image






