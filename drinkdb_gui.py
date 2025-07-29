import json
import tkinter as tk
from tkinter import ttk, messagebox

# Load drinks data from JSON file
def load_drinks(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def show_drink_details(event):
    selection = drink_listbox.curselection()
    if not selection:
        return
    index = selection[0]
    drink = drinks[index]
    # Ingredients
    ingredients_text = "\n".join([
        f"- {ing['name']}: {ing['amount']}" for ing in drink['ingredients']
    ])
    # Instructions
    instructions_text = drink.get('instructions', 'No instructions provided.')
    # Update text widgets
    ingredients_var.set(ingredients_text)
    instructions_var.set(instructions_text)

# Main window
root = tk.Tk()
root.title("DrinkDB - Drinks and Ingredients")
root.geometry("500x400")

# Load data
try:
    drinks = load_drinks("drinks.json")
except Exception as e:
    messagebox.showerror("Error", f"Failed to load drinks.json: {e}")
    root.destroy()
    exit()

# Drink list
drink_listbox = tk.Listbox(root, height=8, font=("Arial", 12))
for drink in drinks:
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
if drinks:
    drink_listbox.selection_set(0)
    show_drink_details(None)

root.mainloop()
