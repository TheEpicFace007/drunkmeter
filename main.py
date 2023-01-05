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
from mttkinter import mtTkinter
from PIL import Image, ImageTk

import splashscreen
import standardDrinks

THEME = "Clearlooks"
ALCOHOL_DOSAGE = [
    ("Threshold", "1 standard drink", "#81f8f3"),
    ("Light", "1-3 standard drinks", "#90ed91"),
    ("Common", "3-5 standard drinks", "#ffff00"),
    ("Strong", "5-6 standard drinks", "#ffff00"),
    ("Heavy", "6+ standard drinks", "#ff0000")
]
app_dir = os.path.dirname(__file__)


class Drunkmeter(ttkthemes.ThemedTk, mtTkinter.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Drunkmeter")
        # Configure the rows and columns to be resizable
        for row in range(5):
            self.rowconfigure(row, weight=1)
        for col in range(3):
            self.columnconfigure(col, weight=1)
        
        self.create_variables()
        self.build_ui()
    
    
    def create_variables(self):
        self.vol_var = tkinter.StringVar()
        self.abv_var = tkinter.StringVar()
    
    def build_ui(self):
        self.abv_label = tkinter.Label(self, text="ABV (%)")
        self.abv_label.grid(row=0, column=0)

        self.vol_label = tkinter.Label(self, text="Volume (ml)")
        self.vol_label.grid(row=0, column=1, columnspan=1)
        
        tkinter.Label(self, text="Resullt").grid(row=0, column=2, columnspan=1)

        self.abv_entry = tkinter.Entry(self, textvariable=self.abv_var)
        self.abv_entry.grid(row=1, column=0)

        vol_entry = tkinter.Entry(self, textvariable=self.vol_var)
        vol_entry.grid(row=1, column=1)

        self.result_label = tkinter.Label(self, text="")
        self.result_label.grid(row=1, column=2)
        
        self.calculate_btn = tkmacosx.Button(self, text="Calculate", command=self.calculate)
        self.calculate_btn.configure(bg="#FFC000", fg="black",
                                activebackground="#ffd558", activeforeground="black")
        self.calculate_btn.grid(row=2, column=0, columnspan=3, padx=10)

        # Display a grid displaying the alcohol dosage according to psychonautwiki
        self.dosage_label = tkinter.Label(self, text="Alcohol dosage (Standard drinks)")
        self.dosage_label.grid(row=3, column=0, columnspan=3)

        dosage_table = ttk.Treeview(self, show="headings", selectmode="none",
                                    height=5, columns=("strenght", "dosage"),
                                    displaycolumns="#all")
        dosage_table.heading("strenght", text="Strenght")
        dosage_table.heading("dosage", text="Dosage")
        dosage_table.grid(row=4, column=0, columnspan=3, rowspan=2)

        for dose, dosage, color in ALCOHOL_DOSAGE:
            # Unpack the hex color into a tuple of 3 integers
            is_color_dark = splashscreen.is_color_dark(color)
            dosage_table.tag_configure(dose, background=color, foreground="white" if is_color_dark else "black")
            dosage_table.insert('', index="end", values=[dose, dosage], tags=(dose))

    def calculate(self):
        try:
            if float(self.abv_var.get()) >= 100:
                tkinter.messagebox.showerror(
                    "Error", "ABV must be less than 100%", icon="error", parent=self)
                return
            elif float(self.abv_var.get()) <= 0:
                tkinter.messagebox.showerror(
                    "Error", "ABV must be greater than 0%", icon="error", parent=self)
                return
            elif float(self.vol_var.get()) <= 0:
                tkinter.messagebox.showerror(
                    "Error", "Volume must be greater than 0", icon="error", parent=self)
                return
            standard_drinks = standardDrinks.calculate_standard_drink(float(self.abv_var.get()), float(self.vol_var.get()))
            standard_drinks = round(standard_drinks, 2)
            result = f"{standard_drinks} standard drink{standard_drinks > 1 and 's' or ''}"
        except ValueError as e:
            # tkinter.messagebox.showerror("Error", str(e), icon="error", parent=tk)
            result = "Invalid input"

        self.result_label.config(text="{}".format(result))
win = Drunkmeter(theme=THEME)
win.eval('tk::PlaceWindow %s center' % win.winfo_pathname(win.winfo_id()))

win.withdraw()
splash = splashscreen.SplashScreen(Image.open(os.path.join(app_dir, "splashscreen.png")), win)
splash.focus()
def after_splash():
    splash.destroy()
    win.deiconify()
    win.focus()
    win.iconphoto(True, ImageTk.PhotoImage(Image.open(os.path.join(app_dir, "icon.png"))))
splash.after(3000, after_splash)
    


win.mainloop()