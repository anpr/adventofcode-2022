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
# state is (head_position, tail_position, tail_positions)
State: TypeAlias = tuple[Position, Position, TailPositions]


def move(state: State, direction: str) -> State:
    """Move the head in the given direction.
    Returns new state (head_position, tail_position, tail_positions)
    """
    head_position, tail_position, tail_positions = state

    offset_map = {
        "U": array([0, 1]),
        "D": array([0, -1]),
        "R": array([1, 0]),
        "L": array([-1, 0]),
    }
    offset = offset_map[direction]

    new_head_position = head_position + offset
    diff = new_head_position - tail_position
    if (abs(diff) <= array([1, 1])).all():
        new_tail_position = tail_position
    elif diff[0] > 1:  # moved right
        new_tail_position = new_head_position + array([-1, 0])
    elif diff[0] < -1:  # moved left
        new_tail_position = new_head_position + array([1, 0])
    elif diff[1] > 1:  # moved up
        new_tail_position = new_head_position + array([0, -1])
    elif diff[1] < -1:  # moved down
        new_tail_position = new_head_position + array([0, 1])
    else:
        raise ValueError("Invalid move")

    new_tail_positions = tail_positions.union({tuple(new_tail_position)})
    return new_head_position, new_tail_position, new_tail_positions


def process_command(state: State, command: tuple[str, int]) -> State:
    """Process a command (direction, distance)
    Returns new state (head_position, tail_position, tail_positions)
    """
    direction, distance = command
    for _ in range(distance):
        new_state = move(state, direction)
        # print("\n*** After move ***", direction)
        # print_state(new_state)
        state = new_state

    return state


def process_commands(state: State, commands: list[tuple[str, int]]) -> State:
    """Process a list of commands
    Returns final state (head_position, tail_position, tail_positions)
    """
    for command in commands:
        state = process_command(state, command)
    return state


def print_state(state: State):
    # Used for debugging
    head_position, tail_position, tail_positions = state
    print(" --- State ---")
    print("head_position: ", head_position)
    print("tail_position: ", tail_position)
    # print("tail_positions:", tail_positions)


def main():
    commands = read_commands()
    initial_state = (array([0, 0]), array([0, 0]), set())
    final_state = process_commands(initial_state, commands)
    # print("*** Final state ***")
    # print_state(final_state)
    tail_positions = {tuple(position) for position in final_state[2]}
    # print("Tail positions:", tail_positions)
    print(len(tail_positions))


if __name__ == "__main__":
    main()
