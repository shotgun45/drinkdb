import json
import tkinter as tk
from tkinter import ttk, messagebox

# Load drinks data from JSON file
def load_drinks(filename):
    with open(filename, 'r') as f:
        return json.load(f)


# Main window
root = tk.Tk()
root.title("DrinkDB - Drinks and Ingredients")
root.geometry("1024x768")


# Load data with absolute path
import os
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    drinks_path = os.path.join(script_dir, "drinks.json")
    drinks = load_drinks(drinks_path)
except Exception as e:
    messagebox.showerror("Error", f"Failed to load drinks.json: {e}")
    root.destroy()
    exit()

drink_listbox = tk.Listbox(root, height=8, font=("Arial", 12))


# Alphabetize drinks by name
drinks_sorted = sorted(drinks, key=lambda d: d['name'].lower())

# Ingredients and instructions variables must be defined before the callback
ingredients_var = tk.StringVar()
instructions_var = tk.StringVar()

def show_drink_details(event):
    selection = drink_listbox.curselection()
    if not selection:
        return
    index = selection[0]
    drink = drinks_sorted[index]
    ingredients_text = "\n".join([
        f"- {ing['amount']} {ing['name']}" for ing in drink['ingredients']
    ])
    instructions_text = drink.get('instructions', 'No instructions provided.')
    ingredients_var.set(ingredients_text)
    instructions_var.set(instructions_text)

drink_listbox = tk.Listbox(root, height=8, font=("Arial", 12))
for drink in drinks_sorted:
    drink_listbox.insert(tk.END, drink['name'])
drink_listbox.pack(fill=tk.X, padx=10, pady=10)
drink_listbox.bind('<<ListboxSelect>>', show_drink_details)

# Ingredients label
ingredients_label = ttk.Label(root, text="Ingredients:", font=("Arial", 11, "bold"))
ingredients_label.pack(anchor='w', padx=10)

# Ingredients text
ingredients_var = tk.StringVar()
ingredients_text = ttk.Label(root, textvariable=ingredients_var, font=("Arial", 11), justify='left')
ingredients_text.pack(anchor='w', padx=20, pady=(0,10))

# Instructions label
instructions_label = ttk.Label(root, text="Instructions:", font=("Arial", 11, "bold"))
instructions_label.pack(anchor='w', padx=10)

# Instructions text
instructions_var = tk.StringVar()
instructions_text = ttk.Label(root, textvariable=instructions_var, font=("Arial", 11), wraplength=460, justify='left')
instructions_text.pack(anchor='w', padx=20, pady=(0,10))

# Select first drink by default
if drinks_sorted:
    drink_listbox.selection_set(0)
    show_drink_details(None)

root.mainloop()
