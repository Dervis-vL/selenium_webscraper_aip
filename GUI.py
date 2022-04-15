from tkinter import *
from tkinter import font
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
from PIL import ImageTk, Image
from matplotlib.pyplot import box
from codebase import scraper
import re

# run as admin
ADMIN = True
scraper.admin(ADMIN)

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

frame_three = LabelFrame(root, text="Download", padx=20, pady=5)
frame_three.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky=W+E)
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

# opens dialog box to manually select the destination
def dialog_box():
    root.folder = filedialog.askdirectory(initialdir=r"c:\Users", title="Select directory")
    dest_entry.delete(0, "end")
    dest_entry.insert(0, root.folder)
    dest_entry.config(fg='black')

# check for direct_login input from login folder. 
login = open("login\\direct_login.txt", 'r')
find = login.read()
regex_tag_user = 'Username: "(.*?)"'
regex_tag_pass = 'Password: "(.*?)"'
username_regex = re.findall(regex_tag_user, str(find))
password_regex = re.findall(regex_tag_pass, str(find))
print(username_regex, password_regex)

# Auto user input
if len(username_regex[0]) > 1:
    user_input = username_regex[0]
else: 
    user_input = "enter e-mail"

if len(password_regex[0]) > 1:
    pass_input = password_regex[0]
else:
    pass_input= "enter password"

# Entry boxes with label
user_entry = Entry(frame_one, width=52)
user_entry.grid(row=0, column=1, padx=20, pady=(10, 0))
user_entry.insert(0, user_input)
user_entry.bind('<FocusIn>', on_entry_click_user)
user_entry.bind('<FocusOut>', on_focusout_user)
user_entry.config(fg="grey")
user_label = Label(frame_one, text="Username: ")
user_label.grid(row=0, column=0, pady=(10, 0), sticky=E)

password_entry = Entry(frame_one, width=52, show="*")
password_entry.grid(row=1, column=1, padx=20, pady=(10, 0))
password_entry.insert(0, pass_input)
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
all_download = ["Whole batch", "Single object", "Assets in Excel"]

# radio button for download type
action = IntVar()

radio_1 = Radiobutton(frame_three, text=all_download[0], variable=action, value=1)
radio_1.grid(row=0, column=0, sticky=W)
radio_2 = Radiobutton(frame_three, text=all_download[1], variable=action, value=2)
radio_2.grid(row=1, column=0, sticky=W)
radio_3 = Radiobutton(frame_three, text=all_download[2], variable=action, value=3)
radio_3.grid(row=2, column=0, sticky=W)

