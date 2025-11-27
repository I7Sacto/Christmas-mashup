#!/usr/bin/env python3
import os
import time
import random
import shutil

# ===== TERMINAL SIZE =====
ROWS, COLS = shutil.get_terminal_size((27, 143))

# ===== SETTINGS =====
TREE_HEIGHT = 18             # велика ялинка
TREE_WIDTH = TREE_HEIGHT*2   # ширина
TREE_X = 5
TEXT_X = TREE_X + TREE_WIDTH + 8
DELAY = 0.12

# Плавні кольори
colors = [31, 32, 33, 34, 35, 36, 91, 92, 93, 94, 95, 96]

# ===== TEXTS =====
texts = [
    "🌟 CONGRATULATION!!! 🌟",
    "You successfully done this christmas-mashup",
    "🎄 MERRY CHRISTMAS ☃"
]

# ===== CLEAR =====
def cls():
    print("\033[2J\033[H", end="")

# ===== STAR =====
def draw_star():
    print(f"\033[2;{TREE_X + TREE_WIDTH//2}H\033[93m★\033[0m")

# ===== TREE =====
def draw_tree(frame):
    row = 3

    for i in range(1, TREE_HEIGHT + 1):
        dots = i * 2 - 1
        pad = TREE_WIDTH // 2 - dots // 2

        print(f"\033[{row};{TREE_X}H" + " " * pad, end="")

        for j in range(dots):
            col = colors[(j + frame) % len(colors)]   # плавне мерехтіння
            print(f"\033[{col}m●\033[0m", end="")

        row += 1

    # TRUNK
    print(f"\033[{row};{TREE_X}H" + " " * (TREE_WIDTH//2 - 1) + "\033[45m   \033[0m")

# ===== PRESENTS =====
def draw_presents(base_row):
    presents = [
        ("\033[41m   \033[0m", 4),
        ("\033[46m   \033[0m", 10),
        ("\033[43m   \033[0m", 17)
    ]
    for box, offset in presents:
        print(f"\033[{base_row};{TREE_X + offset}H{box}")

# ===== SNOW =====
snow = [" " * COLS for _ in range(ROWS)]

def update_snow():
    global snow
    snow = [("".join("*" if random.randint(0, 25) == 0 else " " for _ in range(COLS)))] + snow[:-1]

    for i, line in enumerate(snow):
        print(f"\033[{i+1};1H\033[97m{line}\033[0m", end="")

# ===== TEXT BLOCK =====
def draw_texts(step):
    for i in range(step):
        if i < len(texts):
            print(f"\033[{5 + i*2};{TEXT_X}H\033[92m{texts[i]}\033[0m")

# ===== MAIN LOOP =====
cls()

frame = 0
step = 1

while True:
    update_snow()

    draw_star()
    draw_tree(frame)
    draw_presents(3 + TREE_HEIGHT + 2)

    draw_texts(step)

    print(f"\0" * 16)
    frame += 1
    if step < len(texts):
        step += 1

    time.sleep(DELAY)
