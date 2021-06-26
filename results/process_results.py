import csv
from collections import Counter
import matplotlib.pyplot as plt

file_name = "../Results.csv"

winner_list = []
winner_list_wo_player_1 = []

def plot_bar_graph(x_axis, y_axis):

	fig = plt.figure(figsize = (10, 5))

	plt.bar(x_axis, y_axis, color ='maroon', width = 0.4)

	plt.xlabel("Type of Agent")
	plt.ylabel("No. of Wins")
	plt.title("Type of Agents vs No. of Wins")
	plt.show()

def plot_bar_graph_except_player_1(x_axis, y_axis):

	fig = plt.figure(figsize = (10, 5))

	plt.bar(x_axis, y_axis, color = 'blue', width = 0.4)

	plt.xlabel("Type of Agent")
	plt.ylabel("No. of Wins")
	plt.title("Type of Agents vs No. of Wins as secondary or tertiary player")
	plt.show()



with open(file_name, newline='') as csvfile:
	csv_reader = csv.reader(csvfile, delimiter=' ')
	for i, row in enumerate(csv_reader):
		if (i % 2 != 0):
			player_1 = row[0].split(',')[0]
			player_2 = row[0].split(',')[1]
			player_3 = row[0].split(',')[2]

			winner = row[0].split(',')[3]
			winner_list.append(winner)

			type_of_player = row[0].split(',')[4]

			if type_of_player != 'Player_1':
				winner_list_wo_player_1.append(winner)


			

winners_dict = Counter(winner_list)
winners_dict_wo_player_1 = Counter(winner_list_wo_player_1)



x_axis = []
y_axis = []

for key, value in winners_dict.items():
	x_axis.append(key)
	y_axis.append(value)

plot_bar_graph(x_axis, y_axis)



x_axis = []
y_axis = []

for key, value in winners_dict_wo_player_1.items():
	x_axis.append(key)
	y_axis.append(value)

plot_bar_graph_except_player_1(x_axis, y_axis)