# funcions for download button
def download_click():
    ready = False
    # first check of input
    if "@" not in user_entry.get( ):
        messagebox.showwarning("Oops", "Incorrect e-mail adres")
    elif password_entry.get() == "enter password" or password_entry.get() == "":
        messagebox.showwarning("Oops", "Incorrect password")
    elif dest_entry.get() == "enter destination" or dest_entry.get() == "":
        messagebox.showwarning("Oops", "Incorrect path")
    elif action.get() == 0:
        messagebox.showwarning("Oops", "Select full, single or asset download option")
    else:
        try:
            if int(batch_entry.get()) >= 999:
                messagebox.showwarning("Oops", "Incorrect batch number")
            else:
                ready = True
        except:
            messagebox.showwarning("Oops", "Input batch number not an integer")
    
    # test is positive; run tool
    if ready:
        # url to get with driver
        url = "https://aip.amsterdam.nl"
        username = user_entry.get()
        password = password_entry.get()
        batch = batch_entry.get()
        directory = dest_entry.get()
        download = action.get()

        # pass input data through scraper
        selenium_options = scraper.input_scraper(batch, directory)

        # find correct driver
        driver = scraper.version_find(selenium_options[0])

        # check for notifications
        if driver[1] == False:
            messagebox.showwarning("Oops", "Your version of chrome is not found. Contact developer.")
        else:
            driver[0].get(url)

            brus_found = scraper.login(username, password, driver[0], selenium_options[2])

            if len(brus_found) == 0:
                messagebox.showwarning("Oops", "Loading objects failed. Try again.")
                driver[0].quit()
            else:
                # download whole batch
                if download == 1:
                    total = scraper.all_data(brus_found, driver[0], selenium_options[3], selenium_options[4], selenium_options[1])
                    
                    progress = Toplevel()
                    progress.title("Progress window")
                    progress.iconbitmap(ico_path)
                    # progress_text = "(" + str(count_loop) + "/" + str(len(brus_found)) + "): " + "From " + str(selenium_options[4]) + " and object " + str(bru_select.get().rstrip()) + " there were " + str(len(brus_found)) + " files downloaded."
                    # progress_bru = Label(progress, text=progress_text, justify=LEFT)
                    # progress_bru.grid(row=1, column=0, padx=8, pady=(5, 5), sticky=W)
                    progress_compl = Label(progress, text="Download has completed, see downloading time:", justify=LEFT)
                    progress_compl.grid(row=2, column=0, padx=8, pady=(5, 5), sticky=W)
                    progress_time = Label(progress, text=total, justify=LEFT)
                    progress_time.grid(row=3, column=0, padx=8, pady=(5, 5), sticky=W)
                    progress_close = Label(progress, text="!__You can close this window now__!", justify=LEFT)
                    progress_close.grid(row=4, column=0, padx=8, pady=(5, 5), sticky=W)
                    progress_donger = Label(progress, text="ლ ( ◕  ᗜ  ◕ ) ლ", justify=LEFT)
                    progress_donger.grid(row=5, column=0, padx=8, pady=(5, 5), sticky=W)
                # download excel sheets only
                elif download == 3:
                    scraper.all_assets(brus_found, driver[0], selenium_options[3], selenium_options[1])
                # download single object
                else:
                    bru_level = Toplevel()
                    bru_level.title("Select object")
                    bru_level.iconbitmap(ico_path)

                    bru_label = Label(bru_level, text="Select object for download:", justify=LEFT)
                    bru_label.grid(row=0, column=0, padx=8, pady=(10, 5), sticky=W)
                    bru_label.config(font=("Arial", 11))

                    count = 0
                    bru_select = StringVar()
                    bru_select.set(brus_found[0])
                    for bru in brus_found:
                        Radiobutton(bru_level, text=bru, variable=bru_select, value=bru).grid(row=count+1, column=0, sticky=W, padx=(80, 50))
                        count += 1
                    
                    def single_click():
                        count_loop = 1
                        bru_selected = bru_select.get().rstrip()
                        for bru in brus_found:
                            if bru == bru_select.get():
                                # TODO: add waiting window
                                bru_level.destroy()

                                single = scraper.single_data(driver[0], count_loop, bru_selected, selenium_options[3], selenium_options[1])
                                
                                progress = Toplevel()
                                progress.title("Progress window")
                                progress.iconbitmap(ico_path)
                                progress_text = "(" + str(count_loop) + "/" + str(len(brus_found)) + "): " + "From " + str(selenium_options[4]) + " and object " + str(bru_select.get().rstrip()) + " there were " + str(single[1]) + " files downloaded."
                                progress_bru = Label(progress, text=progress_text, justify=LEFT)
                                progress_bru.grid(row=1, column=0, padx=8, pady=(5, 5), sticky=W)
                                progress_compl = Label(progress, text="Download has completed, see downloading time:", justify=LEFT)
                                progress_compl.grid(row=2, column=0, padx=8, pady=(5, 5), sticky=W)
                                progress_time = Label(progress, text=single[0], justify=LEFT)
                                progress_time.grid(row=3, column=0, padx=8, pady=(5, 5), sticky=W)
                                progress_close = Label(progress, text="!__You can close this window now__!", justify=LEFT)
                                progress_close.grid(row=4, column=0, padx=8, pady=(5, 5), sticky=W)
                                progress_donger = Label(progress, text="ლ ( ◕  ᗜ  ◕ ) ლ", justify=LEFT)
                                progress_donger.grid(row=5, column=0, padx=8, pady=(5, 5), sticky=W)

                            else:
                                count_loop += 1

                    single_btn = Button(bru_level, text="CONFIRM", command=single_click, padx=10, pady=5)
                    single_btn.grid(row=len(brus_found)+2, column=0, columnspan=3, pady=(4, 10))


        # close interface when ready
        # root.destroy

# buttons
dest_btn = Button(root, text="Select destination", command=dialog_box, borderwidth=3)
dest_btn.grid(row=3, column=0, columnspan=3, pady=(0, 15))
download_btn = Button(root, text="DOWNLOAD", command=download_click, padx=10, pady=5)
download_btn.grid(row=6, column=0, columnspan=3, pady=(0, 10))

root.mainloop()