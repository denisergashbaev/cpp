from os.path import join
from dimacs import dimacs
from file_operations import file_operations
from solitaire.Card import CardMapper
from solitaire.Pile import Pile
from solitaire.Stack import Stack

debug = False


class DimacsMapper(object):
    def __init__(self, num_ranks, num_suits, turns_count):
        self.num_turns = turns_count
        self.num_variables = num_ranks * num_suits * turns_count
        self.dimacs_lines = []

    def map(self, card, turn, negation=False):
        if debug:
            mapping = "x%s*%d+%d" % (card, self.num_turns, turn)
        else:
            mapping = card.index * self.num_turns + turn
        return ("-" if negation else "") + str(mapping)

    def get_num_clauses(self):
        return len(self.dimacs_lines)

    def encode(self):
        return dimacs.encode(self.num_variables, self.get_num_clauses(), self.dimacs_lines)

def main():
    input_file_name = "solit_4_4_0.txt"
    with open(join("Benchmark", input_file_name), 'r') as fh:
        data = fh.readlines()

    cards_per_suit = 3
    for idx, line in enumerate(data):
        l = line.strip()
        if idx == 0:
            num_suits, num_ranks = l.split(" ")
            num_suits = int(num_suits)
            num_ranks = int(num_ranks)
            card_mapper = CardMapper(num_suits, num_ranks)
            cards_in_piles_count = num_suits * num_ranks - 1
            r = range(cards_in_piles_count / cards_per_suit)
            piles = [Pile() for _ in r]
            stack = Stack(card_mapper.get_max_card())
        else:
            pile = piles[(idx - 1) / cards_per_suit]
            index = int(l)
            pile.add_card(card_mapper.get_card(index))

    print(stack)
    for pile in piles:
        print(pile)

    #===modelling===#

    num_turns = cards_in_piles_count
    turns_range = range(num_turns+1)
    dimacs_mapper = DimacsMapper(num_ranks, num_suits, num_turns)
    #1 constraint: you can only take an 'open' card from a pile and put it on the stack
    for pile in piles:
        for top_card_idx, top_card in enumerate(pile.cards):
            for turn in turns_range:
                if top_card_idx > turn:
                    line = [dimacs_mapper.map(top_card, turn, negation=True)]
                    dimacs_mapper.dimacs_lines.append(line)

    all_pile_cards = []
    for p in piles:
        for card in p.cards:
            all_pile_cards.append(card)

    #2 there should be a card played each turn
    for turn in turns_range:
        line = []
        for card in all_pile_cards:
            line.append(dimacs_mapper.map(card, turn))
        dimacs_mapper.dimacs_lines.append(line)

    #3 there can be only one move at a time
    for turn in turns_range:
        line = []
        for card in all_pile_cards:
            line.append(dimacs_mapper.map(card, turn, negation=True))
        dimacs_mapper.dimacs_lines.append(line)

    #4 the stack may only contain the valid moves +/-1 rank between consecutive cards
    for turn in turns_range:
        for card in all_pile_cards:
            line = []
            next_turn = turn + 1
            if next_turn < len(turns_range):
                line.append(dimacs_mapper.map(card, turn, negation=True))
                for other_card in all_pile_cards:
                    if card != other_card and not card.is_valid_neighbor(other_card, num_ranks):
                        line.append(dimacs_mapper.map(other_card, next_turn, negation=True))
                if len(line) > 1:
                    dimacs_mapper.dimacs_lines.append(line)

    output = dimacs_mapper.encode()
    cnf_file_name, cnf_full_file_name = file_operations.write_cnf("cnfs", input_file_name, output, dimacs_mapper.num_variables, dimacs_mapper.get_num_clauses())
    file_operations.call_sat_solver("solutions", cnf_file_name, cnf_full_file_name)

if __name__ == "__main__":
    main()