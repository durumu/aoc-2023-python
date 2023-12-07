from __future__ import annotations

import sys
from collections import Counter
from enum import IntEnum


class HandType(IntEnum):
    EmptyHand = 0
    HighCard = 1
    OnePair = 2
    TwoPair = 3
    ThreeOfAKind = 4
    FullHouse = 5
    FourOfAKind = 6
    FiveOfAKind = 7

    def upgrade(self) -> HandType:
        """What we would get by adding one joker"""
        return {
            self.EmptyHand: self.HighCard,
            self.HighCard: self.OnePair,
            self.OnePair: self.ThreeOfAKind,
            self.TwoPair: self.FullHouse,
            self.ThreeOfAKind: self.FourOfAKind,
            self.FourOfAKind: self.FiveOfAKind,
        }[self]


def hand_type_no_jokers(hand: str) -> HandType:
    if not hand:
        return HandType.EmptyHand
    counts = list(Counter(hand).values())
    if 5 in counts:
        return HandType.FiveOfAKind
    if 4 in counts:
        return HandType.FourOfAKind
    if 2 in counts and 3 in counts:
        return HandType.FullHouse
    if 3 in counts:
        return HandType.ThreeOfAKind
    if counts.count(2) == 2:
        return HandType.TwoPair
    if 2 in counts:
        return HandType.OnePair
    return HandType.HighCard


def hand_type(hand: str) -> HandType:
    ret = hand_type_no_jokers("".join(c for c in hand if c != "J"))
    n_jokers = hand.count("J")
    for _ in range(n_jokers):
        ret = ret.upgrade()
    return ret


def key(hand: str) -> tuple:
    rank_order = "J23456789TQKA"

    return (hand_type(hand).value, tuple(rank_order.find(c) for c in hand))


def main():
    hands = []
    for line in sys.stdin:
        hand, bet = line.split()
        hands.append((hand, int(bet)))
    hands.sort(key=lambda hand_and_bet: key(hand_and_bet[0]))
    winnings = sum((i + 1) * bet for i, (_, bet) in enumerate(hands))
    print(winnings)


if __name__ == "__main__":
    main()
