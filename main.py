"""
AUTHOR: James San
Date: 11/15/2022
"""

from tkinter import *
from tkinter import messagebox
from random import choice
from time import sleep

keyboard_keys = {}
squares_list = []
CURRENT_SQUARE_CELL = 0
CURRENT_SQUARE_ROW = 0
end_of_row_flag = False
WIN_FLAG = None


""" COLORS """
bg = "black"
square_bg = "#3a3a3c"
keyboard_keys_colors = "#818384"
# keyboard_keys_colors_no = "#3a3a3c"
key_bg = "gray"
text_fg = "white"


""" SETTINGS """
title_font = ("Comic Sans MS", 48, "bold")
text_font = ("Comic Sans MS", 28, "bold")
small_text_font = ("Comic Sans MS", 16, "bold")
window_width = 610
window_height = 900
title = "Wordle"
square_width = square_height = 75
key_width = 50
key_height = 75
space = 10
filename = "wordbank.txt"


""" Reads from word bank. Grabs a random word """
wordbank = []
used_words = []
used_green_letters = []
with open(filename, "r") as f:
    wordbank = f.readlines()
    wordbank = [word.strip() for word in wordbank]

WORDLE_WORD = choice(wordbank)


""" SETUP """
root = Tk()
screen_width = root.winfo_screenwidth()  # Grabs the user's screen width
screen_height = root.winfo_screenheight()  # Grabs the user's screen height
x_pos = int((screen_width / 2) - (window_width / 2))
y_pos = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
root.title("CS1010-03 Wordle")
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

def is_word_valid(word):
    """ Returns True if the word is in the wordbank """
    global used_words
    if word in used_words:
        return False

    if word in wordbank:
        used_words.append(word)
        return True
    return False

def get_word():
    """ Returns the current row's word """
    my_squares_list = squares_list[CURRENT_SQUARE_ROW]
    word = ""
    for square in my_squares_list:
        word += square["text"]

    return word

def update_square_boxes(word):
    """ After the enter key is clicked, change the color of the boxes to green or yellow. Including the keyboard """
    global used_green_letters, WIN_FLAG
    temp_list = list(word)
    for index, letter in enumerate(temp_list):
        if letter in WORDLE_WORD:
            squares_list[CURRENT_SQUARE_ROW][index].config(bg="#c9b458")

            if letter not in used_green_letters:
                keyboard_keys[letter].config(bg="#c9b458")
        else:
            keyboard_keys[letter].config(bg="#3A3A3C")

        if letter == WORDLE_WORD[index]:
            used_green_letters.append(letter)
            squares_list[CURRENT_SQUARE_ROW][index].config(bg="#6aaa64")
            keyboard_keys[letter].config(bg="#6aaa64")

    if word == WORDLE_WORD:
        WIN_FLAG = True


""" Keyboard Listener Functions """
def pressed_key(event):
    key = event.char
    pressed(key)

def return_key(event):
    return_line()

def backspace_key(event):
    backspace()


def pressed(key):
    """ Whenever a valid alphabetical key is pressed, add it to the squares if there's space. """
    global CURRENT_SQUARE_ROW, CURRENT_SQUARE_CELL, WIN_FLAG

    # Makes game unplayable if there's a winner.
    if WIN_FLAG: return

    # Makes sure the key pressed is valid.
    if key not in keyboard_keys.keys():
        return

    # Check if the current row is filled with letters.
    if CURRENT_SQUARE_CELL % 5 == 0 and CURRENT_SQUARE_CELL != 0:
        return

    # Writes the letter to the screen.
    squares_list[CURRENT_SQUARE_ROW][CURRENT_SQUARE_CELL].config(text=key.upper(), fg=text_fg, font=text_font)

    # Increases counter by one
    CURRENT_SQUARE_CELL += 1

    global end_of_row_flag  # end_of_row_flag fixes a bug
    end_of_row_flag = False

def return_line():
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

    # Checks if the word on the current row is valid. If not, popup that the word is not valid.
    word = get_word().lower()
    if not is_word_valid(word):
        messagebox.showinfo("Wordle", "This word is not part of our wordbank or you used this word. Please chose a different word.")
        return

    update_square_boxes(word)

    # Player has won!
    global WIN_FLAG
    if WIN_FLAG:
        messagebox.askyesno("Wordle", f"Congrats you have beaten the game! The word was {WORDLE_WORD}. Would you like to try another game? ")

    # Increments to the beginning of the next row.
    CURRENT_SQUARE_ROW += 1
    CURRENT_SQUARE_CELL = 0

    end_of_row_flag = True

def backspace():
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
title_label = make_label(root, 0, 0, 75, window_width, text=title, bg=bg, fg=text_fg, font=title_font)  # Title screen
frame = Frame(root, height=2, width=window_width, bg=square_bg)  # Horizontal line break
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
    key_button = make_button(root, key_x, key_y, key_height, key_width, text=key.upper(), bg=keyboard_keys_colors, fg=text_fg, font=small_text_font, command=lambda a=key: pressed(a))
    keyboard_keys[key] = key_button  # Adds button to a dictionary to use for later
    key_x += key_width + space

# Second Row
key_x = 35  # x-pos of second row first col key
key_y = 730  # y-pos of second row keys
second_row_keys = ["a", "s", "d", "f", "g", "h", "j", "k", "l"]
for i, key in enumerate(second_row_keys):
    key_button = make_button(root, key_x, key_y, key_height, key_width, text=key.upper(), bg=keyboard_keys_colors, fg=text_fg, font=small_text_font, command=lambda a=key: pressed(a))
    keyboard_keys[key] = key_button  # Adds button to a dictionary to use for later
    key_x += key_width + space

# Third Row
key_x = 35  # x-pos of second row first col key
key_y = 815  # y-pos of second row keys
third_row_keys = ["ENTER", "z", "x", "c", "v", "b", "n", "m", "BACK"]
for i, key in enumerate(third_row_keys):

    # For the last row, the left and right most keys are a bit longer than the rest of the keys.
    if i == 0:
        key_button = make_button(root, key_x - 25, key_y, key_height, key_width + 25, text=key.upper(), bg=keyboard_keys_colors, fg=text_fg, font=small_text_font, command=return_line)
        keyboard_keys[key] = key_button  # Adds button to a dictionary to use for later
        key_x += key_width + space
        continue
    elif i == 8:
        key_button = make_button(root, key_x, key_y, key_height, key_width + 25, text=key.upper(), bg=keyboard_keys_colors, fg=text_fg, font=small_text_font, command=backspace)
        keyboard_keys[key] = key_button  # Adds button to a dictionary to use for later
        key_x += key_width + space
        continue

    key_button = make_button(root, key_x, key_y, key_height, key_width, text=key.upper(), bg=keyboard_keys_colors, fg=text_fg, font=small_text_font, command=lambda a=key: pressed(a))
    keyboard_keys[key] = key_button  # Adds button to a dictionary to use for later
    key_x += key_width + space


""" Event listener - Keyboard Input """
root.bind("<Return>", return_key)  # Enter key
root.bind("<BackSpace>", backspace_key)  # Backspace key
root.bind("<Key>", pressed_key)

print(WORDLE_WORD)

root.mainloop()
