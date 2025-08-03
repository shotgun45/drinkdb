
import json
import tkinter as tk
from tkinter import ttk, messagebox
from drink_utils import load_drinks

# Main window
root = tk.Tk()
root.title("DrinkDB")
root.geometry("1024x768")

# Load drinks.json
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
ingredients_text.pack(anchor='w', padx=20, pady=(0, 10))

# Instructions label
instructions_label = ttk.Label(root, text="Instructions:", font=("Arial", 11, "bold"))
instructions_label.pack(anchor='w', padx=10)

# Instructions text
instructions_var = tk.StringVar()
instructions_text = ttk.Label(root, textvariable=instructions_var, font=("Arial", 11), justify='left')
instructions_text.pack(anchor='w', padx=20, pady=(0, 10))

# Select first drink by default
if drinks_sorted:
    drink_listbox.selection_set(0)
    show_drink_details(None)


# --- Add Drink Functionality ---

def open_add_drink_window():
    open_drink_form_window("Add New Drink")


def open_edit_drink_window():
    selection = drink_listbox.curselection()
    if not selection:
        messagebox.showwarning("No selection", "Please select a drink to edit.")
        return
    index = selection[0]
    drink = drinks_sorted[index]
    open_drink_form_window("Edit Drink", drink, index)


def open_drink_form_window(title, drink=None, edit_index=None):
    form_win = tk.Toplevel(root)
    form_win.title(title)
    form_win.geometry("400x500")

    # Drink name
    tk.Label(form_win, text="Drink Name:").pack(anchor='w', padx=10, pady=(10, 0))
    name_entry = tk.Entry(form_win, width=40)
    name_entry.pack(padx=10, pady=2)
    if drink:
        name_entry.insert(0, drink['name'])

    # Ingredients
    tk.Label(form_win, text="Ingredients (one per line, format: amount ingredient):").pack(anchor='w', padx=10, pady=(10, 0))
    ingredients_text = tk.Text(form_win, width=40, height=8)
    ingredients_text.pack(padx=10, pady=2)
    if drink:
        ingredients_lines = [f"{ing['amount']} {ing['name']}" for ing in drink['ingredients']]
        ingredients_text.insert("1.0", "\n".join(ingredients_lines))

    # Instructions
    tk.Label(form_win, text="Instructions:").pack(anchor='w', padx=10, pady=(10, 0))
    instructions_entry = tk.Text(form_win, width=40, height=4, wrap="word")
    instructions_entry.pack(padx=10, pady=2)
    if drink:
        instructions_entry.insert("1.0", drink['instructions'])

    def save_drink():
        global drinks_sorted
        name = name_entry.get().strip()
        instructions = instructions_entry.get("1.0", tk.END).strip()
        ingredients_lines = ingredients_text.get("1.0", tk.END).strip().splitlines()
        if not name or not ingredients_lines:
            messagebox.showerror("Error", "Drink name and at least one ingredient are required.")
            return
        # Prevent duplicate names
        lower_name = name.lower()
        existing_names = [d['name'].lower() for d in drinks]
        if edit_index is not None:
            orig_name = drinks_sorted[edit_index]['name']
            orig_name_lower = orig_name.lower()
            # Remove the original name from the list for edit
            filtered_names = [n for n in existing_names if n != orig_name_lower]
            if lower_name in filtered_names:
                messagebox.showerror("Error", f"A drink named '{name}' already exists.")
                return
        else:
            if lower_name in existing_names:
                messagebox.showerror("Error", f"A drink named '{name}' already exists.")
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
        if edit_index is not None:
            # Find the original drink in the unsorted list and update it
            orig_name = drinks_sorted[edit_index]['name']
            for i, d in enumerate(drinks):
                if d['name'] == orig_name:
                    drinks[i] = {"name": name, "ingredients": ingredients, "instructions": instructions}
                    break
        else:
            # Add new drink
            drinks.append({"name": name, "ingredients": ingredients, "instructions": instructions})
        # Re-sort and update display
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
        form_win.destroy()

    btn_frame = tk.Frame(form_win)
    btn_frame.pack(pady=20)
    tk.Button(btn_frame, text="Save", command=save_drink).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Cancel", command=form_win.destroy).pack(side=tk.LEFT, padx=10)


def delete_selected_drink():
    global drinks_sorted
    selection = drink_listbox.curselection()
    if not selection:
        messagebox.showwarning("No selection", "Please select a drink to delete.")
        return
    index = selection[0]
    drink_to_delete = drinks_sorted[index]
    confirm = messagebox.askyesno("Delete Drink", f"Are you sure you want to delete '{drink_to_delete['name']}'?")
    if not confirm:
        return
    # Remove from drinks and update sorted list
    drinks.remove(next(d for d in drinks if d['name'] == drink_to_delete['name']))
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
    # Clear details if nothing is selected
    if not drinks_sorted:
        ingredients_var.set("")
        instructions_var.set("")
    else:
        drink_listbox.selection_set(0)
        show_drink_details(None)



# Toolbar with Backup button

def backup_json():
    import shutil
    import datetime
    backup_dir = os.path.join(script_dir, "backups")
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"drinks_backup_{timestamp}.json")
    try:
        shutil.copy2(drinks_path, backup_path)
        messagebox.showinfo("Backup Successful", f"Backup created at:\n{backup_path}")
    except Exception as e:
        messagebox.showerror("Backup Failed", f"Could not backup drinks.json: {e}")

def restore_from_backup():
    import shutil
    from tkinter import filedialog
    backup_dir = os.path.join(script_dir, "backups")
    if not os.path.exists(backup_dir):
        messagebox.showerror("Restore Failed", "No backups directory found.")
        return
    filetypes = [("JSON Files", "*.json")]
    backup_file = filedialog.askopenfilename(
        title="Select Backup File",
        initialdir=backup_dir,
        filetypes=filetypes
    )
    if not backup_file:
        return
    try:
        shutil.copy2(backup_file, drinks_path)
        messagebox.showinfo("Restore Successful", f"Restored from backup:\n{backup_file}\n\nPlease restart the app to see changes.")
    except Exception as e:
        messagebox.showerror("Restore Failed", f"Could not restore drinks.json: {e}")


# Menu
menubar = tk.Menu(root)
drinks_menu = tk.Menu(menubar, tearoff=0)
drinks_menu.add_command(label="Add Drink", command=open_add_drink_window)
drinks_menu.add_command(label="Edit Drink", command=open_edit_drink_window)
drinks_menu.add_command(label="Delete Drink", command=delete_selected_drink)
drinks_menu.add_separator()
drinks_menu.add_command(label="Backup JSON", command=backup_json)
drinks_menu.add_command(label="Restore from Backup", command=restore_from_backup)
menubar.add_cascade(label="Edit", menu=drinks_menu)
root.config(menu=menubar)

root.mainloop()
