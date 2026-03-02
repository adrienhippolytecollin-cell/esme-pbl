import tkinter as tk
from tkinter import messagebox

#creating the window
root = tk.Tk()

#creating the status
status_label = tk.Label(root, text="Current Player: X", font=("Arial", 15))
status_label.grid(row=3, column=0, columnspan=3)

#game mode selection
game_mode_var = tk.StringVar(value="HUMAN")
difficulty_var = tk.StringVar(value="EASY")

# stocking base variables 
buttons = []
current_player = 'X'
win = False

#finishes the game as there has been a winning combisnation 
def print_winner():
    global win
    if win is False:
        win = True
        print("Player", current_player, "has won! Congratulations!")
        show_popup_winner()

def show_popup_winner():
    messagebox.showinfo("Game Over", f"Player {current_player} wins!")


#finding winning combinations
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
        print_winner()

  
    #if no one wins, meaning the grid is full and there are no winning combination 
    if win is False:
        count = 0
        for col in range(3):
            for row in range(3):
                current_button = buttons[col][row]
                if current_button['text'] == 'X' or current_button['text'] == '0':
                    count += 1
        if count == 9:
            print("It's a tie!")

#switching players once each one has played once 
def switch_player():
    global current_player
    if current_player == 'X':
        current_player = '0'
    else:
        current_player = 'X'

#putting the corresponding symbol when a player clicks somewhere on the grid if the space is empty, then after each play we check if there is a win and if not we change player 
def place_symbol(row, column):

    global win
    if win:
        return

    clicked_button = buttons[column][row]
    if clicked_button['text'] == "":
        clicked_button.config(text=current_player)

        check_win(row, column)
        switch_player()
        if game_mode_var.get() == "AI" and current_player == "0" and not win:
            ai_move(difficulty_var.get())


# drawing the grid inside a function to have a more efficient code (it endend up working) 
def draw_grid():
    for col in range(3):
        buttons_in_cols = []
        for row in range(3):
            button = tk.Button(
                root, font=("Arial", 50),
                width=5, height=3,
                command=lambda r=row, c=col: place_symbol(r, c)
            )
            button.grid(row=row, column=col)
            buttons_in_cols.append(button)
        buttons.append(buttons_in_cols)

#the restart button 
def restart_game():
    global win, current_player
    win = False
    current_player = "X"
    status_label.config(text="Current Player: X")

    for col in range(3):
        for row in range(3):
            buttons[col][row].config(text="")

#empty
def ai_move(difficulty):
    print("AI plays in", difficulty, "mode")

# parameters of the window
root.title("New game of TicTacToe")
root.minsize(500, 500)
restart_button = tk.Button(root, text="Restart", font=("Arial", 15), command=restart_game)
restart_button.grid(row=4, column=0, columnspan=3)

tk.Radiobutton(root, text="Human vs Human", variable=game_mode_var, value="HUMAN").grid(row=5, column=0)
tk.Radiobutton(root, text="Human vs AI", variable=game_mode_var, value="AI").grid(row=5, column=2)

difficulty_menu = tk.OptionMenu(root, difficulty_var, "EASY", "MEDIUM", "HARD")
difficulty_menu.grid(row=6, column=0, columnspan=3)

draw_grid()
root.mainloop()


def evaluation(board):
    # evaluation function: -1000 if the player won, +1000 if thee AI won
    if check_winner(board, 1):
        return 1000
    is check_winner(board, -1):
        return -1000
    return 0

def square_available(board):
    #returns a list of the empty squares
    list = []
    for square in enumerate(board):
        if square == 0:
            list.append(square)
    return list

def minimax(board, level, is_max, level_max=None):
    """
    parameters: 
    - board: actual state of the game (list of 9 elements for each square)
    - level: actual level in the tree
    - is_max: true if its the AI's turn (node max), else: false (nose min)
    - level_max: maximal level that we are looking for (None = unlimited)

    returns: the score of the best combijation found
    """
    #basic case: end of the game or maximal level reached
    score = evaluation(board)
    if score != 0: # someone won
        return score 
    if is_full(board): # tie
        return 0
    if level_max is not None and level >= level_max:
        return 0 #we stop looking

    available = squares_available(board)

    if is_max: 
        # Node max : the AI looks for the highest score
        best_score = float ('-inf')
        for case in available: 
            board[square] = 1 # the AI plays
            score = minimax(board, level + 1, False, level_max)
            board[square] = max(bes_score, score)
        return best_score

    else:
        # node min : the other player looks for the lowest score
        for square in available:
            board[square] = -1 # the human player plays
            score = minimax(board, level + 1, True, level_max)
            board[case] = 0 # we cancel the play
            best_score = min(best_score, score)
        return best_score

def best_play(board, level_max=None):
    """
    finds the best combination of plays using the minimac function
    returns: 
    - the index of the square the AI must play
    - the score associated to this play
    """
    best_score = float('-inf')
    best_index = -1
    for square in square_available(board):
        board[square] = 1 #the AI plays
        score = minimax(board, 1, False, level_max)
        board[square] = 0

        print(f" Square {square} -> score = {score}")
        if score > best_score:
            best_score = score
            best_index = square

    return best_index, best_score

