from __future__ import annotations

import sys

import attrs


@attrs.frozen
class Rule:
    variable: str
    destination: str
    min_val: int = 1
    max_val: int = 4001

    @property
    def complement(self) -> Rule:
        assert (self.min_val == 1) ^ (self.max_val == 4001)
        min_val = self.max_val if self.max_val != 4001 else 1
        max_val = self.min_val if self.min_val != 1 else 4001
        return Rule(self.variable, self.destination, min_val, max_val)


@attrs.frozen
class Workflow:
    name: str
    rules: list[Rule]

    @classmethod
    def parse(cls, line: str) -> Workflow:
        name, rules_str = line.rstrip("}").split("{")
        rules = []
        for rule_spec in rules_str.split(","):
            if ":" in rule_spec:
                expr, dest = rule_spec.split(":")
                if "<" in expr:
                    variable, constraint = expr.split("<")
                    rules.append(Rule(variable, dest, max_val=int(constraint)))
                else:
                    variable, constraint = expr.split(">")
                    rules.append(Rule(variable, dest, min_val=int(constraint) + 1))
            else:
                rules.append(Rule("x", rule_spec))
        return cls(name, rules)


def ways_to_satisfy(rules: list[Rule]) -> int:
    ways = 1
    for variable in "xmas":
        min_val = max(
            (rule.min_val for rule in rules if rule.variable == variable), default=1
        )
        max_val = min(
            (rule.max_val for rule in rules if rule.variable == variable), default=4001
        )
        ways *= max(max_val - min_val, 0)
    return ways


@attrs.frozen
class WorkflowMap:
    workflows: dict[str, Workflow]

    def _count_ways(self, label: str, rules: list[Rule]) -> int:
        if label == "A":
            return ways_to_satisfy(rules)
        if label == "R":
            return 0
        workflow = self.workflows[label]
        return sum(
            self._count_ways(
                rule.destination,
                [*rules, *(r.complement for r in workflow.rules[:i]), rule],
            )
            for i, rule in enumerate(workflow.rules)
        )

    def count_ways(self) -> int:
        return self._count_ways("in", [])


def main():
    workflow_lines, _ = (s.split("\n") for s in sys.stdin.read().split("\n\n"))

    workflow_map = WorkflowMap({w.name: w for w in map(Workflow.parse, workflow_lines)})

    print(f"Part 2: {workflow_map.count_ways()}")


if __name__ == "__main__":
    main()
