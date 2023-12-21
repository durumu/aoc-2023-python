from __future__ import annotations

import sys
from collections import defaultdict
from collections.abc import Iterable
from functools import cached_property

from attrs import field, frozen


@frozen
class State:
    high_flip_flops: set[str]
    conjunction_memory: dict[str, set[str]]
    total_low: int = 0
    total_high: int = 0


@frozen(slots=False)
class Machine:
    flip_flops: set[str]
    conjunctions: set[str]
    children: defaultdict[str, list[str]]

    @cached_property
    def parents(self) -> dict[str, list[str]]:
        parents = defaultdict(list)
        for node, child_nodes in self.children.items():
            for child in child_nodes:
                parents[child].append(node)
        return parents

    def next_state(self, state: State) -> State:
        receiving = {
            node: ("broadcaster", True) for node in self.children["broadcaster"]
        }
        flip_flop_high = {
            node: node in state.high_flip_flops for node in self.flip_flops
        }
        conjunction_memory = {
            node: memory.copy() for node, memory in state.conjunction_memory.items()
        }
        lows_sent = highs_sent = 0
        while receiving:
            sending = {}
            for node, (sender, is_high) in receiving.items():
                if is_high:
                    highs_sent += 1
                else:
                    lows_sent += 1
                if node in self.flip_flops:
                    if is_high != flip_flop_high[node]:
                        flip_flop_high[node] = is_high
                        for child in self.children[node]:
                            sending[child] = (node, is_high)
                elif node in self.conjunctions:
                    if is_high:
                        conjunction_memory[node].add(sender)
                    else:
                        conjunction_memory[node].discard(sender)
                    send_high = len(conjunction_memory[node]) == len(self.parents[node])
                    for child in self.children[node]:
                        sending[child] = (node, send_high)
                else:
                    for child in self.children[node]:
                        sending[child] = (node, is_high)
            receiving = sending

        return State(
            {node for node, is_high in flip_flop_high.items() if is_high},
            conjunction_memory,
            state.total_low + lows_sent,
            state.total_high + highs_sent,
        )

    def count_pulses(self, runs: int) -> int:
        """returns (low pulses * high pulses)"""
        state = State(set(), {node: set() for node in self.conjunctions})
        for _ in range(runs):
            print(state)
            state = self.next_state(state)
        print(state)
        return state.total_low * state.total_high

    @classmethod
    def parse(cls, lines: Iterable[str]) -> Machine:
        flip_flops = set()
        conjunctions = set()
        children = defaultdict(list)

        for line in lines:
            node, child_nodes = line.split(" -> ")
            if node.startswith("%"):
                node = node.removeprefix("%")
                flip_flops.add(node)
            elif node.startswith("&"):
                node = node.removeprefix("&")
                conjunctions.add(node)
            children[node] = child_nodes.split(", ")

        return Machine(flip_flops, conjunctions, children)


def main():
    machine = Machine.parse(line.strip() for line in sys.stdin)
    print(machine.count_pulses(4))
    # print(machine.count_pulses(1000))


if __name__ == "__main__":
    main()
