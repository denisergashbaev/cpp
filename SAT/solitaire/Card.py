class CardMapper(object):
    def __init__(self, num_suits, num_ranks):
        self.index_to_card = {}
        for suit in range(num_suits):
            for rank in range(num_ranks):
                index = num_ranks * suit + rank
                card = Card(suit, rank, index)
                if index == 0:
                    self.first_card = card
                else:
                    self.index_to_card[index] = card

    def get_card(self, index):
        return self.index_to_card[index]

    def get_first_card(self):
        return self.first_card


class Suit(object):
    names = ("spades", "clubs", "diamonds", "hearts")

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)
        #return Suit.names[self.value][:1]


class Card(object):
    def __init__(self, suit, rank, index):
        self.suit = Suit(suit)
        self.rank = rank
        self.index = index

    def is_valid_neighbor(self, other, num_ranks):
        min_v = min(self.rank, other.rank)
        max_v = max(self.rank, other.rank)
        diff = max_v - min_v
        return diff == 1 or (min_v == 0 and max_v == num_ranks - 1)

    def __repr__(self):
        return "%s:%s--ind%s" % (self.rank, self.suit, self.index)