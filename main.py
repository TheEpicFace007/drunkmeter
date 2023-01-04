import tkinter
import tkmacosx
import os


def calculate_avb(abv, volume):
    return round(abv * volume / 1000, 2)

tk = tkinter.Tk()
tk.title("US alcohol units calculator")
tk.iconphoto(True, tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "icon.png")))

# Configuure the rows and columns
for row in range(3):
    tk.rowconfigure(row, weight=1)
for col in range(3):
    tk.columnconfigure(col, weight=1) 

# Setup a menubar
menu = tkinter.Menu(tk)
tk.config(menu=menu)

# Add a file menu
file_menu = tkinter.Menu(menu)
file_menu.add_command(label="Exit", command=tk.destroy)

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
        result = str(calculate_avb(float(abv_var.get()), float(vol_var.get()))) + " units"
    except ValueError:
        result = "Invalid input"
    
    result_label.config(text="Result: {}".format(result))

calculate_btn = tkmacosx.Button(tk, text="Calculate", command=calculate)
calculate_btn.configure(bg="#007AFF", fg="white")
calculate_btn.grid(row=2, column=0, columnspan=3)

tk.mainloop()