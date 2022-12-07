#!/usr/bin/env python
from functools import reduce

from pydantic import BaseModel
from toolz import merge_with, concat, valmap, compose


class Move(BaseModel):
    count: int
    from_no: int
    to_no: int

    @classmethod
    def from_line(cls, line: str) -> "Move":
        _, count, _, from_no, _, to_no = line.split()
        return cls(count=int(count), from_no=int(from_no), to_no=int(to_no))

    def __str__(self):
        return f"move {self.count} from {self.from_no} to {self.to_no}"


def top_items(crate_config: dict[int, list[str]]) -> str:
    def top_item(items: list[str]) -> str:
        if items:
            return items[-1]
        return " "

    return "".join([top_item(items) for items in crate_config.values()])


def read_input() -> tuple[list[str], int, list[Move]]:
    with open("input.txt", "r") as file:
        lines = []
        for line in file:
            if not line.strip():
                break
            lines.append(line.rstrip())
        # Last line is the column numbers
        column_count = int(lines[-1].split()[-1])
        lines = lines[:-1]

        moves = []
        for line in file:
            moves.append(Move.from_line(line))
    return lines, column_count, moves


def parse_crate_line(line: str, column_count: int) -> dict[int, str]:
    crate_line = {}
    for column in range(1, column_count + 1):
        # 1 -> 1
        # 2 -> 5
        # 3 -> 9
        # 4 -> 13
        offset = 1 + 4 * (column - 1)
        if offset < len(line) and line[offset] != " ":
            crate_line[column] = line[offset]
    return crate_line


def parse_crate_config(lines: list[str], column_count) -> dict[int, list[str]]:
    crate_lines = [parse_crate_line(line, column_count) for line in lines]
    crate_config = merge_with(compose(list, reversed, list, concat), *crate_lines)
    # e.g. {1: ['Z', 'N'], 2: ['M', 'C', 'D'], 3: ['P']}
    return dict(sorted(crate_config.items()))  # This just sorts the keys


def apply_move(crate_config: dict[int, list[str]], move: Move) -> dict[int, list[str]]:
    from_items = crate_config[move.from_no]
    to_items = crate_config[move.to_no]
    crate_config[move.from_no] = from_items[: -move.count]
    crate_config[move.to_no] = to_items + list(reversed(from_items[-move.count :]))
    return crate_config


def apply_moves(crate_config: dict[int, list[str]], moves: list[Move]) -> dict[int, list[str]]:
    return reduce(apply_move, moves, crate_config)


def main():
    lines, column_count, moves = read_input()
    crate_config = parse_crate_config(lines, column_count)
    # print(crate_config)
    # print(moves)
    print(top_items(crate_config))
    new_crate_config = apply_moves(crate_config, moves)
    # print(new_crate_config)
    print(top_items(new_crate_config))


if __name__ == "__main__":
    main()
