from os.path import join

from file_operations import file_operations
from solitaire.Card import CardMapper
from solitaire.Pile import Pile
from solitaire.Stack import Stack
from SAT.dimacs import dimacs


class DimacsMapper(object):

    def __init__(self, card_mapper, cards_in_piles_count, num_turns, debug):
        self.num_turns = num_turns
        self.num_variables = cards_in_piles_count * num_turns
        self.dimacs_lines = []
        self.debug = debug
        self.index_to_card = {}
        for key, value in card_mapper.index_to_card.iteritems():
            for turn in range(num_turns):
                mapping = self.map(value, turn)
                self.index_to_card[mapping] = {"card": value, "turn": turn}

    def map(self, card, turn, negation=False):
        if self.debug:
            mapping = "%s*%d+%d" % (card, self.num_turns, turn)
        else:
            mapping = (card.index - 1) * self.num_turns + turn + 1
        ret_val = ("-" if negation else "") + str(mapping)
        return ret_val

    def get_num_clauses(self):
        return len(self.dimacs_lines)

    def encode(self):
        return dimacs.encode(self.num_variables, self.get_num_clauses(), self.dimacs_lines)

    def append_lines(self, lines):
        for line in lines:
            self.dimacs_lines.append(line)

def main():
    debug_encoding = False
    debug_messages = True
    solutions_dir = "solutions"
    cnfs_dir = "cnfs"
    file_operations.clean_directories([solutions_dir, cnfs_dir])
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
            stack = Stack(card_mapper.get_first_card())
        else:
            pile = piles[(idx - 1) / cards_per_suit]
            index = int(l)
            pile.add_card(card_mapper.get_card(index))

    print(stack)
    for pile in piles:
        print(pile)

    #===modelling===#

    num_turns = cards_in_piles_count
    turns_range = range(num_turns)
    dimacs_mapper = DimacsMapper(card_mapper, cards_in_piles_count, num_turns, debug_encoding)
    all_pile_cards = []
    for p in piles:
        for card in p.get_reversed_cards():
            all_pile_cards.append(card)


    ##clauses##

    dimacs = []
    #constraints: special treatment for the first move
    for pile in piles:
        top_card = pile.get_reversed_cards()[0]
        if not top_card.is_valid_neighbor(stack.first_card, num_ranks):
            line = [dimacs_mapper.map(top_card, turns_range[0], negation=True)]
            dimacs.append(line)
    dimacs_mapper.append_lines(dimacs)

    if debug_messages:
        print "first valid moves"
        print dimacs

    #only open cards can be dealt
    dimacs = []
    for pile in piles:
        pile_cards = pile.get_cards()
        for card_idx, card in enumerate(pile_cards):
            next_idx = card_idx + 1
            if next_idx < len(pile_cards):
                prev_card = pile_cards[next_idx]
                for turn_idx, turn in enumerate(turns_range):
                    line = [dimacs_mapper.map(card, turn, negation=True)]
                    for prev_turn in turns_range[:turn_idx]:
                        line.append(dimacs_mapper.map(prev_card, prev_turn))
                    dimacs.append(line)
    dimacs_mapper.append_lines(dimacs)
    if debug_messages:
        print "only open cards can be dealt"
        print dimacs

    #there should be at least one card played each turn
    dimacs = []
    for turn in turns_range:
        line = []
        for card in all_pile_cards:
            line.append(dimacs_mapper.map(card, turn))
        dimacs.append(line)

    dimacs_mapper.append_lines(dimacs)

    if debug_messages:
        print "at least one card played each turn"
        print dimacs

    dimacs = []
    #there can only be one card played at a time
    for turn in turns_range:
        for idx, card in enumerate(all_pile_cards):
            for another_card in all_pile_cards[idx+1:]:
                line = [dimacs_mapper.map(card, turn, negation=True),
                        dimacs_mapper.map(another_card, turn, negation=True)]
                dimacs.append(line)

    dimacs_mapper.append_lines(dimacs)
    if debug_messages:
        print "only one card played at a time"
        print dimacs

    #a single card can only be played once
    dimacs = []
    for card in all_pile_cards:
        for idx, turn in enumerate(turns_range):
            for next_turn in turns_range[idx+1:]:
                line = [dimacs_mapper.map(card, turn, negation=True),
                        dimacs_mapper.map(card, next_turn, negation=True)]
                dimacs.append(line)

    dimacs_mapper.append_lines(dimacs)
    if debug_messages:
        print "a single card can only be played once"
        print dimacs

    #the stack may only contain the valid moves +/-1 rank between consecutive cards
    dimacs = []
    for turn in turns_range:
        for card in all_pile_cards:
            next_turn = turn + 1
            if next_turn < len(turns_range):
                for other_card in all_pile_cards:
                    if card != other_card and not card.is_valid_neighbor(other_card, num_ranks):
                        line = [dimacs_mapper.map(card, turn, negation=True),
                                dimacs_mapper.map(other_card, next_turn, negation=True)]
                        dimacs.append(line)

    dimacs_mapper.append_lines(dimacs)
    if debug_messages:
        print "the stack may only contain the valid moves"
        print dimacs


    output = dimacs_mapper.encode()
    cnf_file_name, cnf_full_file_name = file_operations.write_cnf(cnfs_dir, input_file_name, output, dimacs_mapper.num_variables, dimacs_mapper.get_num_clauses())
    _, sat_output_full_file_name = file_operations.call_sat_solver(solutions_dir, cnf_file_name, cnf_full_file_name)
    satisfiable, variables = file_operations.read_sat_output(sat_output_full_file_name)
    if satisfiable:
        print "SATISFIABLE"
        card_sequence = []
        for variable in variables:
            variable = str(variable)
            if variable in dimacs_mapper.index_to_card:
                dict = dimacs_mapper.index_to_card[variable]
                card_sequence.append(dict)

        card_sequence.sort(key=lambda pair: pair["turn"])
        ordered_cards = []
        for pair in card_sequence:
            ordered_cards.append(pair["card"])
        print "SOLUTION: " + str(ordered_cards)

if __name__ == "__main__":
    main()