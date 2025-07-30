import subprocess
import sys
import os


def launch_gui():
    gui_path = os.path.join(os.path.dirname(__file__), 'src', 'drinkdb_gui.py')
    subprocess.run([sys.executable, gui_path])


if __name__ == "__main__":
    launch_gui()
