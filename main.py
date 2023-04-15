import os
import tkinter
import tkinter.messagebox
import tkinter.ttk as ttk
import sys
import typing
import time

import tkmacosx
from rich import inspect
from rich.pretty import pprint
from PIL import Image, ImageTk, ImageColor

import splashscreen


def calculate_standard_drink(abv, volume):
    """
    Calculate the number of standard drink in a drink according to the WHO
    """
    return round(abv * volume / 1000, 2)


ALCOHOL_DOSAGE = [
    ("Threshold", "1 standard drink", "#81F7F3"),
    ("Light", "1-3 standard drinks", "#90ee90"),
    ("Common", "3-5 standard drinks", "#ffff00"),
    ("Strong", "5-6 standard drinks", "#ffa500"),
    ("Heavy", "6+ standard drinks", "#ff0000")
]
app_dir = os.path.dirname(__file__)


def is_color_dark(color):
    """
    According to https://stackoverflow.com/a/3943023/10930878
    Check if the color is dark or not
    """
    if isinstance(color, str):
        color = ImageColor.getcolor(color, "RGB")
    r, g, b = color
    r *= 0.299; g *= 0.587; b *= 0.114
    color = (r, g, b)
    return sum(color) < 186
        
class Drunkmeter(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Drunkmeter")
        
        # Configure the rows and columns to be resizable
        for row in range(5):
            self.rowconfigure(row, weight=1)
        for col in range(3):
            self.columnconfigure(col, weight=1)
        
        self.create_theme()
        self.create_variables()
        self.build_ui()
        self.width
    
    def create_theme(self):
        # Style the treevview so it looks like a table with a header with a dark border color
        tv_style = ttk.Style()
        tv_style.theme_use("default")
        tv_style.configure("Treeview", background="golden", foreground="black", rowheight=25,
                           fieldbackground="#ffd000")
        tv_style.map("Treeview", background=[("selected", "blue")])
        tv_style.configure("Treeview.Heading", background="gold", foreground="black",
                           bordercolor="#ffd900", relief="solid", font=("./StayVibes.otf", 10, "bold"))
        tv_style.map("Treeview.Heading", background=[("active", "white")])
        
    
    def create_variables(self):
        self.vol_var = tkinter.StringVar()
        self.abv_var = tkinter.StringVar()
    
    def build_ui(self):
        self.abv_label = tkinter.Label(self, text="ABV (%)")
        self.abv_label.grid(row=0, column=0)

        self.vol_label = tkinter.Label(self, text="Volume (ml)")
        self.vol_label.grid(row=0, column=1, columnspan=1)
        
        self.result_lbl = tkinter.Label(self, text="Resullt")
        self.result_lbl.grid(row=0, column=2, columnspan=1)

        self.abv_entry = ttk.Entry(self, textvariable=self.abv_var)
        self.abv_entry.grid(row=1, column=0)
        self.abv_entry.bind("<Return>", lambda event: self.calculate())

        self.vol_entry = ttk.Entry(self, textvariable=self.vol_var)
        self.vol_entry.grid(row=1, column=1)
        self.vol_entry.bind("<Return>", lambda event: self.calculate())

        self.result_container = tkinter.Label(self, text="")
        self.result_container.grid(row=1, column=2)
        self.result_container.configure(font=("sans-serif", 20, "bold"), borderwidth=2, relief="sunken", padx=10, pady=5)
        
        self.calculate_btn = tkmacosx.Button(self, text="Calculate", command=self.calculate)
        self.calculate_btn.configure(bg="#FFC000", fg="black", activebackground="#ffd558", activeforeground="black",
                                     highlightcolor="#ffd558", relief=tkinter.RAISED, 
                                     )
        self.calculate_btn.grid(row=2, column=0, columnspan=3, ipadx=30, ipady=3, pady=10)

        # Display a grid displaying the alcohol dosage
        self.dosage_label = tkinter.Label(self, text="Alcohol dosage (Standard drinks)")
        self.dosage_label.grid(row=3, column=0, columnspan=3)

        dosage_table = ttk.Treeview(self, show="headings", selectmode="none",
                                    height=5, columns=("strenght", "dosage"),
                                    displaycolumns="#all", padding=(5, 5))
        dosage_table.heading("strenght", text="Strenght")
        dosage_table.heading("dosage", text="Dosage")
        dosage_table.grid(row=4, column=0, columnspan=3, rowspan=2, pady=10)

        for dose, dosage, color in ALCOHOL_DOSAGE:
            is_dark = is_color_dark(color)
            dosage_table.tag_configure(dose, background=color, foreground="white" if is_dark else "black")
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
            standard_drinks = calculate_standard_drink(float(self.abv_var.get()), float(self.vol_var.get()))
            if standard_drinks == 1 or standard_drinks < 1:
                self.result_container.config(bg="#81F7F3", fg="black")
            elif standard_drinks > 1 and standard_drinks <= 3:
                self.result_container.config(bg="#98ee90", fg="#000")
            elif standard_drinks > 3 and standard_drinks <= 5:
                self.result_container.config(bg="#ffff00", fg="#000")
            elif standard_drinks > 5 and standard_drinks <= 6:
                self.result_container.config(bg="#ffa500", fg="#000")
            else:
                self.result_container.config(fg="#ff0000", fg="#000")
            result = f"{standard_drinks} standard drink{standard_drinks > 1 and 's' or ''}"
        except ValueError:
            tkinter.messagebox.showerror("Imvalid sinput", "ABV and volume must be numbers", icon="error", parent=self)
            result = "Invalid input"
            self.result_container.config(fg="#cb0606", bg="white")
        self.result_container.config(text="{}".format(result))
        

if sys.platform == "darwin":
    pass
win = Drunkmeter()
# Place the windows on the center of the screen in a manner that works on all platforms
win.update_idletasks()
win.geometry(f"+{win.winfo_screenwidth() // 2 - win.winfo_width() // 2}+{win.winfo_screenheight() // 2 - win.winfo_height() // 2}")
win.iconphoto(True, ImageTk.PhotoImage(file=os.path.join(app_dir, "icon.png")))

splash = splashscreen.SplashScreen(Image.open(os.path.join(app_dir, "splashscreen.png")), win)
splash.hide_root(hide=True)

def after3s():
    splash.hide_root(hide=False)
    splash.destroy()
    
win.after(3000, after3s)
win.mainloop()