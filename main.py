import os
import random
import sys
import threading
import time
import tkinter
import tkinter.messagebox
import tkinter.ttk as ttk

import tkmacosx
import ttkthemes
from PIL import Image

import splashscreen

THEME = "Clearlooks"


def calculate_standard_drink(abv, volume):
    """Calculate the number of standard drink in a drink"""
    return round(abv * volume / 1000, 2)


splash = splashscreen.SplashScreen(Image.open(os.path.join("splashscreen.png")),
                                   most_common_color_idx=random.randint(0, 4),
                                   theme=THEME,
                                   )

tk = ttkthemes.ThemedTk(theme=THEME, baseName="Drunkmeter")
# Set the file icon.png as the icon of the window
splash.tk.call('wm', 'iconphoto', splash._w, tkinter.PhotoImage(file=os.path.join("icon.png")))

for row in range(5):
    tk.rowconfigure(row, weight=1)
for col in range(3):
    tk.columnconfigure(col, weight=1)

abv_label = tkinter.Label(tk, text="ABV (%)")
abv_label.grid(row=0, column=0)

vol_label = tkinter.Label(tk, text="Volume (ml)")
vol_label.grid(row=0, column=1, columnspan=2)

vol_var = tkinter.StringVar()
abv_var = tkinter.StringVar()

abv_entry = tkinter.Entry(tk, textvariable=abv_var)
abv_entry.grid(row=1, column=0)

vol_entry = tkinter.Entry(tk, textvariable=vol_var)
vol_entry.grid(row=1, column=1)

result_label = tkinter.Label(tk, text="Result: ")
result_label.grid(row=1, column=2)

def calculate():
    try:
        if float(abv_var.get()) >= 100:
            tkinter.messagebox.showerror(
                "Error", "ABV must be less than 100%", icon="error", parent=tk)
            return
        elif float(abv_var.get()) <= 0:
            tkinter.messagebox.showerror(
                "Error", "ABV must be greater than 0%", icon="error", parent=tk)

        if float(vol_var.get()) <= 0:
            tkinter.messagebox.showerror(
                "Error", "Volume must be greater than 0", icon="error", parent=tk)
            return
        standard_drinks = calculate_standard_drink(
            float(abv_var.get()), float(vol_var.get()))
        result = f"{standard_drinks} standard drink{standard_drinks > 1 and 's' or ''}"
    except ValueError as e:
        # tkinter.messagebox.showerror("Error", str(e), icon="error", parent=tk)
        result = "Invalid input"

    result_label.config(text="Result: {}".format(result))


calculate_btn = tkmacosx.Button(tk, text="Calculate", command=calculate)
calculate_btn.configure(bg="#FFC000", fg="black",
                        activebackground="#ffd558", activeforeground="black")
calculate_btn.grid(row=2, column=0, columnspan=3, padx=10)

# Display a grid displaying the alcohol dosage according to psychonautwiki
dosage_label = tkinter.Label(tk, text="Alcohol dosage (units)")
dosage_label.grid(row=3, column=0, columnspan=3)

dosage_table = tkinter.Listbox(tk)
dosage_table.grid(row=4, column=0, columnspan=3)
# Set the dosage table items to be unselectable and to display 5 items
dosage_table.config(selectmode="none", height=5)

dosage_table.insert(tkinter.END, "Threshold: 1 standard drink")
dosage_table.insert(tkinter.END, "Light: 1-3 standard drinks")
dosage_table.insert(tkinter.END, "Common: 3-5 standard drinks")
dosage_table.insert(tkinter.END, "Strong: 5-6 standard drinks")
dosage_table.insert(tkinter.END, "Heavy: 6+ standard drinks")

loading_texts = ["Loading wines", "Opening cans of beers",
                 "Loading spirits", "Mixing cocktails", "Pouring shots"]

def loading_thread():
    # Focus to the loading window
    splash.focus_force()
    if sys.platform in ['win32', 'cygwin']:
        tk.wm_attributes("-disabled", True)
    time.sleep(0.5)
    for i, text in enumerate(loading_texts):
        splash.loading_status = text
        time.sleep(0.5 * i)
    
    if sys.platform in ['win32', 'cygwin']:
        tk.wm_attributes("-disabled", False)
    splash.destroy()

# Center the tk window
tk.eval('tk::PlaceWindow %s center' % tk.winfo_pathname(tk.winfo_id()))

splash.loading_status = "Loading..."
threading.Thread(target=loading_thread).start()
splash.mainloop()