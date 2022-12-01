#!/usr/bin/env python


def read_calories() -> list[list[int]]:
    calories = []
    elf_calories = []
    with open("input.txt") as f:
        for line in f:
            if not line.strip():
                calories.append(elf_calories)
                elf_calories = []
            else:
                elf_calories.append(int(line.strip()))
    return calories


def sum_calories(calories: list[list[int]]) -> list[int]:
    return [sum(elf_calories) for elf_calories in calories]


def find_max(calories: list[list[int]]) -> int:
    return max(sum_calories(calories))


def top_three(calories: list[list[int]]) -> int:
    sorted_calories = sorted(sum_calories(calories), reverse=True)
    print("**** sorted_calories ****")
    print(sorted_calories)
    return sum(sorted_calories[:3])


def print_max() -> None:
    calories = read_calories()
    print("\n\n********** calories **********")
    print(calories)
    print("\n\n********** find_max **********")
    print(find_max(calories))


def print_top_three() -> None:
    calories = read_calories()
    print("\n\n********** top_three **********")
    print(top_three(calories))


if __name__ == "__main__":
    print_top_three()
