from play_bluff import *
from Game import Game

def main():

    deck = Deck(1)
    deck.shuffle()

    g = Game(3)


    # deal cards

    for i in range(5):
        for hand in g.players:
            card = deck.draw_card()
            hand.addTo_hand(card)

    for player in g.players:
        print(player.name)



        for card in player.stash:
            print(card.rank, SUIT_SYMBOLS[card.suit])






        print ("\n")

    g.game_play()

main()