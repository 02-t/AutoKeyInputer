import time, json, ait, pyautogui
from run_keyboard_inputs import *

pyautogui.FAILSAFE = False

count__ = 0


def click(key, type_):
    if type_ == "click":
        key = key[0].upper()
        ait.click(key)
    elif type_ == "hold":
        pyautogui.mouseDown(button=key)
    elif type_ == "release":
        pyautogui.mouseUp(button=key)


def press(key, type_):
    if type_ == "click":
        hold_key(key)
        release_key(key)
    elif type_ == "hold":
        hold_key(key)
    elif type_ == "release":
        release_key(key)


def input_key(type_, full_key, temp_count):
    global count__
    if temp_count != count__:
        return
    keys = full_key.split("+")

    for key in keys:
        if key == "left_click" or key == "right_click" or key == "middle_button":
            click(key.split("_")[0], type_)
            continue
        elif get_code(key) != -1:
            press(key, type_)
        else:
            ait.write(key)


def start(info, repeat_type, repeat_count, stop):
    global count__
    temp_count = count__
    if repeat_type == 1:
        repeat_count = pow(pow(10, 10), 2)
    elif repeat_type == 0:
        repeat_count = 1

    for i in range(int(repeat_count)):
        for line in info:
            if temp_count != count__:
                return
            line = json.loads(line)
            time_ = line["time"] / 1000
            x = line["x"]
            y = line["y"]
            move = line["move"]
            type_ = line["type"]
            full_key = line["key"]

            if move == "teleport":
                time.sleep(time_)
                if temp_count != count__:
                    return
                ait.move(x, y)
                input_key(type_, full_key, temp_count)
            elif move == "move":
                pyautogui.moveTo(x, y, duration=time_)
                input_key(type_, full_key, temp_count)
            elif move == "none":
                time.sleep(time_)
                input_key(type_, full_key, temp_count)
            else:
                time.sleep(time_)

    if temp_count != count__:
        return

    stop()
