import os
import curses
from curses import wrapper

cursor = {
    "row": 0,
    "col": 0
}

f = open("hello.txt")
filename = "hello.txt"
lines = f.read().splitlines()
lines_s = [list(line) for line in lines]

# move left cursor
def ml(cursor, lines_s):
    if cursor["col"] > 0:
        cursor["col"] -= 1
    elif cursor["row"] > 0:
        cursor["row"] -= 1
        cursor["col"] = len(lines_s[cursor["row"]])

# move right cursor
def mr(cursor, lines_s):
    if cursor["col"] < len(lines_s[cursor["row"]]):
        cursor["col"] += 1
    elif cursor["row"] < len(lines_s) - 1:
        cursor["row"] += 1
        cursor["col"] = 0

# move up cursor
def mu(cursor, lines_s):
    if cursor["row"] > 0:
        cursor["row"] -= 1
        cursor["col"] = min(cursor["col"], len(lines_s[cursor["row"]]))

# move down cursor

def md(cursor, lines_s):
    if cursor["row"] < len(lines_s) - 1:
        cursor["row"] += 1
        cursor["col"] = min(cursor["col"], len(lines_s[cursor["row"]]))   

def save_file(filename, lines_s):
    with open(filename, "w") as f:
        for line in lines_s:
            f.write(''.join(line) + '\n')


def main(stdscr):
    # initialize curses
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    # your existing buffer and cursor
    mode = "NORMAL"
    lines_s = [list(line) for line in open("hello.txt").read().splitlines()]
    cursor = {"row": 0, "col": 0}

    while True:
        stdscr.clear()
        
        # draw your buffer
        for i, line in enumerate(lines_s):
            line_str = ''.join(line)

            if i == cursor["row"]:
            # Insert ^ at the cursor column
                display_line = line_str[:cursor["col"]] + "|" + line_str[cursor["col"]:]
            else:
                display_line = line_str

            stdscr.addstr(i, 0, f"{i + 1} | {display_line}")

        # move the terminal cursor
        stdscr.move(cursor["row"], cursor["col"])
        stdscr.refresh()
        
        key = stdscr.getch()
        
        if mode == "NORMAL":
            if key == curses.KEY_LEFT:
                ml(cursor, lines_s)
            elif key == curses.KEY_RIGHT:
                mr(cursor, lines_s)
            elif key == curses.KEY_UP:
                mu(cursor, lines_s)
            elif key == curses.KEY_DOWN:
                md(cursor, lines_s)
            elif key == ord("i"):
                mode = "INSERT"
            elif key == ord("q"):
                break
            elif key == 23:
                save_file(filename, lines_s)
        
        elif mode == "INSERT":
            if key == 27:  # ESC key
                mode = "NORMAL"

            if key == curses.KEY_LEFT:
                ml(cursor, lines_s)
            elif key == curses.KEY_RIGHT:
                mr(cursor, lines_s)
            elif key == curses.KEY_UP:
                mu(cursor, lines_s)
            elif key == curses.KEY_DOWN:
                md(cursor, lines_s)

            elif 32 <= key <= 126:
                lines_s[cursor["row"]].insert(cursor["col"], chr(key))
                cursor["col"] += 1

            elif key in (curses.KEY_BACKSPACE, 127):
                if key in (curses.KEY_BACKSPACE, 127):
                    if cursor["col"] > 0:
                        # remove character before cursor
                        lines_s[cursor["row"]].pop(cursor["col"] - 1)
                        cursor["col"] -= 1
                    elif cursor["row"] > 0:
                        # merge with previous line
                        prev_len = len(lines_s[cursor["row"] - 1])
                        lines_s[cursor["row"] - 1].extend(lines_s[cursor["row"]])
                        lines_s.pop(cursor["row"])
                        cursor["row"] -= 1
                        cursor["col"] = prev_len
                ...
            elif key in (10, 13):
                line = lines_s[cursor["row"]]
                new_line = line[cursor["col"]:]  # split after cursor
                lines_s[cursor["row"]] = line[:cursor["col"]]
                lines_s.insert(cursor["row"] + 1, new_line)
                cursor["row"] += 1
                cursor["col"] = 0

                ...

            elif key == 23:
                save_file(filename, lines_s)



curses.wrapper(main)