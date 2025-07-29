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


# --- Add Drink Functionality ---
def open_add_drink_window():
    add_win = tk.Toplevel(root)
    add_win.title("Add New Drink")
    add_win.geometry("400x500")

    # Drink name
    tk.Label(add_win, text="Drink Name:").pack(anchor='w', padx=10, pady=(10,0))
    name_entry = tk.Entry(add_win, width=40)
    name_entry.pack(padx=10, pady=2)

    # Instructions
    tk.Label(add_win, text="Instructions:").pack(anchor='w', padx=10, pady=(10,0))
    instructions_entry = tk.Text(add_win, width=40, height=4)
    instructions_entry.pack(padx=10, pady=2)

    # Ingredients
    tk.Label(add_win, text="Ingredients (one per line, format: amount ingredient):").pack(anchor='w', padx=10, pady=(10,0))
    ingredients_text = tk.Text(add_win, width=40, height=8)
    ingredients_text.pack(padx=10, pady=2)

    def add_drink():
        name = name_entry.get().strip()
        instructions = instructions_entry.get("1.0", tk.END).strip()
        ingredients_lines = ingredients_text.get("1.0", tk.END).strip().splitlines()
        if not name or not ingredients_lines:
            messagebox.showerror("Error", "Drink name and at least one ingredient are required.")
            return
        # Parse ingredients
        ingredients = []
        for line in ingredients_lines:
            if not line.strip():
                continue
            parts = line.strip().split(' ', 1)
            if len(parts) != 2:
                messagebox.showerror("Error", f"Invalid ingredient format: '{line}'. Use: amount ingredient")
                return
            amount, ing_name = parts
            ingredients.append({"name": ing_name, "amount": amount})
        # Add to drinks list
        new_drink = {"name": name, "ingredients": ingredients, "instructions": instructions}
        drinks.append(new_drink)
        # Re-sort and update display
        global drinks_sorted
        drinks_sorted = sorted(drinks, key=lambda d: d['name'].lower())
        drink_listbox.delete(0, tk.END)
        for drink in drinks_sorted:
            drink_listbox.insert(tk.END, drink['name'])
        # Save to JSON
        try:
            with open(drinks_path, 'w') as f:
                json.dump(drinks, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save to drinks.json: {e}")
        add_win.destroy()

    btn_frame = tk.Frame(add_win)
    btn_frame.pack(pady=20)
    tk.Button(btn_frame, text="Add Drink", command=add_drink).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Cancel", command=add_win.destroy).pack(side=tk.LEFT, padx=10)

# Add button to main window
add_btn = ttk.Button(root, text="Add Drink", command=open_add_drink_window)
add_btn.pack(pady=10)

root.mainloop()
