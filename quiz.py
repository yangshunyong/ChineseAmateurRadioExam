#
#MIT License
#
#Copyright (c) 2022 Shunyong Yang (yang.shunyong@gmail.com)
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
#

import tkinter as tk
from tkinter import font
from enum import Enum
import random
import os
import sys
from tkinter import messagebox
from tkinter import font
from tkinter import messagebox

DIGRAM_LABLE_ENABLE = False

class MODE(Enum):
    STUDY = 0
    QUIZ = 1
    FAVORITE = 2
    WRONG = 3

class PARAM_TYPE(Enum):
    PARAM_INT = 0
    PARAM_LIST = 1

mode = MODE.STUDY
history_file_path ='history.txt'
favorite_file_path ='favorite.txt'
wrong_file_path ='wrong.txt'
exercise_class = 'A'
class_to_number = {
    'A':(30, 25),
    'B':(50, 40),
    'C':(80, 60),
}

mode_to_question_color = {
    MODE.STUDY: "black",
    MODE.QUIZ: "blue",
    MODE.FAVORITE: "green",
    MODE.WRONG: "red"
}

def save_config_to_file(file_path:str, parameter):
    with open(file_path, 'w') as file:
        if (isinstance(parameter, int)):
            file.write(str(parameter))
        elif (isinstance(parameter, list)) and all(isinstance(item, int) for item in parameter):
            for value in parameter:
                file.write(f"{value}\n")

def load_config_from_file(file_path:str, type: PARAM_TYPE):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            array = [int(line.strip()) for line in file]
            if (type == PARAM_TYPE.PARAM_LIST):
                return array
            else:
                return array[0]
    else:
        if (type == PARAM_TYPE.PARAM_LIST):
            return []
        else:
            return 0

def save_history():
    save_config_to_file(history_file_path, current_index)

def load_history():
    global history_index
    history_index = load_config_from_file(history_file_path, PARAM_TYPE.PARAM_INT)

def save_favorite():
    save_config_to_file(favorite_file_path, favorite_array)

def load_favorite():
    global favorite_array
    favorite_array = load_config_from_file(favorite_file_path, PARAM_TYPE.PARAM_LIST)

def save_wrong():
    save_config_to_file(wrong_file_path, wrong_array)

def load_wrong():
    global wrong_array
    wrong_array = load_config_from_file(wrong_file_path, PARAM_TYPE.PARAM_LIST)

