import operator


class CardMapper(object):
    def __init__(self, num_suits, num_ranks):
        self.index_to_card = {}
        for suit in range(num_suits):
            for rank in range(num_ranks):
                index = num_suits * suit + rank
                card = Card(suit, rank, index)
                if index == 0:
                    self.first_card = card
                else:
                    self.index_to_card[index] = card

    def get_card(self, index):
        return self.index_to_card[index]

    def get_max_card(self):
        return max(self.index_to_card.iteritems(), key=operator.itemgetter(0))[1]


class Suit(object):
    names = ("spades", "clubs", "diamonds", "hearts")

    def __init__(self, value):
        self.name = Suit.names[value]

    def __repr__(self):
        return self.name[:1]


class Card(object):
    def __init__(self, suit, rank, index):
        self.suit = Suit(suit)
        self.rank = rank
        self.index = index

    def __repr__(self):
        return "%s:%s" % (self.rank, self.suit)