#!/usr/bin/env python
from collections import defaultdict
from functools import reduce
from pprint import pprint
from typing import TypeAlias, DefaultDict

from pydantic import BaseModel
from toolz import valfilter


def read_lines() -> list[str]:
    with open("input.txt", "r") as file:
        lines = [line for line in file]
    return lines


class File(BaseModel):
    name: str
    size: int


# A directory is represented by a tuple of strings, representing the path
Dir: TypeAlias = tuple[str, ...]
# dirs to list of files, with name and size
FileMap: TypeAlias = DefaultDict[Dir, list[File]]
# dirs to list of other dirs
DirMap: TypeAlias = DefaultDict[Dir, list[Dir]]

State: TypeAlias = tuple[Dir, FileMap, DirMap]


def lines_to_commands(lines: list[str]) -> list[tuple[str, list[str]]]:
    """lines to list of (command_line, output_lines)"""
    commands = []
    command = None
    for line in lines:
        if line.startswith("$"):
            if command:
                commands.append(command)
            command = (line.strip(), [])
        else:
            command[1].append(line.strip())
    if command:
        commands.append(command)
    return commands


def process_output_line(state: State, output_line: str) -> State:
    """Process a line of output from a ls command
    Returns new state (pwd, file_map, dir_map)
    """
    pwd, file_map, dir_map = state
    if output_line.startswith("dir"):
        new_dir = pwd + (output_line.split()[1],)
        dir_map[pwd].append(new_dir)
        dir_map[new_dir] = []
        file_map[new_dir] = []
    else:
        new_file = File(name=output_line.split()[1], size=int(output_line.split()[0]))
        file_map[pwd].append(new_file)
    return pwd, file_map, dir_map


def process_output_lines(state: State, output_lines: list[str]) -> State:
    """Process the output of a command
    Returns (file_map, dir_map)
    """
    return reduce(process_output_line, output_lines, state)


def apply_command(state: State, command: tuple[str, list[str]]) -> State:
    """Apply a command to file_map and dir_map
    Returns (new_pwd, new_file_map, new_dir_map)
    """
    pwd, file_map, dir_map = state
    command_line, output_lines = command
    if command_line.split()[1] == "cd":
        if command_line.split()[2] == "..":
            new_pwd = pwd[:-1]
        elif command_line.split()[2] == "/":
            new_pwd = ("/",)
        else:
            new_pwd = pwd + (command_line.split()[2],)
        new_file_map = file_map
        new_dir_map = dir_map
    elif command_line.split()[1] == "ls":
        new_state = process_output_lines(state, output_lines)
        new_pwd, new_file_map, new_dir_map = new_state
    else:
        raise ValueError(f"Unknown command {command_line}")
    # print_state((new_pwd, new_file_map, new_dir_map))
    return new_pwd, new_file_map, new_dir_map


def apply_commands(state: State, commands: list[tuple[str, list[str]]]) -> State:
    """Apply a list of commands to file_map and dir_map
    Returns (new_pwd, new_file_map, new_dir_map)
    """
    return reduce(apply_command, commands, state)


def print_state(state: State):
    # Used for debugging
    pwd, file_map, dir_map = state
    print("pwd:", pwd)
    print("file_map:")
    pprint(file_map)
    print("dir_map:")
    pprint(dir_map)


def size_of_dir(state: State, directory: Dir) -> int:
    """Return the size of a directory"""
    _, file_map, dir_map = state
    return sum([file.size for file in file_map.get(directory, [])]) + sum(
        [size_of_dir(state, subdir) for subdir in dir_map.get(directory, [])]
    )


def get_size_map(state: State) -> dict[Dir, int]:
    _, file_map, dir_map = state
    return {directory: size_of_dir(state, directory) for directory in dir_map.keys()}


# part 1
def sum_of_sizes_up_to(state: State) -> int:
    size_map = get_size_map(state)
    return sum(valfilter(lambda size: size <= 100000, size_map).values())


def size_of_dir_to_delete(state: State) -> int:
    _, file_map, dir_map = state
    total_used_space = size_of_dir(state, ("/",))
    unused_space = 70000000 - total_used_space
    min_to_delete = 30000000 - unused_space

    min_size_map = valfilter(lambda size: size >= min_to_delete, get_size_map(state))
    print("\n**** min_size_map:\n", min_size_map)
    return min(min_size_map.values())


def main():
    lines = read_lines()
    commands = lines_to_commands(lines)
    # pprint(commands)
    initial_state = (("/",), defaultdict(list), defaultdict(list))
    state = apply_commands(initial_state, commands)
    print("\n**** Final state:")
    print_state(state)
    # print("sum of size up to 100000: ", sum_of_sizes_up_to(state))
    print("size of dir to delete: ", size_of_dir_to_delete(state))


if __name__ == "__main__":
    main()
