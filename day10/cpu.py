#!/usr/bin/env python

from pydantic import BaseModel


def read_commands() -> list[list[str]]:
    with open("input.txt", "r") as file:
        lines = [line.split() for line in file]
    return lines


class State(BaseModel):
    command_stack: list[list[str]]
    cycle: int
    command_cycle: int
    x: int
    # signal_strength: int
    sum_signal_strength: int

    def current_command(self) -> list[str]:
        if len(self.command_stack) == 0:
            return []
        return self.command_stack[0]

    def __str__(self):
        return (
            f"command={self.current_command()} cycle={self.cycle} command_cycle={self.command_cycle} "
            f"x={self.x}, sum={self.sum_signal_strength}"
        )


def next_sum_signal_strength(state: State) -> int:
    if (state.cycle - 20) % 40 == 0:
        signal_strength = state.x * state.cycle
        print("** signal_strength=", signal_strength)
        return state.sum_signal_strength + signal_strength
    else:
        return state.sum_signal_strength


def process_cycle(state: State) -> tuple[State, bool]:
    durations = {
        "noop": 1,
        "addx": 2,
    }
    if len(state.command_stack) == 0 or state.cycle == 220:
        return state, False

    command = state.command_stack[0]
    new_state = state
    new_state.cycle += 1
    new_state.command_cycle += 1
    is_command_done = new_state.command_cycle > durations[command[0]]
    if command[0] == "noop":
        pass
    elif command[0] == "addx":
        v = int(command[1])
        if is_command_done:
            new_state.x += v
    else:
        raise ValueError("Invalid command")

    new_state.sum_signal_strength = next_sum_signal_strength(state)
    if is_command_done:
        new_state.command_stack = new_state.command_stack[1:]
        new_state.command_cycle = 1

    return new_state, True


def main():
    commands = read_commands()
    initial_state = State(
        command_stack=commands,
        x=1,
        cycle=1,
        command_cycle=1,
        sum_signal_strength=0,
    )
    state = initial_state
    while True:
        print("state: ", state)
        state, is_done = process_cycle(state)
        if not is_done:
            break

    print("\nFinal state: ", state)
    print(state.sum_signal_strength)


if __name__ == "__main__":
    main()
