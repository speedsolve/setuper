#!/usr/bin/env python3

import os
import re
import random
import sys


LOCK_FILE = "lock.txt"
ALGORISM_FILE = "algorism.txt"


def run():
    lock_list = []
    is_lock_file = os.path.isfile(LOCK_FILE)
    if is_lock_file:
        with open(LOCK_FILE, encoding="utf-8") as f:
            lock_list = list(map(int, f.read().splitlines()))

    is_alogrism_file = os.path.isfile(ALGORISM_FILE)
    if not is_alogrism_file:
        print("algorism.txtが存在しません。")
        exit()

    quetions = []
    with open(ALGORISM_FILE, encoding="utf-8") as f:
        algo_list = f.read().splitlines()
        for algo in algo_list:

            if is_natural(algo):
                c = algo.strip().split()
            else:
                setup_text = None
                if contain_setup(algo):
                    setup_text = setup(algo)
                    algos = takeoff_for_setup(algo).split(",")
                else:
                    algos = takeoff(algo).split(",")
                c = convert(algos, setup_text)

            f = list(map(reverse_word, c[::-1]))
            # 逆も追加
            quetions.append(" ".join(c))
            quetions.append(" ".join(f))

    for lock_id in lock_list:
        quetions.pop(lock_id)

    for _ in range(run_count):
        rand = random.choice(quetions)
        index = quetions.index(rand)

        print(str(index) + ": " + rand)


def is_natural(text):
    return "[" not in text


def contain_setup(text):
    return ":" in text


def setup(text):
    m = re.findall(r"\[(.*?):", text)
    if m is None:
        return None
    return m[0]


def takeoff(text):
    m = re.findall(r"\[(.*?)\]", text)
    if m is None:
        return None
    return m[0]


def takeoff_for_setup(text):
    m = re.findall(r"\[.*?\[(.*?)\]", text)
    if m is None:
        return None
    return m[0]


def reverse_word(word):
    if "2" in word:
        return word
    if "'" in word:
        return word.replace("'", "")
    else:
        return word + "'"


def convert(algos, setup=None):
    insert = algos[0].strip()
    interchange = algos[1].strip()

    algo = (
        insert.split()
        + interchange.split()
        + list(map(reverse_word, insert.split()))[::-1]
        + list(map(reverse_word, interchange.split()))[::-1]
    )
    if setup:
        setup = setup.strip()
        algo = setup.split() + algo + list(map(reverse_word, setup.split()))[::-1]

    return algo


def lock():
    with open(LOCK_FILE, mode="a") as f:
        f.write(str(lock_id) + "\n")


if __name__ == "__main__":
    action = sys.argv[1]
    if action == "run":
        run_count = int(sys.argv[2])
        run()
    elif action == "lock":
        lock_id = int(sys.argv[2])
        lock()
