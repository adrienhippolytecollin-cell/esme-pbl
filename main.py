import tkinter as tk
from tkinter import messagebox
import random

# using the MINIMAX method

WINNING_COMBINATION = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8], # lines
    [0, 3, 6], [1, 4, 7], [2, 5, 8], # columns
    [0, 4, 8], [2, 4, 6] # diagonals
]

def check_winner(board, player):
    """returns True if a player won"""
    for combo in WINNING_COMBINATION:
        if all(board[i] == player for i in combo):
            return True
    return False

def evaluation(board, player):
    """evaluation function: +1000 if the AI won, -1000 if the player won"""
    if check_winner(board, player):
        return 1000
    if check_winner(board, -player):
        return -1000
    return 0

def is_full(board):
    """returns True if the board is full (tie)"""
    empty_squares = []
    for i in range(len(board)):
        if board[i] == 0:
            empty_squares.append(i)
    return len(empty_squares) == 0

def squares_available(board):
    """returns a list of the empty squares' index"""
    empty_squares = []
    for i in range(len(board)):
        if board[i] == 0:
            empty_squares.append(i)
    return empty_squares

def minimax(board, level, is_max, player=1, level_max=None, path=None, all_paths=None):
    """
    Recursive Minimax algorithm.
    - path: the current path of (square, who) steps taken so far
    - all_paths: list that collects every fully explored path (for display)
    """
    if path is None:
        path = []
    if all_paths is None:
        all_paths = []

    score = evaluation(board)
    if score != 0: #someone won 
        all_paths.append((list(path), score))
        return score, all_paths
    if is_full(board): #tie
        all_paths.append((list(path), 0))
        return 0, all_paths
    if level_max is not None and level >= level_max:   #depth limit reached
        all_paths.append((list(path), 0))
        return 0, all_paths

    available = squares_available(board)

    if is_max:
        #node MAX: the AI looks for the highest score
        best_score = float('-inf')
        for square in available:
            board[square] = 1
            score, all_paths = minimax(board, level + 1, False, player, level_max,
                                       path + [(square, "AI")], all_paths)
            board[square] = 0
            best_score = max(best_score, score)
        return best_score, all_paths
    else:
        #node MIN: the other player looks for the lowest score
        best_score = float('inf')
        for square in available:
            board[square] = -1
            score, all_paths = minimax(board, level + 1, True,player, level_max,
                                       path + [(square, "Human")], all_paths)
            board[square] = 0
            best_score = min(best_score, score)
        return best_score, all_paths

def best_play(board, player=1, level_max=None):
    """find the best square for the AI and return all explored paths."""
    best_score = float('-inf')
    best_index = -1
    chosen_paths = []

    for square in squares_available(board):
        board[square] = player
        score, paths = minimax(board, 1, False, player, level_max, [(square, "AI")], [])
        board[square] = 0

        if score > best_score:
            best_score = score
            best_index = square
            chosen_paths = paths #save paths from the best move

    return best_index, best_score, chosen_paths


#1st TKINTER PART

root = tk.Tk()
root.title("TicTacToe")
root.minsize(900, 600)
root.configure(bg="#1a1a2e")

#status label
status_label = tk.Label(
    root,
    text="CURRENT PLAYER: X",
    font=("Arial", 15),
    bg="#1a1a2e",
    fg="white"
)
status_label.grid(row=3, column=0, columnspan=3, pady=(10, 5))

#game mode and difficulty label
game_mode_var = tk.StringVar(value="HUMAN")
difficulty_var = tk.StringVar(value="EASY")

#base variables
buttons = []
current_player = 'X'
win = False
ai_symbol = "X"

#internal numeric board for minimax (0=empty, 1=AI (O), -1=human (X))
internal_board = [0] * 9


#GAME FUNCTIONS

def print_winner():
    global win
    if win is False:
        win = True
        show_popup_winner()

def show_popup_winner():
    status_label.config(text=f"Player {current_player} wins!")
    messagebox.showinfo("Game Over", f"Player {current_player} wins!")

