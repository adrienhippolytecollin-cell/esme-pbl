import tkinter as tk

#creating the window
root = tk.Tk()


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

    clicked_button = buttons[column][row]
    if clicked_button['text'] == "":
        clicked_button.config(text=current_player)

        check_win(row, column)
        switch_player()


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



# parameters of the window
root.title("New game of TicTacToe")
root.minsize(500, 500)

draw_grid()
root.mainloop()
