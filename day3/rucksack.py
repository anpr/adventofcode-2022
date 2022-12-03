#!/usr/bin/env python
from toolz import partition


def read_rucksacks() -> list[str]:
    with open("input.txt", "r") as file:
        lines = [line.rstrip() for line in file]

    return lines


def priority(item: str) -> int:
    assert len(item) == 1
    if item.islower():
        return ord(item) - ord("a") + 1
    return ord(item) - ord("A") + 27


def rucksack_to_compartments(rucksack: str) -> tuple[str, str]:
    compartment_count = int(len(rucksack) / 2)

    first_compartment = rucksack[:compartment_count]
    second_compartment = rucksack[compartment_count:]
    return first_compartment, second_compartment


def to_charset(rucksack: str) -> set[str]:
    return {c for c in rucksack}


def compartments_to_common_char(compartments: tuple[str, str]) -> set[str]:
    first_compartment, second_compartment = compartments

    first_compartment_charset = to_charset(first_compartment)
    second_compartment_charset = to_charset(second_compartment)
    return first_compartment_charset & second_compartment_charset


def rucksack_to_priority_of_common_char(rucksack) -> int:
    return sum(
        priority(item)
        for item in compartments_to_common_char(rucksack_to_compartments(rucksack))
    )


def sum_of_priority_of_common_char(rucksacks: list[str]) -> int:
    scores = [rucksack_to_priority_of_common_char(rucksack) for rucksack in rucksacks]
    print(scores)
    return sum(scores)


### Part 2


def get_groups(rucksacks: list[str]) -> list[tuple[str]]:
    return list(partition(3, rucksacks))


def common_item_of_group(group: tuple[str]) -> set[str]:
    first_rucksack, second_rucksack, third_rucksack = group
    first_compartment_charset = to_charset(first_rucksack)
    second_compartment_charset = to_charset(second_rucksack)
    third_compartment_charset = to_charset(third_rucksack)
    return (
        first_compartment_charset
        & second_compartment_charset
        & third_compartment_charset
    )


def group_priority(group: tuple[str]) -> int:
    return sum(priority(item) for item in common_item_of_group(group))


def sum_group_priorities(rucksacks: list[str]) -> int:
    groups = get_groups(rucksacks)
    group_priorities = [group_priority(group) for group in groups]
    print(group_priorities)
    return sum(group_priorities)


def main():
    rucksacks = read_rucksacks()
    print(sum_of_priority_of_common_char(rucksacks))


def main2():
    rucksacks = read_rucksacks()
    print(sum_group_priorities(rucksacks))


if __name__ == "__main__":
    main2()
