#!/usr/bin/env python
from pprint import pprint


def read_strategy() -> list[tuple[str]]:
    with open("input.txt", "r") as file:
        lines = [line.rstrip() for line in file]

    return [tuple(line.split()) for line in lines]


def round_to_score(play: tuple[str]) -> int:
    enemy = {
        "A": "Rock",
        "B": "Paper",
        "C": "Scissors",
    }
    you = {
        "X": "Rock",
        "Y": "Paper",
        "Z": "Scissors",
    }
    shape_score = {
        "Rock": 1,
        "Paper": 2,
        "Scissors": 3,
    }
    win_score = {
        "lost": 0,
        "draw": 3,
        "won": 6,
    }
    win_score_key = {
        ("Rock", "Rock"): "draw",
        ("Rock", "Paper"): "won",
        ("Rock", "Scissors"): "lost",
        ("Paper", "Rock"): "lost",
        ("Paper", "Paper"): "draw",
        ("Paper", "Scissors"): "won",
        ("Scissors", "Rock"): "won",
        ("Scissors", "Paper"): "lost",
        ("Scissors", "Scissors"): "draw",
    }
    return shape_score[you[play[1]]] + win_score[win_score_key[enemy[play[0]], you[play[1]]]]


def round_to_score_part2(play: tuple[str]) -> int:
    enemy_code = {
        "A": "Rock",
        "B": "Paper",
        "C": "Scissors",
    }
    you_code = {
        "X": "lost",
        "Y": "draw",
        "Z": "won",
    }
    you = {
        ("Rock", "lost"): "Scissors",
        ("Rock", "draw"): "Rock",
        ("Rock", "won"): "Paper",
        ("Paper", "lost"): "Rock",
        ("Paper", "draw"): "Paper",
        ("Paper", "won"): "Scissors",
        ("Scissors", "lost"): "Paper",
        ("Scissors", "draw"): "Scissors",
        ("Scissors", "won"): "Rock",
    }
    shape_score = {
        "Rock": 1,
        "Paper": 2,
        "Scissors": 3,
    }
    win_score = {
        "lost": 0,
        "draw": 3,
        "won": 6,
    }
    won_key = you_code[play[1]]
    your_play = you[(enemy_code[play[0]], won_key)]
    return shape_score[your_play] + win_score[won_key]


def score_strategy(strategy: list[tuple[str]]) -> int:
    scores = [round_to_score(play) for play in strategy]
    print(scores)
    return sum(scores)


def score_strategy_part2(strategy: list[tuple[str]]) -> int:
    scores = [round_to_score_part2(play) for play in strategy]
    print(scores)
    return sum(scores)


pprint(score_strategy_part2(read_strategy()))