def show_popup_tie():
    status_label.config(text="It's a tie!")
    messagebox.showinfo("Game Over", "It's a tie!")

def check_win_and_tie():
    """Check winning combinations and tie using the internal board."""
    if check_winner(internal_board, 1): #human ('O') won
        print_winner()
        return True
    if check_winner(internal_board, -1): # AI ('X') won
        print_winner()
        return True
    if is_full(internal_board):
        show_popup_tie()
        return True
    return False

def switch_player():
    global current_player
    if current_player == 'X':
        current_player = 'O'
    else:
        current_player = 'X'
    if not win:
        status_label.config(text=f"Current Player: {current_player}")

def place_symbol(row, column):
    global win

    if win:
        return

    player = 1 if ai_symbol == "O" else -1
    opponent_symbol = "X" if ai_symbol == "O" else "O"
    # buttons[row][col]
    clicked_button = buttons[row][column]

    if clicked_button['text'] == "":
        #update button text
        clicked_button.config(
            text=current_player,
            fg="#e94560" if current_player == opponent_symbol else "#0f3460"
        )

        #update internal board: index = row * 3 + col
        square_index = row * 3 + column
        if current_player == opponent_symbol:
            internal_board[square_index] = -player
        else:
            internal_board[square_index] = player

        #check game over
        if check_win_and_tie():
            return

        #switch player
        switch_player()

        #trigger AI move if needed
        if game_mode_var.get() == "AI" and current_player == 'O' and not win:
            root.after(300, lambda: ai_move(difficulty_var.get()))


def display_tree_paths(chosen_index, best_score, paths, difficulty):
    """output the path taken by the AI into the textbox"""
    text_widget.config(state="normal")
    text_widget.delete("1.0", tk.END)

    text_widget.insert(tk.END, f"AI MOVE (difficulty: {difficulty})\n")
    text_widget.insert(tk.END, f"Chosen square : {chosen_index}\n")
    text_widget.insert(tk.END, f"Best score    : {best_score}\n\n")

    #it it's the easy level, the AI's moves are random, therefore there is no tree to output
    if not paths:
        text_widget.insert(tk.END, "(random move, no tree to display)\n")

    #otherwise we show the paths
    else:
        text_widget.insert(tk.END, "Number of paths explored : " + str(len(paths)) + "\n")

        #only show the first 30 paths so that the box doesn't overflow
        number_of_paths_to_show = 30
        shown = paths[:number_of_paths_to_show]

        #go through each path one by one
        for i in range(len(shown)):
            path = shown[i][0] #the list of steps in this path
            final_score = shown[i][1]  #the score at the end of this path

            #build the step by step string for this path
            path_text = ""
        
        for j in range(len(path)):
                square = path[j][0]  #which square was played
                who = path[j][1]  #"A" for AI and "H" for human
                step = "square" + str(square) + "(" + who[0] + ")"
                if j == 0:
                    path_text = step
                else:
                    path_text = path_text + " -> " + step

                #write the path and its score into the text box
                text_widget.insert(tk.END, "[" + str(j + 1) + "] " + path_text + "\n")
                text_widget.insert(tk.END, "      score: " + str(final_score) + "\n")

        #if there were more than 30 paths, say how many were hidden
        if len(paths) > number_of_paths_to_show:
            hidden = len(paths) - number_of_paths_to_show
            text_widget.insert(tk.END, "\n... (" + str(hidden) + " more paths not shown)\n")

    #lock the text box again so that the user can't type in it
    text_widget.config(state="disabled")




