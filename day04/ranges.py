#!/usr/bin/env python
def read_intervals() -> list[str]:
    with open("input.txt", "r") as file:
        lines = [line.rstrip() for line in file]

    return lines


def parse_intervals(interval: str) -> tuple[set[int], set[int]]:
    first, second = interval.split(",")
    first_range = set(range(int(first.split("-")[0]), int(first.split("-")[1]) + 1))
    second_range = set(range(int(second.split("-")[0]), int(second.split("-")[1]) + 1))
    return first_range, second_range


def is_contained(first: set[int], second: set[int]) -> int:
    if first.issubset(second):
        return 1
    if second.issubset(first):
        return 1
    return 0


def overlaps(first: set[int], second: set[int]) -> int:
    if first & second:
        return 1
    return 0


def main():
    intervals = read_intervals()
    sum = 0
    for interval in intervals:
        first, second = parse_intervals(interval)
        sum += overlaps(first, second)
        print(overlaps(first, second))
    print("********")
    print(sum)


if __name__ == "__main__":
    main()
