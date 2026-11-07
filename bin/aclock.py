#!/usr/bin/env python3.12

import tkinter as tk
import math
from datetime import datetime

# --------------------------------
# 基本設定
# --------------------------------

WIDTH  = 384
HEIGHT = 384

BG_COLOR   = "#f6f6f6"
FACE_COLOR = "#ffffff"
LINE_COLOR = "#222222"
TEXT_COLOR = "#222222"

root = tk.Tk()
root.title("アナログ時計")

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg=BG_COLOR,
    highlightthickness=0
)
canvas.pack(fill=tk.BOTH, expand=True)


# --------------------------------
# 文字盤
# --------------------------------

def draw_face(cx, cy, radius):

    canvas.create_oval(
        cx - radius,
        cy - radius,
        cx + radius,
        cy + radius,
        fill=FACE_COLOR,
        outline="#dddddd",
        width=3
    )


# --------------------------------
# 目盛り
# --------------------------------

def draw_marks(cx, cy, radius):

    # 色の設定
    hour_color = "#222222"
    minute_color = "#bbbbbb"

    # 太さの設定
    hour_width = max(1, radius * 0.015)
    minute_width = 1

    # 60個の目盛り
    for i in range(60):

        angle = math.radians(i * 6)

        # 12・3・6・9時：小さな円
        if i % 15 == 0:

            r = radius * 0.945

            x = cx + r * math.sin(angle)
            y = cy - r * math.cos(angle)

            dot_radius = radius * 0.012

            canvas.create_oval(
                x - dot_radius,
                y - dot_radius,
                x + dot_radius,
                y + dot_radius,
                fill=hour_color,
                outline=hour_color
            )

        # その他の時の目盛り
        elif i % 5 == 0:

            r1 = radius * 0.84
            r2 = radius * 0.96

            color = hour_color
            line_width = hour_width

        # 分・秒の目盛り
        else:

            r1 = radius * 0.92
            r2 = radius * 0.96

            color = minute_color
            line_width = minute_width

        # 線の描画
        if i % 5 != 0 or i % 15 != 0:

            if i % 5 == 0:
                r1 = radius * 0.84
                r2 = radius * 0.96

            x1 = cx + r1 * math.sin(angle)
            y1 = cy - r1 * math.cos(angle)

            x2 = cx + r2 * math.sin(angle)
            y2 = cy - r2 * math.cos(angle)

            canvas.create_line(
                x1, y1,
                x2, y2,
                fill=color,
                width=line_width,
                capstyle=tk.ROUND
            )


# --------------------------------
# 数字
# --------------------------------

def draw_numbers(cx, cy, radius):

    numbers = [12, 3, 6, 9]

    for number in numbers:

        angle = math.radians(number * 30)

        r = radius * 0.81

        x = cx + r * math.sin(angle)
        y = cy - r * math.cos(angle)

        font_size = max(1, int(radius * 0.12))

        canvas.create_text(
            x, y,
            text=str(number),
            fill=TEXT_COLOR,
            font=("IPAPGothic", font_size, "normal")
        )


# --------------------------------
# 針
# --------------------------------

def draw_hands(cx, cy, radius):

    now = datetime.now()

    hour   = now.hour % 12
    minute = now.minute
    second = now.second

    # --------------------------------
    # 角度計算
    # --------------------------------

    hour_angle = math.radians(
        (hour + minute / 60 + second / 3600) * 30
    )

    minute_angle = math.radians(
        (minute + second / 60) * 6
    )

    second_angle = math.radians(second * 6)

    # --------------------------------
    # 針の設定
    # --------------------------------

    hour_length = radius * 0.54
    minute_length = radius * 0.89
    second_length = radius * 0.94

    # 秒針の反対側
    second_tail = radius * 0.30

    hour_width = max(1, radius * 0.035)
    minute_width = max(1, radius * 0.022)
    second_width = max(1, radius * 0.008)

    # --------------------------------
    # 中心の軸
    # --------------------------------

    hub_radius = radius * 0.025

    canvas.create_oval(
        cx - hub_radius,
        cy - hub_radius,
        cx + hub_radius,
        cy + hub_radius,
        fill="#222222",
        outline="#222222"
    )

    # --------------------------------
    # 時針
    # --------------------------------

    x = cx + hour_length * math.sin(hour_angle)
    y = cy - hour_length * math.cos(hour_angle)

    canvas.create_line(
        cx, cy, x, y,
        fill="#222222",
        width=hour_width,
        capstyle=tk.ROUND
    )

    # --------------------------------
    # 分針
    # --------------------------------

    x = cx + minute_length * math.sin(minute_angle)
    y = cy - minute_length * math.cos(minute_angle)

    canvas.create_line(
        cx, cy, x, y,
        fill="#222222",
        width=minute_width,
        capstyle=tk.ROUND
    )

    # --------------------------------
    # 秒針（両方向）
    # --------------------------------

    x1 = cx - second_tail * math.sin(second_angle)
    y1 = cy + second_tail * math.cos(second_angle)

    x2 = cx + second_length * math.sin(second_angle)
    y2 = cy - second_length * math.cos(second_angle)

    canvas.create_line(
        x1, y1, x2, y2,
        fill="#d32f2f",
        width=second_width,
        capstyle=tk.ROUND
    )


# --------------------------------
# 全体描画
# --------------------------------

def draw_clock(event=None):

    canvas.delete("all")

    # ウィンドウサイズから中心と半径を計算
    width  = canvas.winfo_width()
    height = canvas.winfo_height()

    cx = width / 2
    cy = height / 2

    radius = min(width, height) * 0.45

    draw_face(cx, cy, radius)
    draw_marks(cx, cy, radius)
    draw_numbers(cx, cy, radius)
    draw_hands(cx, cy, radius)


# --------------------------------
# 時計の更新
# --------------------------------

def update_clock():

    now = datetime.now()

    draw_clock()

    # 次の0.1秒境界までの時間を計算
    delay = 100 - (now.microsecond // 1000 % 100)

    root.after(delay, update_clock)


# --------------------------------
# 終了処理
# --------------------------------

def close_app(event=None):

    root.destroy()


root.bind_all("<Escape>", close_app)
root.bind_all("q", close_app)


# --------------------------------
# 起動
# --------------------------------

canvas.bind("<Configure>", draw_clock)

root.after(0, update_clock)

root.mainloop()

