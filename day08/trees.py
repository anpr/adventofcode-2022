#!/usr/bin/env python
def read_lines() -> list[str]:
    with open("input.txt", "r") as file:
        lines = [line for line in file]
    return lines


def to_grid(lines: list[str]) -> list[list[int]]:
    return [list(map(int, line.strip())) for line in lines]


def grid_size(grid: list[list[int]]) -> int:
    return len(grid)


def is_visible(grid: list[list[int]], x: int, y: int) -> bool:
    height = grid[y][x]
    size = grid_size(grid)

    left = [grid[y][i] for i in range(x - 1, -1, -1)]
    right = [grid[y][i] for i in range(x + 1, size)]
    down = [grid[j][x] for j in range(y + 1, size)]
    up = [grid[j][x] for j in range(y - 1, -1, -1)]

    if all([height > h for h in left]):
        return True
    if all([height > h for h in right]):
        return True
    if all([height > h for h in down]):
        return True
    if all([height > h for h in up]):
        return True
    return False


def count_visible(grid: list[list[int]]) -> int:
    size = grid_size(grid)
    count = 0
    for x in range(size):
        for y in range(size):
            if is_visible(grid, x, y):
                count += 1
    return count


def num_visible_trees(heights: list[int], height: int) -> int:
    for i, h in enumerate(heights):
        if h >= height:
            return i + 1
    return len(heights)


def scenic_score(grid: list[list[int]], x: int, y: int) -> int:
    height = grid[y][x]
    size = grid_size(grid)

    left = [grid[y][i] for i in range(x - 1, -1, -1)]
    right = [grid[y][i] for i in range(x + 1, size)]
    down = [grid[j][x] for j in range(y + 1, size)]
    up = [grid[j][x] for j in range(y - 1, -1, -1)]

    to_left = num_visible_trees(left, height)
    to_right = num_visible_trees(right, height)
    to_down = num_visible_trees(down, height)
    to_up = num_visible_trees(up, height)

    # print(height)
    # print("left", left)
    # print("right", right)
    # print("down", down)
    # print("up", up)
    # print("to_left", to_left)
    # print("to_right", to_right)
    # print("to_down", to_down)
    # print("to_up", to_up)

    return to_left * to_right * to_down * to_up


def max_scenic_score(grid: list[list[int]]) -> int:
    size = grid_size(grid)
    max_score = 0
    for x in range(size):
        for y in range(size):
            score = scenic_score(grid, x, y)
            if score > max_score:
                max_score = score
    return max_score


def main():
    lines = read_lines()
    grid = to_grid(lines)
    # print(grid)
    # print(count_visible(grid))
    print(scenic_score(grid, 2, 1))
    print(max_scenic_score(grid))


if __name__ == "__main__":
    main()
