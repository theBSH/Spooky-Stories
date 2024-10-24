import os, sys
import customtkinter as ui
from customtkinter import filedialog as fd
from tkinter import messagebox as mb
from collections import defaultdict
dirr = os.path.dirname(__file__)

ui.set_appearance_mode("dark")
ui.set_default_color_theme(os.path.join(dirr, "themes", "main.json"))


root = ui.CTk()
root.title("Spooky Stories")
root.resizable(False, False)
root.iconbitmap(os.path.join(dirr, "spokystories.ico"))

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_x = (screen_width // 2) - (900 // 2)
position_y = (screen_height // 2) - (600 // 2)
root.geometry(f'900x600+{position_x}+{position_y}')


try:
    from ctypes import windll
    myappid = u'BloodShot.SpookyStories.2'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

title = ui.CTkLabel(master=root, text="Spooky Stories", font=("Monster Pumpkin", 50),height=70,width=100,anchor="s")
title.place(relx=0.5, rely=0.1, anchor=ui.CENTER)

ver = ui.CTkLabel(master=root, text="V2", font=("Monster Pumpkin", 20),anchor="s",fg_color="transparent")
ver.place(relx=0.05, rely=0.95, anchor=ui.CENTER)

def load_story():
    filet = (('story files', '*.txt'),)

    def checkstory():
        global story
        story = fd.askopenfilename(title="select story file", filetypes=filet,initialdir=os.path.join(dirr, "stories"))
        if story:
            with open(story, 'r') as main:
                s = main.readline().strip()
                if (s != "#ssfile"):
                    mb.showerror(title="Error", message="pls select a supported file")
                    checkstory()
                else:
                    global button3
                    button3 = ui.CTkButton(master=root, text="start", command=main_story, font=("Monster Pumpkin", 15))
                    button3.place(relx=0.5, rely=0.6,anchor=ui.CENTER)
        else:
            mb.showerror(title="Error", message="Please select the story first")
    
    checkstory()

button1 = ui.CTkButton(master=root, text="select your story",width=230, command=load_story, font=("Monster Pumpkin", 30),height=50)
button1.place(relx=0.5, rely=0.25, anchor=ui.CENTER)

def main_story():
    if story:
        textbox1 = ui.CTkEntry(master=root, font=("Monster Pumpkin", 20))
        textbox1.insert(0, "name")
        textbox1.place(relx=0.3, rely=0.4, anchor=ui.CENTER)

        next_pressed = ui.StringVar()
        button2 = ui.CTkButton(master=root, text="Next", command=lambda: next_pressed.set("yes"), font=("Monster Pumpkin", 13))
        button2.place(relx=0.7, rely=0.4, anchor=ui.CENTER)

        def on_entry_click(event):
            textbox1.delete(0, ui.END)
        textbox1.bind("<FocusIn>", on_entry_click)

        name = textbox1.get()
        button2.wait_variable(next_pressed)
        textbox1.delete(0, ui.END)
        button2.focus_set()
        textbox1.insert(0, "age")
        button2.wait_variable(next_pressed)
        def checknumber():
            if (textbox1.get().isnumeric()):
                return textbox1.get()
            else:
                mb.showerror(title="Error", message="pls only enter digits")
                textbox1.delete(0, ui.END)
                button2.focus_set()
                textbox1.insert(0, "age")
                button2.wait_variable(next_pressed)
                checknumber()
        
        age = checknumber()

        textbox1.delete(0, ui.END)
        textbox1.configure(width=160)
        textbox1.insert(0, "describe your self")
        button2.focus_set()
        button2.wait_variable(next_pressed)
        des = textbox1.get()

        textbox1.delete(0, ui.END)
        textbox1.configure(width=140)
        button2.focus_set()
        textbox1.insert(0, "woman/man")
        button2.wait_variable(next_pressed)
        def checkgender():
            if (textbox1.get() == "woman" or textbox1.get() == "man"):
                return textbox1.get()
            else:
                mb.showerror(title="Error", message="pls only enter woman/man")
                textbox1.delete(0, ui.END)
                button2.focus_set()
                textbox1.insert(0, "woman/man")
                button2.wait_variable(next_pressed)
                checkgender()
    
        gender = checkgender()

        textbox1.delete(0, ui.END)
        button2.focus_set()
        textbox1.insert(0, "obj")
        button2.wait_variable(next_pressed)
        obj = textbox1.get()

        textbox1.delete(0, ui.END)
        button2.focus_set()
        textbox1.insert(0, "name the story")
        button2.wait_variable(next_pressed)
        story_name = textbox1.get() + "\n"

        with open(story, 'r') as main:
            s = main.readlines()
            s = [i for i in s if "#ssfile" not in i]
            stor = s[0]
            story_values = defaultdict(str, {
                'gender': 'girl' if gender == 'woman' else 'boy',
                'pronoun': 'her' if gender == 'woman' else 'him',
                'pronoun2': 'she' if gender == 'woman' else 'he',
                'possession': 'her' if gender == 'woman' else 'his',
                'name': name,
                'age': age,
                'des': des,
                'obj': obj
            })
            stor = stor.format_map(story_values)

        export = fd.asksaveasfile(mode='w', defaultextension=".txt")
        if export is None:
            mb.showerror(title="error", message="didn't save")
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
    else:
        mb.showerror(title="Error", message="Please select the story first")

root.mainloop()
