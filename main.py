import tkinter
import tkmacosx
import os
import tkinter.messagebox

def calculate_avb(abv, volume):
    return round(abv * volume / 1000, 2)

tk = tkinter.Tk()
tk.title("Drunkmeter")
tk.iconphoto(True, tkinter.PhotoImage(file=os.path.join(os.path.dirname(__file__), "icon.png")))

for row in range(5):
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
        if float(abv_var.get()) >= 100:
            tkinter.messagebox.showerror("Error", "ABV must be less than or equal to 100%")
            return
        elif float(abv_var.get()) <= 0:
            tkinter.messagebox.showerror("Error", "ABV must be greater than 0%")
        
        if float(vol_var.get()) <= 0:
            tkinter.messagebox.showerror("Error", "Volume must be greater than 0")
            return  
        result = str(calculate_avb(float(abv_var.get()), float(vol_var.get()))) + " units"
    except ValueError:
        result = "Invalid input"
    
    result_label.config(text="Result: {}".format(result))

calculate_btn = tkmacosx.Button(tk, text="Calculate", command=calculate)
calculate_btn.configure(bg="#FFC000", fg="black", activebackground="#FF5733", activeforeground="black")
calculate_btn.grid(row=2, column=0, columnspan=3)

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


tk.mainloop()