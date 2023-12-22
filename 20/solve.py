from __future__ import annotations

import itertools
import sys
from collections import defaultdict
from collections.abc import Iterable
from functools import cached_property

from attrs import frozen


@frozen
class State:
    flip_flop_on: dict[str, bool]
    conjunction_memory: dict[str, set[str]]
    rx_low: bool = False
    total_low: int = 0
    total_high: int = 0


@frozen
class Signal:
    sender: str
    receiver: str
    is_high: bool

    def __str__(self) -> str:
        return f"{self.sender} -{'high' if self.is_high else 'low'}-> {self.receiver}"


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
        flip_flop_on = state.flip_flop_on.copy()
        conjunction_memory = {
            node: memory.copy() for node, memory in state.conjunction_memory.items()
        }
        lows_sent = highs_sent = 0
        rx_low = False
        receiving = [Signal("button", "broadcaster", False)]
        while receiving:
            sending = []
            for s in receiving:
                if s.is_high:
                    highs_sent += 1
                else:
                    lows_sent += 1
                if s.receiver in self.flip_flops:
                    if not s.is_high:
                        flip_flop_on[s.receiver] ^= True
                        for child in self.children[s.receiver]:
                            sending.append(
                                Signal(s.receiver, child, flip_flop_on[s.receiver])
                            )
                elif s.receiver in self.conjunctions:
                    if s.is_high:
                        conjunction_memory[s.receiver].add(s.sender)
                    else:
                        conjunction_memory[s.receiver].discard(s.sender)
                    send_high = len(conjunction_memory[s.receiver]) != len(
                        self.parents[s.receiver]
                    )
                    for child in self.children[s.receiver]:
                        sending.append(Signal(s.receiver, child, send_high))
                else:
                    if not s.is_high and s.receiver == "rx":
                        rx_low = True
                    for child in self.children[s.receiver]:
                        sending.append(Signal(s.receiver, child, s.is_high))
            receiving = sending

        return State(
            flip_flop_on,
            conjunction_memory,
            rx_low,
            state.total_low + lows_sent,
            state.total_high + highs_sent,
        )

    def count_pulses(self, runs: int) -> int:
        """returns (low pulses * high pulses)"""
        state = State(
            {node: False for node in self.flip_flops},
            {node: set() for node in self.conjunctions},
        )
        for _ in range(runs):
            state = self.next_state(state)
        return state.total_low * state.total_high

    def presses_until_rx_low(self) -> int:
        state = State(
            {node: False for node in self.flip_flops},
            {node: set() for node in self.conjunctions},
        )
        for i in itertools.count():
            # print(i)
            # bits = "".join(str(int(h)) for h in state.flip_flop_on.values())
            # print(f"{int(bits, 2):x}")
            # print(*(",".join(sorted(s)) for s in state.conjunction_memory.values()))
            if state.rx_low:
                return i
            state = self.next_state(state)
        raise AssertionError

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
    print(f"Part 1: {machine.count_pulses(1000)}")
    print(f"Part 2: {machine.presses_until_rx_low()}")


if __name__ == "__main__":
    main()
