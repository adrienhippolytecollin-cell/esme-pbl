import tkinter as tk

#creating a window
root = tk.Tk()



#when the current player clicks, its symbol gets put on the grid 
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


#personnalising the window
root.title("tictactoe")
root.minsize(600 , 600)

draw_grid()
root.mainloop 

