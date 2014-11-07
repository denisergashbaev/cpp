from os.path import join
from solitaire.Card import CardMapper
from solitaire.Pile import Pile
from solitaire.Stack import Stack


def main():
    with open(join("Benchmark", "solit_4_4_0.txt"), 'r') as fh:
        data = fh.readlines()

    cards_per_suit = 3
    for idx, line in enumerate(data):
        l = line.strip()
        if idx == 0:
            num_suits, num_ranks = l.split(" ")
            num_suits = int(num_suits)
            num_ranks = int(num_ranks)
            card_mapper = CardMapper(num_suits, num_ranks)
            r = range((num_suits * num_ranks - 1) / cards_per_suit)
            piles = [Pile() for _ in r]
            stack = Stack(card_mapper.get_max_card())
        else:
            pile = piles[(idx - 1) / cards_per_suit]
            index = int(l)
            pile.add_card(card_mapper.get_card(index))

    print(stack)
    total = 1
    for pile in piles:
        print(pile)
        total += len(pile.cards)
    print("total cards %d and should be %d" % (total, num_ranks * num_suits))

    #===modelling===#

    #1 constraint: you can only take an 'open' card from a pile and put it on the stack


    #2 constraint: a card must be a rank higher or lower than the top card on the stack



if __name__ == "__main__":
    main()