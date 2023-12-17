from collections import defaultdict


def hsh(s: str) -> int:
    cur = 0
    for c in s:
        cur += ord(c)
        cur *= 17
        cur %= 256
    return cur


def main():
    instructions = input().strip().split(",")
    print(f"Part 1: {sum(map(hsh, instructions))}")

    boxes = defaultdict(list)
    focals = {}
    for step in instructions:
        if step.endswith("-"):
            label = step.removesuffix("-")
            if label in boxes[hsh(label)]:
                boxes[hsh(label)].remove(label)
        else:
            label, focal = step.split("=")
            focals[label] = int(focal)
            if label not in boxes[hsh(label)]:
                boxes[hsh(label)].append(label)

    power = 0
    for box_num, box in boxes.items():
        for slot, label in enumerate(box):
            power += (box_num + 1) * (slot + 1) * focals[label]
    print(f"Part 2: {power}")


if __name__ == "__main__":
    main()
