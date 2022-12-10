#!/usr/bin/env python
from toolz import sliding_window


def read_input() -> str:
    with open("input.txt", "r") as file:
        lines = [line for line in file]
    return lines[0]


def first_marker(line: str) -> int:
    fours = list(sliding_window(4, line))
    for i, four in enumerate(fours):
        if len(set(four)) == 4:
            return i + 4


def start_of_message_marker(line: str) -> int:
    fours = list(sliding_window(14, line))
    for i, four in enumerate(fours):
        if len(set(four)) == 14:
            return i + 14


def main():
    line = read_input()
    # print(first_marker(line))
    print(start_of_message_marker(line))


if __name__ == "__main__":
    main()
