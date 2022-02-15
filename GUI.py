from email import message
from tkinter import *
from tkinter import font
from tkinter import messagebox
from turtle import width
from PIL import ImageTk, Image
from PIL import ImageTk, Image

# set root window image and icon
ico_path = r"design\iv_plain_3.ico"
png_path = r"design\iv_plain.png"

root = Tk()

# define root prefs
root.title("aip webscraper")
root.iconbitmap(ico_path)
header_logo = ImageTk.PhotoImage(Image.open(png_path))
header_label = Label(root, image=header_logo)
header_label.grid(row=0, column=1)

# developer info
contact = Label(root, text="Developer: Dervis van Leersum", relief=SUNKEN, anchor=E)
contact.grid(row=7, column=0, columnspan=3, sticky=W+E)
contact.config(font=("Arial", 8, "italic"))

# frames in root grid
frame_one = LabelFrame(root, text="Login", padx=20, pady=5)
frame_one.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky=W+E)
frame_one.config(font=("Arial", 11))

frame_two = LabelFrame(root, text="Download info", padx=20, pady=5)
frame_two.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky=W+E)
frame_two.config(font=("Arial", 11))

frame_three = LabelFrame(root, text="Download whole batch", padx=20, pady=5)
frame_three.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky=W+E)
frame_three.config(font=("Arial", 11))

# functions for entry boxes
def on_entry_click_user(event):
    if user_entry.get() == "enter e-mail":
        user_entry.delete(0, "end")
        user_entry.insert(0, '')
        user_entry.config(fg='black')

def on_focusout_user(event):
    if user_entry.get() == "":
        user_entry.insert(0, 'enter e-mail')
        user_entry.config(fg='grey')

def on_entry_click_password(event):
    if password_entry.get() == "enter password":
        password_entry.delete(0, "end")
        password_entry.insert(0, '')
        password_entry.config(fg='black')

def on_focusout_password(event):
    if password_entry.get() == "":
        password_entry.insert(0, 'enter password')
        password_entry.config(fg='grey')

def on_entry_click_batch(event):
    if batch_entry.get() == "999":
        batch_entry.delete(0, "end")
        batch_entry.insert(0, '')
        batch_entry.config(fg='black')

def on_focusout_batch(event):
    if batch_entry.get() == "":
        batch_entry.insert(0, '999')
        batch_entry.config(fg='grey')

def on_entry_click_dest(event):
    if dest_entry.get() == "enter destination":
        dest_entry.delete(0, "end")
        dest_entry.insert(0, '')
        dest_entry.config(fg='black')

def on_focusout_dest(event):
    if dest_entry.get() == "":
        dest_entry.insert(0, 'enter destination')
        dest_entry.config(fg='grey')

# Entry boxes with label
user_entry = Entry(frame_one, width=52)
user_entry.grid(row=0, column=1, padx=20, pady=(10, 0))
user_entry.insert(0, "enter e-mail")
user_entry.bind('<FocusIn>', on_entry_click_user)
user_entry.bind('<FocusOut>', on_focusout_user)
user_entry.config(fg="grey")
user_label = Label(frame_one, text="Username: ")
user_label.grid(row=0, column=0, pady=(10, 0), sticky=E)

password_entry = Entry(frame_one, width=52)
password_entry.grid(row=1, column=1, padx=20, pady=(10, 0))
password_entry.insert(0, "enter password")
password_entry.bind('<FocusIn>', on_entry_click_password)
password_entry.bind('<FocusOut>', on_focusout_password)
password_entry.config(fg="grey")
password_label = Label(frame_one, text="Password: ")
password_label.grid(row=1, column=0, pady=(10, 10), sticky=E)

batch_entry = Entry(frame_two, width=7)
batch_entry.grid(row=0, column=1, padx=10, pady=(10, 0), sticky=W)
batch_entry.insert(0, "999")
batch_entry.bind('<FocusIn>', on_entry_click_batch)
batch_entry.bind('<FocusOut>', on_focusout_batch)
batch_entry.config(fg="grey")
batch_label = Label(frame_two, text="Batch number: ")
batch_label.grid(row=0, column=0, pady=(10, 0), sticky=E)

dest_entry = Entry(frame_two, width=50)
dest_entry.grid(row=1, column=1, padx=10, pady=(10, 0))
dest_entry.insert(0, "enter destination")
dest_entry.bind('<FocusIn>', on_entry_click_dest)
dest_entry.bind('<FocusOut>', on_focusout_dest)
dest_entry.config(fg="grey")
dest_label = Label(frame_two, text="Destination: ")
dest_label.grid(row=1, column=0, pady=(10, 10), sticky=E)

# options for radio nutton
all_download = ["Yes", "No"]

# radio button
action = IntVar()

radio_1 = Radiobutton(frame_three, text=all_download[0], variable=action, value=1)
radio_1.grid(row=0, column=0, sticky=W)
radio_2 = Radiobutton(frame_three, text=all_download[1], variable=action, value=2)
radio_2.grid(row=1, column=0, sticky=W)

# funcions for download button
def download_click():
    # first check of input
    if "@" not in user_entry.get( ):
        messagebox.showwarning("Oops", "Incorrect e-mail adres")
    elif password_entry.get() == "enter password" or password_entry.get() == "":
        messagebox.showwarning("Oops", "Incorrect password")
    elif dest_entry.get() == "enter destination" or dest_entry.get() == "":
        messagebox.showwarning("Oops", "Incorrect path")
    elif action.get() == 0:
        messagebox.showwarning("Oops", "Select full or single download option")
    else:
        try:
            if int(batch_entry.get()) == 999:
                messagebox.showwarning("Oops", "Incorrect batch number")
        except:
            messagebox.showwarning("Oops", "Input batch number not an integer")


# buttons
download_btn = Button(root, text="DOWNLOAD", command=download_click, padx=10, pady=5)
download_btn.grid(row=4, column=0, columnspan=3, pady=(0, 10))

root.mainloop()