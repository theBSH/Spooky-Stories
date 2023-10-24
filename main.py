import os
import tkinter as ui
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb

root = ui.Tk()
root.title("Spooky Stories")
root.geometry("900x600")
root.config(background="orange")
root.resizable(False, False)
dirr = os.path.dirname(__file__)
root.iconbitmap(os.path.join(dirr, "spokystories.ico"))
# made the root window and added the icon
try:
    from ctypes import windll

    myappid = u'BloodShot.FunPython.SpookyStories.1'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass
# if the app is on windows, then we set a custom appid if not we pass

# -------------------------------------
title = ui.Label(text="Spooky Stories", background="white", foreground="black", relief="solid", borderwidth=5,
                 font=("Monster Pumpkin", 40))
title.grid(row=0, column=0, padx=0, pady=20)
title.place(relx=0.5, rely=0.1, anchor=CENTER)


# main label

# --------------------------------------
def load_story():
    filet = (
        ('story files', '*.txt'),
    )
    # noinspection PyGlobalUndefined
    global story
    story = fd.askopenfilename(title="select story file", filetypes=filet)
    # noinspection PyGlobalUndefined
    global button3
    button3 = ui.Button(text="start", background="white", foreground="black", command=main_story,
                        font=("Monster Pumpkin", 15))
    button3.grid(row=3, column=0)
    button3.place(relx=0.49, rely=0.6)


button1 = ui.Button(text="select your story", background="white", foreground="black", command=load_story,
                    font=("Monster Pumpkin", 20))
button1.grid(row=1, column=0, padx=0, pady=50)
button1.place(relx=0.39, rely=0.2)


# load story button and function

def main_story():
    if len(story) > 0:
        # checks if there is something in the story file directory if not we throw an error on line 128
        textbox1 = ui.Entry(background="white", foreground="black",
                            font=("Monster Pumpkin", 20))
        textbox1.insert(0, 'name')
        textbox1.grid(row=2, column=0, padx=0, pady=70)
        textbox1.place(relx=0.3, rely=0.4)
        # ---------------------------------------
        next_pressed = StringVar()
        button2 = ui.Button(text="Next", background="white", foreground="black",
                            command=lambda: next_pressed.set("yes"),
                            font=("Monster Pumpkin", 13))
        button2.grid(row=2, column=1, padx=0, pady=70)
        button2.place(relx=0.7, rely=0.4)
        # a next button to go to the next question and works with a string var and wait_variable function
        # ----------------------------------------
        name = textbox1.get()
        button2.wait_variable(next_pressed)
        textbox1.delete(0, END)
        textbox1.insert(0, "age")
        button2.wait_variable(next_pressed)
        age = textbox1.get()
        # -----------------------------------------
        textbox1.delete(0, END)
        textbox1.insert(0, "how do you describe your self?")
        button2.wait_variable(next_pressed)
        des = textbox1.get()
        # -----------------------------------------
        textbox1.delete(0, END)
        textbox1.insert(0, "woman/man")
        button2.wait_variable(next_pressed)
        gender = textbox1.get()
        # -----------------------------------------
        textbox1.delete(0, END)
        textbox1.insert(0, "obj")
        button2.wait_variable(next_pressed)
        obj = textbox1.get()
        # -----------------------------------------
        textbox1.delete(0, END)
        textbox1.insert(0, "name the story")
        button2.wait_variable(next_pressed)
        story_name = textbox1.get() + "\n"
        with open(story, 'r') as main:
            # we open the story file and use string concat for mad-libs (not the best implementation for sure)
            s = main.readlines()[0]
            stor = s
            if gender == 'woman':
                stor = stor.format(gender='girl', pronoun='her', name=name, age=age, des=des, pronoun2='she', obj=obj)
            if gender == 'man':
                stor = stor.format(gender='boy', pronoun='his', name=name, age=age, des=des, pronoun2='he', obj=obj)
        export = fd.asksaveasfile(mode='w', defaultextension=".txt")
        # then we save a new file
        if export is None:
            # if the person clicks cancel, we throw an error and restart
            mb.showerror(title="error", message="didnt save")
            textbox1.destroy()
            button2.destroy()
            return
        export.write(story_name)
        export.write(stor)
        mb.showinfo(title="complete", message="your story is now saved")
        export.close()
        textbox1.destroy()
        button2.destroy()
        button3.destroy()
        # we restart here
    else:
        mb.showerror(title="Error", message="pls select the story first")


# the main app after start button is clicked

root.mainloop()
