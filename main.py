import tkinter as tk
from tkinter import messagebox
import random

#coding part

WINNING_COMBINATION = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # lines
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
    [0, 4, 8], [2, 4, 6]              # diagonales
]

def check_winner(board, player):
    """returns True if a player won"""
    for combo in WINNING_COMBINATION:
        if all(board[i] == player for i in combo):
            return True
    return False
    
def evaluation(board):
    # evaluation function: -1000 if the player won, +1000 if thee AI won
    if check_winner(board, 1):
        return 1000
    if check_winner(board, -1):
        return -1000
    return 0

def is_full(board):
    #retunrs True if the board is full (tie)
    empty_squares = []
    for i in range(len(board)):
        if board[i] == 0:
            empty_squares.append(i)
    return len(empty_squares) == 0

def squares_available(board):
    #returns a list of the empty squares' index
    empty_squares = []
    for i in range(len(board)):
        if board[i] == 0:
            empty_squares.append(i)
    return empty_squares

def minimax(board, level, is_max, level_max=None):
    """
    Algorithm Minimax recursive.

    parameters :
      - board: actual state of the game (list of 9elements for each square)
      - level: actual level in the tree
      - is_max: True if it's the AI's turn (node max),else: false (node min)
      - level_max: maximal leveml that we are looking for (None = unlimited)

    returns:
      - the score of the best combination found
    """
    # Basic square: end of the game or maximal level reached
    score = evaluation(board)
    if score != 0:  # someone won
        return score
    if is_full(board):  # tie
        return 0
    if level_max is not None and level >= level_max:
        return 0  # we stop looking

    available = squares_available(board)

    if is_max:
        # Node MAX : The AI looks for the highest score
        best_score = float('-inf')
        for square in available:
            board[square] = 1  # l'IA joue
            score = minimax(board, level + 1, False, level_max)
            board[square] = 0  # on annule le coup
            best_score = max(best_score, score)
        return best_score

    else:
        # Node MIN : The other player looks for the lowest score
        best_score = float('inf')
        for square in available:
            board[square] = -1  # the human player plays
            score = minimax(board, level + 1, True, level_max)
            board[square] = 0   # we cancel the play
            best_score = min(best_score, score)
        return best_score


def best_play(board, level_max=None):
    """
    find the best combination of plays using the minimax function

    returns :
      - the index of the square the AI must play 
      - the score associated to this play
    """
    best_score = float('-inf')
    best_index = -1

    for square in squares_available(board):
        board[square] = 1  # The AI plays
        score = minimax(board, 1, False, level_max)
        board[square] = 0  # We cancel

        print(f"  square {square} → score = {score}")

        if score > best_score:
            best_score = score
            best_index = square

    return best_index, best_score

#creating the window
root = tk.Tk()
root.title("TicTacToe")
root.minsize(500, 600)
root.configure(bg="#1a1a2e")

#creating the status
status_label = tk.Label(root, text="Current Player: X", font=("Arial", 15), bg = "#1a1a2e", fg = "white")
status_label.grid(row=3, column=0, columnspan=3, pady = (10, 5))

#game mode selection
game_mode_var = tk.StringVar(value="HUMAN")
difficulty_var = tk.StringVar(value="EASY")

# base variables
buttons = []
current_player = "X"
win = False

#internal board for minimax
internal_board = [0] * 9

#finishes the game as there has been a winning combisnation 
def print_winner():
    global win
    if win is False:
        win = True
        print("Player", current_player, "has won! Congratulations!")
        show_popup_winner()

def show_popup_winner():
    status_label.config(text=f"Player {current_player} wins!")
    messagebox.showinfo("Game Over", f"Player {current_player} wins!")

def show_popup_tie():
    status_label.config(text="It's a tie!")
    messagebox.showinfo("Game Over", "It's a tie!")

def check_win_and_tie():
    if check_winner(internal_board, -1): #human X won
        print_winner()
        return True
    if check_winner(internal_board, 1): #AI 0 won
        print_winner()
        return True
    if is_full(internal_board):
        show_popup_tie()
        return True
    return False

#switching players once each one has played once 
def switch_player():
    global current_player
    if current_player == "X":
        current_player = 0
    else:
        current_player = "X"
    if not win:
        status_label.config(text=f"Current Player: {current_player}")


"""#finding winning combinations
def check_win(clicked_row, clicked_col):

    # horizontal (rows)
    count = 0
    for i in range(3):
        current_button = buttons[i][clicked_row]
        if current_button['text'] == current_player:
            count += 1
    if count == 3:
        print_winner()

    # vertical (columns)
    count = 0
    for i in range(3):
        current_button = buttons[clicked_col][i]
        if current_button['text'] == current_player:
            count += 1
    if count == 3:
        print_winner()

    # diagonal
    count = 0
    for i in range(3):
        current_button = buttons[i][i]
        if current_button['text'] == current_player:
            count += 1
    if count == 3:
        print_winner()

     # inverse diagonal (wouldnt find some victories without)
    count = 0
    for i in range(3):
        current_button = buttons[2-i][i]
        if current_button['text'] == current_player:
            count += 1
    if count == 3:
        print_winner()"""

  
    #if no one wins, meaning the grid is full and there are no winning combination 
