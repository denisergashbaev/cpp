class Stack(object):
    def __init__(self, first_card):
        self.cards = [first_card]

    def add_card(self, card):
        self.cards.append(card)

    def __repr__(self):
        return self.__class__.__name__ + ": " + str(self.cards)