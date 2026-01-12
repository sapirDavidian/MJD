import turtle
import random
import pickle
import os

SAVE_FILE = "tictactoe_save.bin"
HISTORY_FILE = "tictactoe_history.csv"

CELL_SIZE = 100
ORIGIN_X = -150
ORIGIN_Y = 150

# -------------------------
# Game logic
# -------------------------
def create_board():
    return [[" " for _ in range(3)] for _ in range(3)]

def is_valid_move(board, r, c):
    return 1 <= r <= 3 and 1 <= c <= 3 and board[r-1][c-1] == " "

def apply_move(board, r, c, symbol):
    board[r-1][c-1] = symbol

def check_winner(board):
    lines = []

    for r in range(3):
        lines.append([(r, 0), (r, 1), (r, 2)])
    for c in range(3):
        lines.append([(0, c), (1, c), (2, c)])
    lines.append([(0, 0), (1, 1), (2, 2)])
    lines.append([(0, 2), (1, 1), (2, 0)])

    for cells in lines:
        vals = [board[r][c] for r, c in cells]
        if vals[0] != " " and vals.count(vals[0]) == 3:
            return vals[0], cells

    return None, None

def is_draw(board):
    return all(board[r][c] != " " for r in range(3) for c in range(3))

def empty_cells(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]

def random_ai_move(board):
    return random.choice(empty_cells(board))

def find_winning_move(board, symbol):
    for r, c in empty_cells(board):
        board[r][c] = symbol
        winner, _ = check_winner(board)
        board[r][c] = " "
        if winner == symbol:
            return r, c
    return None

def strategic_ai_move(board, ai, human):
    for sym in [ai, human]:
        move = find_winning_move(board, sym)
        if move:
            return move
    if board[1][1] == " ":
        return 1, 1
    for r, c in [(0,0),(0,2),(2,0),(2,2)]:
        if board[r][c] == " ":
            return r, c
    for r, c in [(0,1),(1,0),(1,2),(2,1)]:
        if board[r][c] == " ":
            return r, c
    return random_ai_move(board)

# -------------------------
# Save / History
# -------------------------
def save_game(board, current, p1, p2, mode):
    with open(SAVE_FILE, "wb") as f:
        pickle.dump({
            "board": board,
            "current": current,
            "p1": p1,
            "p2": p2,
            "mode": mode
        }, f)

def load_game():
    if not os.path.exists(SAVE_FILE):
        return None
    try:
        with open(SAVE_FILE, "rb") as f:
            return pickle.load(f)
    except:
        return None

def append_history(p1, p2, winner):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{p1},{p2},{winner}\n")

def print_history():
    if not os.path.exists(HISTORY_FILE):
        print("No history.")
        return
    print("---- History ----")
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        print(f.read())

# -------------------------
# Turtle drawing
# -------------------------

def draw_title(title_pen):
    title_pen.clear()
    title_pen.up()
    title_pen.goto(0, 260)
    title_pen.write(
        "TIC TAC TOE",
        align="center",
        font=("Arial", 24, "bold")
    )

def setup_screen():
    s = turtle.Screen()
    s.setup(600, 600)
    s.title("Tic Tac Toe")
    return s

def make_pen():
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.pensize(3)
    return t

def cell_center(r, c):
    return (
        ORIGIN_X + c * CELL_SIZE + CELL_SIZE / 2,
        ORIGIN_Y - r * CELL_SIZE - CELL_SIZE / 2
    )

def draw_grid(pen):
    pen.up()
    for i in range(1, 3):
        pen.goto(ORIGIN_X + i*CELL_SIZE, ORIGIN_Y)
        pen.down()
        pen.goto(ORIGIN_X + i*CELL_SIZE, ORIGIN_Y - 3*CELL_SIZE)
        pen.up()
    for i in range(1, 3):
        pen.goto(ORIGIN_X, ORIGIN_Y - i*CELL_SIZE)
        pen.down()
        pen.goto(ORIGIN_X + 3*CELL_SIZE, ORIGIN_Y - i*CELL_SIZE)
        pen.up()

def draw_x(pen, r, c):
    pen.color("red")
    cx, cy = cell_center(r, c)
    pen.up(); pen.goto(cx-30, cy+30); pen.down()
    pen.goto(cx+30, cy-30)
    pen.up(); pen.goto(cx-30, cy-30); pen.down()
    pen.goto(cx+30, cy+30); pen.up()

