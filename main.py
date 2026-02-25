import tkinter as tk

#creating a window
root = tk.Tk()


#choosing the current player 
def switch_player():
    global current_player
    if current_player == 'X':
        current_player = '0'
    else:
        current_player = 'X'

#when the current player clicks, its corresponding symbol gets put on the grid 
def place_symbol(row, column):

    clicked_button = buttons[column][row]
    if clicked_button['text'] == "":
        clicked_button.config(text=current_player)



#drawing the grid
def draw_grid():
    for column in range(3):
        buttons_in_cols = []
        for row in range(3):
            button = tk.Button(
                root, font=("Arial", 50),
                width=5, height=2,
                command=lambda r=row, c=column: place_symbol(r, c)
            )
            button.grid(row=row, column=column)
            buttons_in_cols.append(button)
        buttons.append(buttons_in_cols)

def print_winner():
    global win
    if win is False:
        win = True
        print("Le joueur", current_player, "a gagné le jeu")


def check_win(current_row, current_col):

    # detecter victoire horizontale
    count = 0
    for i in range(3):
        current_button = buttons[i][current_row]
        if current_button['text'] == current_player:
            count += 1
    if count == 3:
        print_winner()

    # detecter victoire verticale
    count = 0
    for i in range(3):
        current_button = buttons[current_col][i]
        if current_button['text'] == current_player:
            count += 1
    if count == 3:
        print_winner()

    # detecter victoire diagonale
    count = 0
    for i in range(3):
        current_button = buttons[i][i]
        if current_button['text'] == current_player:
            count += 1
    if count == 3:
        print_winner()

    # detecter victoire diagonale inversee
    count = 0
    for i in range(3):
        current_button = buttons[2-i][i]
        if current_button['text'] == current_player:
            count += 1
    if count == 3:
        print_winner()

    if win is False:
        count = 0
        for col in range(3):
            for row in range(3):
                current_button = buttons[col][row]
                if current_button['text'] == 'X' or current_button['text'] == '0':
                    count += 1
        if count == 9:
            print("Match nul")


#personnalising the window
root.title("tictactoe")
root.minsize(600 , 600)

draw_grid()
root.mainloop 