def ai_move(difficulty):
    """make the AI play based on difficulty."""
    global win

    if win:
        return

    available = squares_available(internal_board)
    if not available:
        return

    if game_mode_var.get() == 'AIvsAI':
        ai_symbol = current_player
    player = 1 if ai_symbol == "O" else -1

    if difficulty == "EASY":
        chosen_index = random.choice(available)
        display_tree_paths(chosen_index, "N/A", [], difficulty)

    elif difficulty == "MEDIUM":
        chosen_index, best_score, paths = best_play(internal_board, player, level_max=3)
        display_tree_paths(chosen_index, best_score, paths, difficulty)

    else:  #HARD: full minimax, unbeatable
        chosen_index, best_score, paths = best_play(internal_board, player)
        display_tree_paths(chosen_index, best_score, paths, difficulty)

    #convert flat index to (row, col)
    row = chosen_index // 3
    col = chosen_index % 3

    buttons[row][col].config(text=ai_symbol, fg="#0f3460" if ai_symbol == "X" else "#0f3460")
    internal_board[chosen_index] = player

    if check_win_and_tie():
        return

    switch_player()
    
    if game_mode_var.get() == "AIvsAI" and not win:
        root.after(300, lambda: ai_move(difficulty_var.get()))

#GRID

def draw_grid():
    # function that draw the grid (columns and rows)
    for row in range(3):
        buttons_in_row = []
        for col in range(3):
            button = tk.Button(
                root,
                font=("Arial", 50),
                width=2, height=1,
                bg="#16213e",
                activebackground="#0f3460",
                relief="sunken",
                command=lambda r=row, c=col: place_symbol(r, c)
            )
            button.grid(row=row, column=col, padx=4, pady=4)
            buttons_in_row.append(button)
        buttons.append(buttons_in_row)


#RESTART

def restart_game():
    global win, current_player
    win = False
    current_player = "X"
    status_label.config(text="CURRENT PLAYER: X")

    for i in range(9):
        internal_board[i] = 0

    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text="", bg="#16213e")
            
    # In AIvsAI mode, AI should start first
    if game_mode_var.get() == "AIvsAI":
        current_player = ai_symbol
        root.after(500, lambda: ai_move(difficulty_var.get()))
    else:
        current_player = "X" if ai_symbol == "O" else "O"

    text_widget.config(state="normal")
    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, "AI tree paths will appear here after each AI move.")
    text_widget.config(state="disabled")


#CONTROLS

#text box to show the AI tree paths
text_widget = tk.Text(
    root,
    font=("Courier", 9),
    bg="#0d0d1a",
    fg="#00ff99",
    wrap="word",
    state="normal"
)
text_widget.insert(tk.END, "AI tree paths will appear here after each AI move.")
text_widget.config(state="disabled")
text_widget.place(x=500, y=50, height=400, width=370)

restart_button = tk.Button(
    root,
    text="RESTART",
    font=("Arial", 13),
    fg="white",
    bg="#e94560",
    activebackground="#c73652",
    relief="sunken",
    padx=10,
    command=restart_game
)
restart_button.grid(row=4, column=0, columnspan=3, pady=8)

#game mode radio buttons
mode_frame = tk.Frame(root, bg="#1a1a2e")
mode_frame.grid(row=5, column=0, columnspan=3, pady=4)

tk.Label(mode_frame, text="MODE:", font=("Arial", 11), bg="#1a1a2e", fg="white").pack(side="left")
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
tk.Radiobutton(
    mode_frame, text="AI vs AI",
    variable=game_mode_var, value="AIvsAI",
    font=("Arial", 11), bg="#1a1a2e", fg="white",
    selectcolor="#0f3460", activebackground="#1a1a2e"
).pack(side="left", padx=6)

#difficulty button
diff_frame = tk.Frame(root, bg="#1a1a2e")
diff_frame.grid(row=6, column=0, columnspan=3, pady=4)

tk.Label(diff_frame, text="Difficulty:", font=("Arial", 11), bg="#1a1a2e", fg="white").pack(side="left", padx=6)
difficulty_menu = tk.OptionMenu(diff_frame, difficulty_var, "EASY", "MEDIUM", "HARD")
difficulty_menu.config(font=("Arial", 11), bg="#0f3460", fg="white",
                       activebackground="#e94560", relief="flat")
difficulty_menu.pack(side="left")

#START

draw_grid()
root.mainloop()






