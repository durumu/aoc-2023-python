from __future__ import annotations

import sys
from collections import Counter
from enum import IntEnum


class HandType(IntEnum):
    HighCard = 1
    OnePair = 2
    TwoPair = 3
    ThreeOfAKind = 4
    FullHouse = 5
    FourOfAKind = 6
    FiveOfAKind = 7


def hand_type(hand: str) -> HandType:
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


def key(hand: str) -> tuple:
    rank_order = "23456789TJQKA"

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
