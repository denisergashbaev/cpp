class Pile(object):
    def __init__(self):
        self.__cards = []

    def add_card(self, card):
        self.__cards.append(card)

    def get_reversed_cards(self):
        return self.__cards[::-1]

    def get_cards(self):
        return self.__cards

    def is_empty(self):
        return len(self.__cards) == 0

    def __repr__(self):
        return self.__class__.__name__ + ": " + str(self.__cards)