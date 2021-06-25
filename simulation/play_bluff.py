import random
from simulation.Player import *

SYMBOLS = ['♠', '♢', '♡', '♣']
SUIT = ['Hearts', 'Spades', 'Diamonds']
RANK = ['A', '2', '3', '4', '5']
RANK_VALUE = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5}
SUIT_SYMBOLS = {'Hearts': '♡', 'Spades': '♠', 'Diamonds': '♢'} # Explain this in the website


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit


class Deck:
    def __init__(self, pack):
        self.pack = pack
        self.cards = []

        for i in range(pack):
            for s in SUIT:
                for r in RANK:
                    self.cards.append(Card(r, s))

    def draw_card(self):

        a = self.cards[0]
        self.cards.pop(0)
        return a

    def shuffle(self):

        random.shuffle(self.cards)











