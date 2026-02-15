import tkinter 

# creating the grid 
def draw_grid():
  for col in range(3):
    for ro in range(3):
      button = tkinter.Button(
        root, font=("Arial", 100), 
        text="X", 
        width=5 height=3
      )
      button.grid(row=ro, column=col) 

#creating a window
root = tkinter.Tk()


#personnalising the window
root.title("tictactoe")
root.minsize(600 , 600) 
root.mainloop 
