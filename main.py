from tkinter import *

""" COLORS """
bg = "black"
square_bg = "gray"
key_bg = "gray"

""" SETTINGS """
root = Tk()
root.title("CS1010-03 Wordle")
root.geometry("610x900")
root.config(bg=bg)

""" Functions """
def make_label(master, x, y, h, w, *args, **kwargs):
    """ Used this function to create labels that are measured in units of px rather than units of text """
    frame = Frame(master, height=h, width=w)
    frame.pack_propagate(0)  # don't shrink
    frame.place(x=x, y=y)
    label = Label(frame, *args, **kwargs)
    label.pack(fill=BOTH, expand=1)
    return label

""" TODO Title Screen """
# title_label = Label(title_frame, text="Wordle")
# title_label.grid(row=0)

""" Main Screen """
square_y = 110
for i in range(6):
    square_x = 97.5
    for j in range(5):
        square_label = make_label(root, square_x, square_y, 75, 75, text="J")

        square_x += 85
    square_y += 85

""" TODO: Character Screen """


root.mainloop()