def draw_o(pen, r, c):
    pen.color("blue")
    cx, cy = cell_center(r, c)
    pen.up(); pen.goto(cx, cy-35); pen.down()
    pen.circle(35); pen.up()

def highlight_win(pen, cells):
    pen.color("green")
    pen.pensize(5)
    x1,y1 = cell_center(*cells[0])
    x2,y2 = cell_center(*cells[-1])
    pen.up(); pen.goto(x1,y1); pen.down(); pen.goto(x2,y2)
    pen.up(); pen.pensize(3); pen.color("black")

def show_message(msg_pen, text):
    msg_pen.clear()
    msg_pen.up()
    msg_pen.goto(0, -220)
    msg_pen.write(text, align="center", font=("Arial", 16, "bold"))

# -------------------------
# Input helpers
# -------------------------
def ask_int(screen, prompt):
    """ Ask the user for a number between 1 and 3.
    If the input is invalid (not a number or not in range),
    the function returns the string "INVALID" """

    s = screen.textinput("Input", prompt)

    if s is None:
        return None

    s = s.strip()

    # Check if input is a number
    if not s.isdigit():
        return "INVALID"

    value = int(s)

    # Check if number is in the valid range 1-3
    if value < 1 or value > 3:
        return "INVALID"

    return value


# -------------------------
# Main
# -------------------------
def main():
    screen = setup_screen()
    pen = make_pen()  # ציור הלוח
    msg_pen = make_pen()  # הודעות
    title_pen = make_pen()  # כותרת

    draw_grid(pen)
    draw_title(title_pen)

    # Start menu
    while True:
        choice = screen.textinput(
            "Start",
            "Type NEW to start a new game, or LOAD to load a game:"
        )
        if choice is None:
            turtle.bye()
            return

        choice = choice.strip().upper()

        if choice in ["NEW", "LOAD"]:
            break
        show_message(msg_pen, "Invalid choice")

    if choice == "LOAD":
        data = load_game()
        if data:
            board = data["board"]
            current = data["current"]
            p1 = data["p1"]
            p2 = data["p2"]
            mode = data["mode"]
            for r in range(3):
                for c in range(3):
                    if board[r][c] == "X":
                        draw_x(pen, r, c)
                    elif board[r][c] == "O":
                        draw_o(pen, r, c)
        else:
            show_message(msg_pen, "No save found")
            board = create_board()
            current = "X"
            p1 = "Player1"
            p2 = "Player2"
            mode = "PVP"
    else:
        board = create_board()
        current = "X"
        p1 = screen.textinput("Player 1", "Name (X):") or "Player1"

        while True:
            mode = screen.textinput("Mode", "PVP / RANDOM / SMART")
            if mode is None:
                turtle.bye()
                return
            mode = mode.strip().upper()
            if mode in ["PVP", "RANDOM", "SMART"]:
                break
            show_message(msg_pen, "Invalid mode")

        p2 = screen.textinput("Player 2", "Name (O):") if mode == "PVP" else "Computer"

    while True:
        show_message(msg_pen, f"{current}'s turn")

        if current == "O" and mode != "PVP":
            r, c = strategic_ai_move(board, "O", "X") if mode == "SMART" else random_ai_move(board)
            r += 1; c += 1
        else:
            r = ask_int(screen, "Row (1-3):")
            if r is None: break
            if r == "INVALID":
                show_message(msg_pen, "Invalid input"); continue

            c = ask_int(screen, "Column (1-3):")
            if c is None: break
            if c == "INVALID":
                show_message(msg_pen, "Invalid input"); continue

        if not is_valid_move(board, r, c):
            show_message(msg_pen, "Cell occupied")
            continue

        apply_move(board, r, c, current)
        draw_x(pen, r-1, c-1) if current == "X" else draw_o(pen, r-1, c-1)

        winner, cells = check_winner(board)
        if winner:
            highlight_win(pen, cells)
            show_message(msg_pen, f"{winner} wins!")
            append_history(p1, p2, p1 if winner=="X" else p2)
            break

        if is_draw(board):
            show_message(msg_pen, "Draw!")
            append_history(p1, p2, "Draw")
            break

        current = "O" if current == "X" else "X"

    screen.textinput("End", "Game over")
    turtle.bye()

if __name__ == "__main__":
    main()

