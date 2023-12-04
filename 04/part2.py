from __future__ import annotations

import attrs
import sys


@attrs.frozen
class Card:
    card_id: int
    winning_numbers: set[int]
    picked_numbers: set[int]

    @classmethod
    def parse(cls, card_str: str) -> Card:
        card_id_str, numbers_str = card_str.strip().split(": ")
        winning_str, picked_str = numbers_str.split(" | ")
        return cls(
            card_id=int(card_id_str.split(" ")[-1]),
            winning_numbers={int(x) for x in winning_str.split()},
            picked_numbers={int(x) for x in picked_str.split()},
        )

    def n_matches(self) -> int:
        return len([x for x in self.picked_numbers if x in self.winning_numbers])


def main():
    cards = [Card.parse(line) for line in sys.stdin]
    scores = [card.n_matches() for card in cards]
    copies = [1] * len(cards)
    for i, score in enumerate(scores):
        for j in range(score):
            copies[i + j + 1] += copies[i]
    print(sum(copies))


if __name__ == "__main__":
    main()
