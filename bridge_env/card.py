from __future__ import annotations

from .suit import Suit


class Card:
    def __init__(self, rank: int, suit: Suit):
        if rank < 2 or 14 < rank:
            raise ValueError("card rank is from 2 to 14")
        if suit == Suit.NT:
            raise ValueError("card suit is not NT")

        self.rank = rank  # int, 2 - 14
        self.suit = suit  # Suit object

    def __str__(self):
        if self.rank == 10:
            return self.suit.name + 'T'
        elif self.rank == 11:
            return self.suit.name + 'J'
        elif self.rank == 12:
            return self.suit.name + 'Q'
        elif self.rank == 13:
            return self.suit.name + 'K'
        elif self.rank == 14:
            return self.suit.name + 'A'

        return self.suit.name + str(self.rank)

    def __int__(self):
        """

        :return: int, [0, 51] (C2 - CA, D2 - DA, H2 - HA, S2 - SA)
        """
        return self.rank - 2 + (self.suit.value - 1) * 13

    def __eq__(self, card):
        return self.suit == card.suit and self.rank == card.rank

    @classmethod
    def int_to_card(cls, x: int) -> Card:
        if x < 0 or 51 < x:
            raise ValueError("card int is from 0 to 51")

        return Card(x % 13 + 2, Suit(x // 13 + 1))

    @classmethod
    def rank_int_to_str(cls, rank: int) -> str:
        if rank < 2 or 14 < rank:
            raise ValueError("card rank is from 2 to 14")

        if rank == 10:
            return 'T'
        elif rank == 11:
            return 'J'
        elif rank == 12:
            return 'Q'
        elif rank == 13:
            return 'K'
        elif rank == 14:
            return 'A'

        return str(rank)