"""
AUTHOR: James San
Date: 11/15/2022
"""

from tkinter import *

keyboard_keys = {}
squares_list = []
CURRENT_SQUARE_CELL = 0
CURRENT_SQUARE_ROW = 0
end_of_row_flag = False


""" COLORS """
bg = "black"
square_bg = "gray"
key_bg = "gray"
text_fg = "white"


""" SETTINGS """
title_font = ("Comic Sans MS", 48, "bold")
screen_width = 610
screen_height = 900
title = "Wordle"
square_width = square_height = 75
key_width = 50
key_height = 75
space = 10


""" SETUP """
root = Tk()
root.title("CS1010-03 Wordle")
root.geometry(f"{screen_width}x{screen_height}")
root.config(bg=bg)


""" FUNCTIONS """
def make_label(root, x, y, h, w, *args, **kwargs):
    """ Used this function to create labels that are measured in units of px rather than units of text """
    frame = Frame(root, height=h, width=w)
    frame.pack_propagate(0)
    frame.place(x=x, y=y)
    label = Label(frame, *args, **kwargs)
    label.pack(fill=BOTH, expand=1)
    return label


def make_button(root, x, y, h, w, *args, **kwargs):
    """ Used this function to create buttons that are measured in units of px rather than units of text """
    frame = Frame(root, height=h, width=w)
    frame.pack_propagate(0)
    frame.place(x=x, y=y)
    button = Button(frame, *args, **kwargs)
    button.pack(fill=BOTH, expand=1)
    return button


""" Keyboard Listener Functions """
def pressed_key(event):
    """ Whenever a valid alphabetical key is pressed, add it to the squares if there's space. """
    global CURRENT_SQUARE_ROW, CURRENT_SQUARE_CELL
    # Makes sure the key pressed is valid.
    if event.char not in keyboard_keys.keys():
        return

    # Check if the current row is filled with letters.
    if CURRENT_SQUARE_CELL % 5 == 0 and CURRENT_SQUARE_CELL != 0:
        return

    # Writes the letter to the screen.
    squares_list[CURRENT_SQUARE_ROW][CURRENT_SQUARE_CELL].config(text=event.char)

    # Increases counter by one
    CURRENT_SQUARE_CELL += 1

    global end_of_row_flag  # end_of_row_flag fixes a bug
    end_of_row_flag = False


def return_key(event):
    """
    When pressed, it attempts to submit the word
    Check: If the word is a repeat, exists, and is 5 characters.
    If wrong: Update the board by starting a new line, change keyboard colors, and change board colors
    If right: Update the board by congratulating them for winning, prompt new game.
     """
    global CURRENT_SQUARE_ROW, CURRENT_SQUARE_CELL
    # Check if there is 5 characters in the row.
    if CURRENT_SQUARE_CELL % 5 != 0:
        return

    global end_of_row_flag  # end_of_row_flag fixes a bug
    if end_of_row_flag:
        return

    # Increments to the beginning of the next row.
    CURRENT_SQUARE_ROW += 1
    CURRENT_SQUARE_CELL = 0

    end_of_row_flag = True


def backspace_key(event):
    """
    When pressed, it removes a character
    Check: If there is atleast 1 character on the screen.
    """
    global CURRENT_SQUARE_ROW, CURRENT_SQUARE_CELL
    global end_of_row_flag  # end_of_row_flag fixes a bug
    # Do not run function if there are no characters in the row.
    if CURRENT_SQUARE_CELL == 0:
        end_of_row_flag = True
        return

    CURRENT_SQUARE_CELL -= 1

    # Remove the most recent character
    squares_list[CURRENT_SQUARE_ROW][CURRENT_SQUARE_CELL].config(text="")

    end_of_row_flag = False


""" Title Screen """
title_label = make_label(root, 0, 0, 75, screen_width, text=title, bg=bg, fg=text_fg, font=title_font)  # Title screen
frame = Frame(root, height=2, width=screen_width, bg=square_bg)  # Horizontal line break
frame.place(x=0, y=75)

""" Main Screen """
square_y = 110
for i in range(6):
    square_x = 97.5
    temp_square_list = []
    for j in range(5):
        square_label = make_label(root, square_x, square_y, square_width, square_height, text="", bg=square_bg)
        temp_square_list.append(square_label)
        square_x += 85
    square_y += 85
    squares_list.append(temp_square_list)

""" Keyboard Screen """
""" There are going to be 3 rows to the keyboard. 10-9-9 """
# First Row
keyboard = []  # list used to store buttons
key_x = 10  # x-pos of first col key
key_y = 645  # y-pos of first row keys
first_row_keys = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"]
for i, key in enumerate(first_row_keys):
    key_button = make_button(root, key_x, key_y, key_height, key_width, text=key)
    keyboard_keys[key] = key_button  # Adds button to a dictionary to use for later
    key_x += key_width + space

# Second Row
key_x = 35  # x-pos of second row first col key
key_y = 730  # y-pos of second row keys
second_row_keys = ["a", "s", "d", "f", "g", "h", "j", "k", "l"]
for i, key in enumerate(second_row_keys):
    key_button = make_button(root, key_x, key_y, key_height, key_width, text=key)
    keyboard_keys[key] = key_button  # Adds button to a dictionary to use for later
    key_x += key_width + space

# Third Row
key_x = 35  # x-pos of second row first col key
key_y = 815  # y-pos of second row keys
third_row_keys = ["ENTER", "z", "x", "c", "v", "b", "n", "m", "BACKSPACE"]
for i, key in enumerate(third_row_keys):

    # For the last row, the left and right most keys are a bit longer than the rest of the keys.
    if i == 0:
        key_button = make_button(root, key_x - 25, key_y, key_height, key_width + 25, text=key)
        keyboard_keys[key] = key_button  # Adds button to a dictionary to use for later
        key_x += key_width + space
        continue
    elif i == 8:
        key_button = make_button(root, key_x, key_y, key_height, key_width + 25, text=key)
        keyboard_keys[key] = key_button  # Adds button to a dictionary to use for later
        key_x += key_width + space
        continue

    key_button = make_button(root, key_x, key_y, key_height, key_width, text=key)
    keyboard_keys[key] = key_button  # Adds button to a dictionary to use for later
    key_x += key_width + space


""" Event listener - Keyboard Input """
root.bind("<Return>", return_key)  # Enter key
root.bind("<BackSpace>", backspace_key)  # Backspace key
root.bind("<Key>", pressed_key)


root.mainloop()
