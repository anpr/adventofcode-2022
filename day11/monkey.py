#!/usr/bin/env python
import re
import sys
from pprint import pprint

from pydantic import BaseModel
from toolz import partitionby


class Monkey(BaseModel):
    monkey_no: int
    items: list[int]
    test_divisible: int
    operation: str
    true_monkey: int
    false_monkey: int
    inspect_count: int

    @staticmethod
    def resolve_val(val: str, worry: int) -> int:
        if val == "old":
            return worry
        return int(val)

    def apply_operation(self, worry: int) -> int:
        val1, op, val2 = self.operation.split()
        value1 = self.resolve_val(val1, worry)
        value2 = self.resolve_val(val2, worry)
        if op == "+":
            return value1 + value2
        elif op == "*":
            return value1 * value2
        raise ValueError(f"Unknown operation {self.operation}")

    def test_worry_level(self, worry: int) -> bool:
        if worry % self.test_divisible == 0:
            return True
        return False


def read_lines() -> list[str]:
    if len(sys.argv) <= 1:
        raise ValueError("Please provide a file path")
    with open(sys.argv[1], "r") as file:
        lines = [line.strip() for line in file]
    return lines


def read_monkey(monkey_lines: tuple[str, str, str, str, str, str]) -> Monkey:
    monkey_no_str, starting_items_str, operation_str, test_str, true_str, false_str = monkey_lines
    return Monkey(
        monkey_no=re.search(r"Monkey (\d+):", monkey_no_str).group(1),
        items=list(
            map(
                lambda item_str: int(item_str.strip()),
                starting_items_str.split(maxsplit=2)[2:][0].split(","),
            )
        ),
        operation=re.search(r"Operation: new = (.*)$", operation_str).group(1),
        test_divisible=re.search(r"Test: divisible by (\d+)", test_str).group(1),
        true_monkey=re.search(r"If true: throw to monkey (\d+)", true_str).group(1),
        false_monkey=re.search(r"If false: throw to monkey (\d+)", false_str).group(1),
        inspect_count=0,
    )


def p(s: str):
    if False:
        print(s)


def make_turn(monkeys: list[Monkey], monkey: Monkey) -> list[Monkey]:
    p(f"Monkey {monkey.monkey_no}")
    while monkey.items:
        item = monkey.items.pop(0)
        p(f"  Monkey inspects item with a worry level of {item}")
        monkey.inspect_count += 1
        worry = monkey.apply_operation(worry=item)
        p(f"  Worry level: {worry}")
        # worry = int(worry / 3)
        p(f"  Bored worry: {worry}")
        test_result = monkey.test_worry_level(worry=worry)
        p(f"  Current worry level is divisible by {monkey.test_divisible}: {test_result}")
        if test_result:
            p(f"  Item with worry level {worry} is thrown to {monkey.true_monkey}")
            monkeys[monkey.true_monkey].items.append(worry)
        else:
            p(f"  Item with worry level {worry} is thrown to {monkey.false_monkey}")
            monkeys[monkey.false_monkey].items.append(worry)

    return monkeys


def make_round(monkeys: list[Monkey]) -> list[Monkey]:
    for monkey in monkeys:
        monkeys = make_turn(monkeys, monkey)

    return monkeys


def monkey_business(monkeys: list[Monkey]) -> int:
    sorted_inspect_counts = sorted([monkey.inspect_count for monkey in monkeys], reverse=True)
    print("sorted_inspect_count: ", sorted_inspect_counts)
    return sorted_inspect_counts[0] * sorted_inspect_counts[1]


def main():
    lines = read_lines()
    all_monkey_lines = list(
        filter(
            lambda monkey_lines: monkey_lines != ("",), partitionby(lambda line: line == "", lines)
        )
    )
    monkeys = [read_monkey(monkey_lines) for monkey_lines in all_monkey_lines]
    for i in range(10000):
        print(f"\n*** Round {i}")
        monkeys = make_round(monkeys)

    print(monkey_business(monkeys))


if __name__ == "__main__":
    main()