"""if win is False:
        count = 0
        for col in range(3):
            for row in range(3):
                current_button = buttons[col][row]
                if current_button['text'] == 'X' or current_button['text'] == '0':
                    count += 1
        if count == 9:
            print("It's a tie!")"""




#putting the corresponding symbol when a player clicks somewhere on the grid if the space is empty, then after each play we check if there is a win and if not we change player 
def place_symbol(row, column):
    global win
    if win:
        return

    clicked_button = buttons[column][row]
    
    if clicked_button['text'] == "":
        clicked_button.config(text=current_player, fg="#e94560" if current_player == 'X' else "#0f3460")

        #update internal board
        square_index = column * 3 + row   # col-major storage used in draw_grid
        if current_player == 'X':
            internal_board[square_index] = -1
        else:
            internal_board[square_index] = 1

        #check game over
        if check_win_and_tie():
            return

        #switch player
        switch_player()

        #trigger AI move if needed
        if game_mode_var.get() == "AI" and current_player == 'O' and not win:
            root.after(300, lambda: ai_move(difficulty_var.get()))




"""#the restart button 
def restart_game():
    global win, current_player
    win = False
    current_player = "X"
    status_label.config(text="Current Player: X")

    for col in range(3):
        for row in range(3):
            buttons[col][row].config(text="")"""


def ai_move(difficulty):
    global win
    if win:
        return
    available = squares_available(internal_board)
    if not available:
        return
    if difficulty == "EASY" :
        #random move
        chosen_index = random.choice(available)
    elif difficulty == "MEDIUM":
        #minimax w/ depth of 3
        chosen_index = best_play(internal_board, level_max=3)
    else:
        #full miniax (hard)
        chosen_index = best_play(internal_board)

    #convert flat index back to row, col
    col = chosen_index // 3
    row = chosen_index % 3

    buttons[col][row].config(text="0", gr="#0f3460")
    internal_board[chosen_index] = 1

    if check_win_and_tie():
        return
    
    switch_player()

#GRID DRAWING

# drawing the grid inside a function to have a more efficient code (it endend up working) 
def draw_grid():
    for col in range(3):
        buttons_in_cols = []
        for row in range(3):
            button = tk.Button(
                root, font=("Arial", 50),
                width=3, height=1, bg="#16213e", activebackground="#0f3460", relief="flat",
                command=lambda r=row, c=col: place_symbol(r, c)
            )
            button.grid(row=row, column=col, padx=4, pady=4)
            buttons_in_cols.append(button)
        buttons.append(buttons_in_cols)

#RESTART

def restart_game():
    global win, current_player
    win = False
    current_player = "X"
    status_label.config(text="Current Player: X")

    for i in range (9):
        internal_board[i] = 0

    for col in range(3):
        for row in range(3):
            buttons[col][row].config(text="", bg="#16213e")


restart_button = tk.Button(
    root,
    text="Restart",
    font=("Arial", 13),
    bg="#e94560",
    fg="white",
    activebackground="#c73652",
    relief="flat",
    padx=10,
    command=restart_game
)
restart_button.grid(row=4, column=0, columnspan=3, pady=8)

# Game mode radio buttons
mode_frame = tk.Frame(root, bg="#1a1a2e")
mode_frame.grid(row=5, column=0, columnspan=3, pady=4)

tk.Label(mode_frame, text="Mode:", font=("Arial", 11), bg="#1a1a2e", fg="white").pack(side="left", padx=6)
tk.Radiobutton(
    mode_frame, text="Human vs Human",
    variable=game_mode_var, value="HUMAN",
    font=("Arial", 11), bg="#1a1a2e", fg="white",
    selectcolor="#0f3460", activebackground="#1a1a2e"
).pack(side="left", padx=6)
tk.Radiobutton(
    mode_frame, text="Human vs AI",
    variable=game_mode_var, value="AI",
    font=("Arial", 11), bg="#1a1a2e", fg="white",
    selectcolor="#0f3460", activebackground="#1a1a2e"
).pack(side="left", padx=6)

# Difficulty dropdown
diff_frame = tk.Frame(root, bg="#1a1a2e")
diff_frame.grid(row=6, column=0, columnspan=3, pady=4)

tk.Label(diff_frame, text="Difficulty:", font=("Arial", 11), bg="#1a1a2e", fg="white").pack(side="left", padx=6)
difficulty_menu = tk.OptionMenu(diff_frame, difficulty_var, "EASY", "MEDIUM", "HARD")
difficulty_menu.config(font=("Arial", 11), bg="#0f3460", fg="white", activebackground="#e94560", relief="flat")
difficulty_menu.pack(side="left")

draw_grid()
root.mainloop()