# Define geometry of the root window
def scale_window():
    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate half of the screen width and height
    width = screen_width * 4 // 5
    height = screen_height * 4 // 5

    # Set the position of the window to the center of the screen
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Set the dimensions and position of the root window
    #root.geometry(f'{width}x{height}+{x}+{y}')

    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(family="Helvetica", size=16)

    # Set the default font for all widgets
    root.option_add("*Font", default_font)
    if (screen_width > 1920):
        root.minsize(width *2 // 3, 0)
    elif (screen_width >= 1400):
        root.minsize(width, 0)
    else:
        messagebox.showerror("警告", "请在1400以上的分辨率运行，不然会有画面缺失")
        sys.exit(-1)

    root.resizable(False, False)
    root.configure(bg=prog_background_color)

# Define a function to parse a single record
def parse_record(record_lines):
    record = {}
    for line in record_lines:
        if line.startswith("[I]"):
            record['id'] = line[3:].strip()
        if line.startswith("[Q]"):
            record['question'] = line[3:].strip()
        elif line.startswith("[A]"):
            record['A'] = line[3:].strip()
        elif line.startswith("[B]"):
            record['B'] = line[3:].strip()
        elif line.startswith("[C]"):
            record['C'] = line[3:].strip()
        elif line.startswith("[D]"):
            record['D'] = line[3:].strip()
    return record

# Initialize an empty list to hold all records
records = []

# Initialize an empty list to hold the lines of the current record
current_record_lines = []

# Open the file and read it line by line
with open('A-class.txt', 'r', encoding='gbk') as file:
    for line in file:
        line = line.strip()  # Remove leading/trailing whitespace
        if line.startswith("[I]"):  # Start of a new record
            if current_record_lines:  # If there's an existing record, parse it
                record = parse_record(current_record_lines)
                records.append(record)
                current_record_lines = []  # Reset for the next record
        current_record_lines.append(line)  # Add line to current record

    # Don't forget to parse the last record if the file doesn't end with [P]
    if current_record_lines:
        record = parse_record(current_record_lines)
        records.append(record)

# Now you have a list of records, each represented as a dictionary

'''
for record in records:
    print(record)
'''

# Assuming you have the 'records' list from the previous parsing code

# Function to update the display with the current record
def update_display(index):
    global choices
    
    answer_label.config(text="")
    record = records[index]
    question_label.config(text=record['question'])
    # Reset the selected answer variable
    selected_answer.set(None)

    # Shuffle answers to random
    random.shuffle(choices)
    # Update radio buttons with the current record's answers
    radio_a.config(text=record[choices[0]], value=0)
    radio_b.config(text=record[choices[1]], value=1)
    radio_c.config(text=record[choices[2]], value=2)
    radio_d.config(text=record[choices[3]], value=3)
    # Update the record index label
    if (mode == MODE.QUIZ):
        record_index_label.config(text=f"第 {quiz_index + 1} 题 ,共 {quiz_number} 题")
    elif (mode == MODE.FAVORITE):
        record_index_label.config(text=f"第 {favorite_index + 1} 题 ,共 {favorite_num} 题")
    elif (mode == MODE.WRONG):
        record_index_label.config(text=f"第 {wrong_index + 1} 题 ,共 {wrong_num} 题")        
    else:
        record_index_label.config(text=f"第 {index + 1} 题 ,共 {len(records)} 题")

def clear_display():
    answer_label.config(text="")
    question_label.config(text="")
    radio_a.config(text="")
    radio_b.config(text="")
    radio_c.config(text="")
    radio_d.config(text="")
    record_index_label.config(text="")

# Function to handle Next button click
def next_record():
    global current_index
    global quiz_index
    global favorite_index
    global wrong_index

    update = False

    if DIGRAM_LABLE_ENABLE:
        diagrm_label.pack()

    if (mode == MODE.QUIZ):
        if (quiz_index < (quiz_number - 1)):
            quiz_index += 1
            current_index = quiz_array[quiz_index]
            update = True
    elif (mode == MODE.FAVORITE):
        if (favorite_index < (favorite_num - 1)):
            favorite_index += 1
            current_index = favorite_array[favorite_index]
            update = True
    elif (mode == MODE.WRONG):
        if (wrong_index < (wrong_num - 1)):
            wrong_index += 1
            current_index = wrong_array[wrong_index]
            update = True
    else:
        if current_index < len(records) - 1:
            current_index += 1
            update = True;

    print("current_index:" + str(current_index))
    if (update):
        update_display(current_index)
# Function to handle Previous button click
def prev_record():
    global current_index
    global quiz_index
    global favorite_index
    global wrong_index

    if DIGRAM_LABLE_ENABLE:
        diagrm_label.pack_forget()

    update = False
    if (mode == MODE.QUIZ):
        if (quiz_index > 0):
            quiz_index -= 1
            current_index = quiz_array[quiz_index]
            update = True
    elif (mode == MODE.FAVORITE):
        if (favorite_index > 0):
            favorite_index -= 1
            current_index = favorite_array[favorite_index]
            update = True
    elif (mode == MODE.WRONG):
        if (wrong_index > 0):
            wrong_index -= 1
            current_index = wrong_array[wrong_index]
            update = True            
    else:
        if current_index > 0:
            current_index -= 1
            update = True

    print("current_index:" + str(current_index))
    if (update):
        update_display(current_index)            

# Function to handle jump button click
def jump_record():
    global current_index
    value = int(entry_index.get()) - 1
    if (value >= 0) and (value <= len(records) - 1):
        current_index = value
        update_display(current_index)


# Function to handle radio selected
def radio_selected():
    global wrong_num
    global history_index

    prompt = ''
    fg_color='green'
    answer = selected_answer.get()
    history_index = current_index
    save_history()

    if (choices[answer] == 'A'):
         prompt = correct_prompt
         if current_index not in correct_answer_array:
             correct_answer_array.append(current_index)
         if current_index in wrong_answer_array:
             wrong_answer_array.remove(current_index)
    else:
        fg_color='red'
        prompt = wrong_prompt
        if current_index not in wrong_array:
            wrong_array.append(current_index)
            save_wrong()
            wrong_num = len(wrong_array)
            print("wrong_num = " + str(wrong_num))
        if current_index not in wrong_answer_array:
            wrong_answer_array.append(current_index)
        if current_index in correct_answer_array:
            correct_answer_array.remove(current_index)


    update_status()

    prompt += " 共答对 " + str(len(correct_answer_array)) + " 题"
    prompt += " 共答错 " + str(len(wrong_answer_array)) + " 题"
    answer_label.config(text=prompt, fg = fg_color)

# Function to handle radio selected
def option_selected():
    global mode
    global choices
    global quiz_index
    global quiz_array
    global current_index
    global answer_wrong
    global answer_correct

    option = MODE(selected_option.get())
    total_quiz_number = len(records)

    wrong_answer_array.clear()
    correct_answer_array.clear()

    print(option)
    print(mode)

    question_label.config(fg=mode_to_question_color[option])
    if (option != MODE.FAVORITE):
        favorite_button.config(state=tk.NORMAL)
    else:
        favorite_button.config(state=tk.DISABLED)

    if ((option == MODE.FAVORITE) or (option == MODE.WRONG)):
        remove_button.config(state=tk.NORMAL)
    else:
        remove_button.config(state=tk.DISABLED)

    if (option == MODE.QUIZ):
        prev_button.config(state=tk.DISABLED)
    else:
        prev_button.config(state=tk.NORMAL)

    if (option != mode):
        mode = option
        if (mode == MODE.STUDY):
            current_index = 0
        elif (mode == MODE.FAVORITE):
            favorite_index = 0
            print("favorite_num = " + str(favorite_num))
            print(favorite_array)
            if (favorite_num == 0):
                clear_display()
                messagebox.showwarning("提示","没有题目!")
                return
            else:
                current_index = favorite_array[favorite_index]
        elif (mode == MODE.WRONG):
            wrong_index = 0
            print("wrong_num = " + str(wrong_num))
            print(wrong_array)
            if (wrong_num == 0):
                clear_display()
                messagebox.showwarning("提示","没有题目!")
                return;
            else:
                current_index = wrong_array[wrong_index]

        else:
            quiz_index = 0
            quiz_array = random.sample(range(total_quiz_number), quiz_number)
            current_index = quiz_array[quiz_index]
            print(quiz_array)
            print("current_index:" + str(current_index))

        update_display(current_index)

def add_favorite():
    global favorite_num
    if current_index not in favorite_array:
        favorite_array.append(current_index)
        save_favorite()
        favorite_num = len(favorite_array)
        print("favortie_num = " + str(favorite_num))

    update_status()

def remove_from_list():
    global current_index

    global favorite_index
    global favorite_num
    global favorite_array

    global wrong_index
    global wrong_num
    global wrong_array

    if (mode == MODE.FAVORITE):
        if current_index in favorite_array:
            favorite_array.remove(current_index)
        favorite_num = len(favorite_array)
        if (favorite_num == 0):
            clear_display()
            messagebox.showwarning("提示","没有题目!")
            favorite_index = 0
        else:
            if (favorite_index >= favorite_num) and (favorite_index > 0) :
                favorite_index -= 1
            current_index = favorite_array[favorite_index]
            update_display(current_index)

        save_favorite()
    elif (mode == MODE.WRONG):
        if current_index in wrong_array:
            wrong_array.remove(current_index)
        wrong_num = len(wrong_array)
        if (wrong_num == 0):
            clear_display()
            messagebox.showwarning("提示","没有题目!")
            wrong_index = 0
        else:
            if (wrong_index >= wrong_num) and (wrong_index > 0) :
                wrong_index -= 1

            current_index = wrong_array[wrong_index]
            update_display(current_index)

        save_wrong()
        update_status()

# Function to double the label's font size
# Function to set the label's font to bold
def bold_question():
    # Get the current font of the label
    current_font = font.nametofont(question_label['font'])
    
    # Create a new font object with the bold attribute
    bold_font = font.Font(family=current_font.actual()['family'], size=current_font.actual()['size'], weight='bold')
    
    # Update the label's font to the new bold font
def update_status():
    status_str = "状态：学习至第" +str(history_index + 1) + "题"
    status_str += " 收藏：" + str(favorite_num)
    status_str += " 错题：" + str(wrong_num)
    status_label.config(text=status_str)





# Initialize global variables
# Initialize the current record index        
current_index = 0
choices = ['A', 'B', 'C', 'D']
correct_prompt = "回答正确！"
wrong_prompt = "回答错误！"
prog_background_color = 'lightblue'

quiz_array = []
quiz_index = 0
quiz_number = class_to_number[exercise_class][0]
quiz_pass_number = class_to_number[exercise_class][1]
print("quiz info:" + str(quiz_number) + " " + str(quiz_pass_number))

favorite_array = []
favorite_index = 0
load_favorite()
favorite_num = len(favorite_array)
print("favorite_num:" + str(favorite_num))
print(favorite_array)

wrong_array = []
wrong_index = 0
load_wrong()
wrong_num = len(wrong_array)
print("wrong_num:" + str(wrong_num))
print(wrong_array)

wrong_answer_array = []
correct_answer_array = []

history_index = 0
load_history()
#print("previous =" + str(history_index))

# Initialize the Tkinter window
root = tk.Tk()
root.title("业余无线电考试题库-A级")
root.iconbitmap("icon.ico")

scale_window()
# Update display and get frame width
root.update_idletasks()
frame_width = root.winfo_width()

radio_wrap_width = frame_width * 4 / 5

# Create a variable to store the selected option
selected_option = tk.IntVar()

# Create a frame to hold the option widgests
option_frame = tk.Frame(root, borderwidth=2, relief="raised")
option_frame.pack(padx=10, pady=10, fill=tk.BOTH)
radio_study = tk.Radiobutton(option_frame, text="学习", variable=selected_option, value=0, \
                             justify=tk.LEFT, command=option_selected, wraplength=radio_wrap_width,borderwidth=0, padx=0)
radio_quiz = tk.Radiobutton(option_frame, text="考试", variable=selected_option, value=1, \
                             justify=tk.LEFT, command=option_selected, wraplength=radio_wrap_width,borderwidth=0, padx=0)
radio_favorite = tk.Radiobutton(option_frame, text="收藏夹", variable=selected_option, value=2, \
                             justify=tk.LEFT, command=option_selected, wraplength=radio_wrap_width,borderwidth=0, padx=0)
radio_wrong = tk.Radiobutton(option_frame, text="错题", variable=selected_option, value=3, \
                             justify=tk.LEFT, command=option_selected, wraplength=radio_wrap_width,borderwidth=0, padx=0)


entry_index=tk.Entry(option_frame)
jump_button = tk.Button(option_frame, text="跳转至题目", command=jump_record)
status_label = tk.Label(option_frame, text="", wraplength=radio_wrap_width, justify=tk.LEFT)
update_status()

radio_study.grid(row=0, column=0)
radio_quiz.grid(row=0, column=1)
radio_favorite.grid(row=0, column=2)
radio_wrong.grid(row=0, column = 3)

entry_index.grid(row=1, column=0)
jump_button.grid(row=1, column=1)
status_label.grid(row=2, column=0)

# Create a frame to hold the question label and question radio button
frame = tk.Frame(root, borderwidth=2, relief="raised")
frame.pack(padx=10, pady=10, fill=tk.BOTH)

# Create the display labels
question_label = tk.Label(frame, text="", wraplength=radio_wrap_width, justify=tk.LEFT)
bold_question()
question_label.pack(fill=tk.BOTH)

# Create a variable to store the selected answer
selected_answer = tk.IntVar()

# Create frame to hold following buttons
buttons_frame = tk.Frame(frame)
buttons_frame.pack(side=tk.TOP, fill=tk.X)
# Create a button for favorite
favorite_button = tk.Button(buttons_frame, text="收藏", command=add_favorite)
favorite_button.pack(side=tk.LEFT, padx=10)

# Create a button for remove
remove_button = tk.Button(buttons_frame, text="移除", command=remove_from_list)
remove_button.config(state=tk.DISABLED)
remove_button.pack(side=tk.RIGHT, padx=10)

# Create radio buttons for the answers
radio_a = tk.Radiobutton(frame, text="", variable=selected_answer, value=0, justify=tk.LEFT, command=radio_selected, wraplength=radio_wrap_width)
radio_a.pack(anchor=tk.W)

radio_b = tk.Radiobutton(frame, text="", variable=selected_answer, value=1, justify=tk.LEFT, command=radio_selected, wraplength=radio_wrap_width)
radio_b.pack(anchor=tk.W)

radio_c = tk.Radiobutton(frame, text="", variable=selected_answer, value=2, justify=tk.LEFT, command=radio_selected, wraplength=radio_wrap_width)
radio_c.pack(anchor=tk.W)

radio_d = tk.Radiobutton(frame, text="", variable=selected_answer, value=3, justify=tk.LEFT, command=radio_selected, wraplength=radio_wrap_width)
radio_d.pack(anchor=tk.W)

if DIGRAM_LABLE_ENABLE:
    digram = tk.PhotoImage(file="quad.gif")
    diagrm_label = tk.Label(frame, image=digram)
    diagrm_label.pack()

# Create the answer notification lable
answer_label = tk.Label(root, text="", wraplength=400, justify=tk.LEFT)
answer_label.configure(bg=prog_background_color)
answer_label.pack()

# Create author image
photo = tk.PhotoImage(file="quad.gif")
# Create a Label widget to display the image
label = tk.Label(root, image=photo)
label.pack()

# Create the record index label
record_index_label = tk.Label(root, text="")
record_index_label.configure(bg=prog_background_color)
record_index_label.pack()

# Create navigation buttons
prev_button = tk.Button(root, text="上一题", command=prev_record)
prev_button.pack(side=tk.LEFT, padx=10)

next_button = tk.Button(root, text="下一题", command=next_record)
next_button.pack(side=tk.RIGHT, padx=10)

# Update the display with the first record
update_display(current_index)

# Start the Tkinter event loop
root.mainloop()
