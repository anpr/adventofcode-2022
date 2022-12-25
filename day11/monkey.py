#!/usr/bin/env python
import re
import sys
from pprint import pprint

from pydantic import BaseModel
from toolz import partitionby
from collections import deque


class Monkey(BaseModel):
    monkey_no: int
    items: deque[
        list[int]
        ]  # A single item is a list of worry levels modulo test_divisible of the respective monkey
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

    def apply_operation(self, monkeys, worries: list[int]) -> list[int]:
        # print(f"   apply_operation to worry {worry}")
        def apply_operation_to_single_worry(divisible: int, worry: int):
            val1, op, val2 = self.operation.split()
            value1 = self.resolve_val(val1, worry)
            value2 = self.resolve_val(val2, worry)
            if op == "+":
                return (value1 + value2) % divisible
            elif op == "*":
                return (value1 * value2) % divisible
            raise ValueError(f"Unknown operation {self.operation}")

        return [
            apply_operation_to_single_worry(divisible=monkey.test_divisible, worry=worry)
            for monkey, worry in zip(monkeys, worries)
        ]

    def test_worry_level(self, worries: list[int]) -> bool:
        if worries[self.monkey_no] % self.test_divisible == 0:
            return True
        return False


def read_lines() -> list[str]:
    if len(sys.argv) <= 1:
        raise ValueError("Please provide a file path")
    with open(sys.argv[1], "r") as file:
        lines = [line.strip() for line in file]
    return lines


def read_monkey(monkey_lines: tuple[str, str, str, str, str, str], monkey_count: int) -> Monkey:
    monkey_no_str, starting_items_str, operation_str, test_str, true_str, false_str = monkey_lines
    return Monkey(
        monkey_no=re.search(r"Monkey (\d+):", monkey_no_str).group(1),
        items=deque(
            map(
                lambda item_str: [int(item_str.strip())] * monkey_count,
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
        item = monkey.items.popleft()
        p(f"  Monkey inspects item with a worry level of {item}")
        monkey.inspect_count += 1
        worries = monkey.apply_operation(monkeys=monkeys, worries=item)
        p(f"  Worry level: {worries}")
        # worry = int(worry / 3)
        # p(f"  Bored worry: {worries}")
        test_result = monkey.test_worry_level(worries=worries)
        p(f"  Current worry level is divisible by {monkey.test_divisible}: {test_result}")
        if test_result:
            p(f"  Item with worry level {worries} is thrown to {monkey.true_monkey}")
            monkeys[monkey.true_monkey].items.append(worries)
        else:
            p(f"  Item with worry level {worries} is thrown to {monkey.false_monkey}")
            monkeys[monkey.false_monkey].items.append(worries)

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
    monkey_count = len(all_monkey_lines)
    monkeys = [read_monkey(monkey_lines, monkey_count) for monkey_lines in all_monkey_lines]
    pprint(monkeys)
    for i in range(10000):
        print(f"\n*** Round {i}")
        if round(i % 10 == 0):
            pprint(monkeys)
        monkeys = make_round(monkeys)

    print(monkey_business(monkeys))


if __name__ == "__main__":
    main()
