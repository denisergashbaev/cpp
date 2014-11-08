class Pile(object):
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.insert(0, card)

    def is_empty(self):
        return len(self.cards) == 0

    def __repr__(self):
        return self.__class__.__name__ + ": " + str(self.cards)