#!/usr/bin/env python
from typing import TypeAlias

from numpy import array


def read_commands() -> list[tuple[str, int]]:
    with open("input.txt", "r") as file:
        lines = [line.split() for line in file]
    return [(line[0], int(line[1])) for line in lines]


# A position is represented by an (x,y) vector
Position: TypeAlias = array
# The set of all tail positions
TailPositions: TypeAlias = set[tuple[int, int]]
# state is (rope, tail_positions). `rope` is a list of positions, first element is head, last element is tail.
State: TypeAlias = tuple[list[Position], TailPositions]


def move_knot(new_first_knot: Position, second_knot: Position) -> tuple[Position, array]:
    """Move first_know according to first_knot_offset. Returns new_second_knot"""
    diff = new_first_knot - second_knot
    if (abs(diff) <= array([1, 1])).all():
        new_second_knot = second_knot
    elif diff[0] > 1 and abs(diff[1]) <= 1:   # moved right
        new_second_knot = new_first_knot + array([-1, 0])
    elif diff[0] < -1 and abs(diff[1]) <= 1:  # moved left
        new_second_knot = new_first_knot + array([1, 0])
    elif abs(diff[0]) <= 1 and diff[1] > 1:   # moved up
        new_second_knot = new_first_knot + array([0, -1])
    elif abs(diff[0]) <= 1 and diff[1] < -1:  # moved down
        new_second_knot = new_first_knot + array([0, 1])
    elif diff[0] > 1 and diff[1] > 1:    # moved up-right
        new_second_knot = new_first_knot + array([-1, -1])
    elif diff[0] > 1 and diff[1] < -1:   # moved down-right
        new_second_knot = new_first_knot + array([-1, 1])
    elif diff[0] < -1 and diff[1] > 1:   # moved up-left
        new_second_knot = new_first_knot + array([1, -1])
    elif diff[0] < -1 and diff[1] < -1:  # moved down-left
        new_second_knot = new_first_knot + array([1, 1])
    else:
        raise ValueError("Invalid move")

    return new_second_knot


def move_head(state: State, head_offset: array) -> State:
    """Move the head in the given direction.
    Returns new state (new_rope, new_tail_positions)
    """
    rope, tail_positions = state

    new_rope = []
    new_first_knot = rope[0] + head_offset
    new_rope.append(new_first_knot)
    for knot in rope[1:]:
        new_second_knot = move_knot(new_first_knot, knot)
        new_rope.append(new_second_knot)
        new_first_knot = new_second_knot

    new_tail_positions = tail_positions.union({tuple(new_rope[-1])})
    return new_rope, new_tail_positions


def process_command(state: State, command: tuple[str, int]) -> State:
    """Process a command (direction, distance)
    Returns new state (head_position, tail_position, tail_positions)
    """
    direction, distance = command
    offset_map = {
        "U": array([0, 1]),
        "D": array([0, -1]),
        "R": array([1, 0]),
        "L": array([-1, 0]),
    }
    head_offset = offset_map[direction]
    for _ in range(distance):
        new_state = move_head(state, head_offset)
        # print("\n*** After move ***", direction)
        # print_state(new_state)
        state = new_state

    return state


def process_commands(state: State, commands: list[tuple[str, int]]) -> State:
    """Process a list of commands
    Returns final state (head_position, tail_position, tail_positions)
    """
    new_state = state
    for command in commands:
        new_state = process_command(state, command)
        # print("\n*** After command ***", command)
        # print_state(new_state)
        state = new_state

    return new_state


def print_state(state: State):
    # Used for debugging
    rope, tail_positions = state
    print(" --- State ---")
    for i, knot in enumerate(rope):
        print(f"knot {i}: ", knot)
    # print("tail_positions:", tail_positions)


def main():
    commands = read_commands()
    rope = [array([1, 1]) for _ in range(10)]
    initial_state = (rope, set())
    final_state = process_commands(initial_state, commands)
    print("*** Final state ***")
    print_state(final_state)
    _, tail_positions = final_state
    print("Tail positions:", sorted(list(tail_positions)))
    print(len(tail_positions))


if __name__ == "__main__":
    main()
