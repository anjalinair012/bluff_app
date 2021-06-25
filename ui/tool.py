from PIL import Image

import os


list_of_images = os.listdir('cards')

for image in list_of_images:

	image1 = Image.open('cards\\' + image)
	back_card = Image.open('cards\\cardback1.png')

	image1 = image1.convert("RGBA")
	back_card = back_card.convert("RGBA")

	blended_image = Image.blend(image1, back_card, alpha=.7)

	blended_image.save('cards\\' + image.split('.')[0] + '_blended.png')