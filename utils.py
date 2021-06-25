import pygame as pg

class DropDown():

	def __init__(self, color_menu, color_option, x, y, w, h, font, main, options):
		self.color_menu = color_menu
		self.color_option = color_option
		self.rect = pg.Rect(x, y, w, h)
		self.font = font
		self.main = main
		self.options = options
		self.draw_menu = False
		self.menu_active = False
		self.active_option = -1

	def draw(self, surf):
		pg.draw.rect(surf, self.color_menu[self.menu_active], self.rect, 0)
		msg = self.font.render(self.main, 1, (0, 0, 0))
		surf.blit(msg, msg.get_rect(center = self.rect.center))

		if self.draw_menu:
			for i, text in enumerate(self.options):
				rect = self.rect.copy()
				rect.y += (i+1) * self.rect.height
				pg.draw.rect(surf, self.color_option[1 if i == self.active_option else 0], rect, 0)
				msg = self.font.render(text, 1, (0, 0, 0))
				surf.blit(msg, msg.get_rect(center = rect.center))

	def update(self, event_list):
		mpos = pg.mouse.get_pos()
		self.menu_active = self.rect.collidepoint(mpos)
		
		self.active_option = -1
		for i in range(len(self.options)):
			rect = self.rect.copy()
			rect.y += (i+1) * self.rect.height
			if rect.collidepoint(mpos):
				self.active_option = i
				break

		if not self.menu_active and self.active_option == -1:
			self.draw_menu = False

		for event in event_list:
			if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
				if self.menu_active:
					self.draw_menu = not self.draw_menu
				elif self.draw_menu and self.active_option >= 0:
					self.draw_menu = False
					return self.active_option
		return -1

def DrawBar(pos, size, borderC, barC, progress, screen):

	pg.draw.rect(screen, borderC, (*pos, *size), 1)
	innerPos  = (pos[0]+3, pos[1]+3)
	innerSize = ((size[0]-6) * progress, size[1]-6)
	pg.draw.rect(screen, barC, (*innerPos, *innerSize))

def get_player_stash(stash):

	player_stash = []

	for card in stash:
		player_stash.append(card.rank + '_of_' + (card.suit).lower())

	return player_stash

def get_player_play(played):

	player_play = []

	for card in played:
		player_play.append(card.rank + '_of_' + (card.suit).lower())

	return player_play

