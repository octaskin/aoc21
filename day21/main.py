#!/usr/bin/env python

from pathlib import Path

import numpy as np


def read_input(fname):
    with open(Path(__file__).parent.joinpath(fname), "r") as f:
        return f.read()


def parse_input(inp: str):
    return [int(i.split(": ")[1]) for i in inp.split("\n")[:-1]]


def part1(input):
    posn = [i - 1 for i in input]
    score = [0, 0]
    t = 0  # turn
    while not sum([i >= 1000 for i in score]):
        i = t % 2  # player ind
        roll = 3 * (3 * t + 2)
        posn[i] = (posn[i] + roll) % 10
        score[i] += posn[i] + 1
        t += 1
        # print(f"{roll=}")
        # print(f"{posn[i]=},{score[i]=}")
    print(f"Result:{t*3*min(score)}")


def part2(initial_posn):
    def one_round(mat: np.array):
        res_mat = np.zeros_like(mat)
        won = 0
        # Could be done without the second loop since prob. end posns are
        # deterministic
        for pnt_i, pos_i in zip(*np.nonzero(mat)):
            count = mat[pnt_i, pos_i]
            distrb = np.array([1, 3, 6, 7, 6, 3, 1], dtype=int) * count
            for move, count in zip(list(range(3, 10)), distrb):
                pos_new = (pos_i + move) % 10
                pnt_new = pnt_i + 1 + pos_new
                if pnt_new > 20:
                    won += count
                else:
                    res_mat[pnt_new, pos_new] += count
        return res_mat, won

    players = np.zeros(shape=(21, 10, 2), dtype=int)  # scores X posn matrix
    players[0, initial_posn[0] - 1, 0] += 1
    players[0, initial_posn[1] - 1, 1] += 1
    wins = [0, 0]
    while np.any(players > 0):
        for i in range(2):
            res, won = one_round(players[..., i])
            players[..., i] = res
            # print(f"Player {i} played")
            # print(players[..., i])
            # print(f"Won in:{won}")
            # print(f"Total universes:{np.sum(players, axis=(0,1))}")
            wins[i] += won * np.sum(players[..., abs(1 - i)])
            # print(f"{global_wins=}")
            # _ = input("") # to debug each play
    print(f"Result:{max(wins)}")


def main():
    input = parse_input(read_input("input.txt"))
    # part1(input)
    part2(input)


if __name__ == "__main__":
    main()
