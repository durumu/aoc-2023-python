from __future__ import annotations

import sys

import attrs


@attrs.frozen
class Rating:
    x: int
    m: int
    a: int
    s: int

    @classmethod
    def parse(cls, line: str) -> Rating:
        x, m, a, s = (
            int(pair.split("=")[1]) for pair in line.lstrip("{").rstrip("}").split(",")
        )
        return cls(x, m, a, s)

    @property
    def value(self) -> int:
        return self.x + self.m + self.a + self.s


@attrs.frozen
class Rule:
    expr: str
    destination: str


@attrs.frozen
class Workflow:
    name: str
    rules: list[Rule]

    def apply(self, rating: Rating) -> str:
        for rule in self.rules:
            if eval(rule.expr, attrs.asdict(rating)):
                return rule.destination
        raise AssertionError

    @classmethod
    def parse(cls, line: str) -> Workflow:
        name, rules_str = line.rstrip("}").split("{")
        rules = []
        for rule_spec in rules_str.split(","):
            if ":" in rule_spec:
                rules.append(Rule(*rule_spec.split(":")))
            else:
                rules.append(Rule("True", rule_spec))
        return cls(name, rules)


@attrs.frozen
class WorkflowMap:
    workflows: dict[str, Workflow]

    def accepts(self, rating: Rating) -> bool:
        cur = "in"
        while cur not in {"A", "R"}:
            cur = self.workflows[cur].apply(rating)
        return cur == "A"


def main():
    workflow_lines, rating_lines = (
        s.split("\n") for s in sys.stdin.read().split("\n\n")
    )

    workflow_map = WorkflowMap({w.name: w for w in map(Workflow.parse, workflow_lines)})
    ratings = [Rating.parse(line) for line in rating_lines]

    print(f"Part 1: {sum(r.value for r in ratings if workflow_map.accepts(r))}")


if __name__ == "__main__":
    main()
