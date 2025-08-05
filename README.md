
# DrinkDB

DrinkDB is a small Python application for storing the recipes of some of the most common and your favorite cocktails.
![main screen](./docs/drinkdbmainMacOS.PNG)

## Installation
As of this time I have confirmed the app will run on MacOS and Linux. Windows testing has only been done in WSL with Ubuntu. I will try running on Windows natively at a later time.

1.) Install Python
```
MacOS

brew install python
```

```
Linux (Debian/Ubuntu)

sudo apt install python3
```

2.) Install Tkinter 
```
MacOS

brew install tcl-tk
```

```
Linux (Debian/Ubuntu)
sudo apt-get install python3-tk (Debian/Ubuntu)
```

3.) Clone repository to your local machine

4.) To execute the application navigate to the drinkdb root directory and execute the following command
```
python3 main.py
```
## Updates
- 2025.08.04 - Move backup actions to its own menu option. Made drink list larger to fill more of the screen.
- 2025.08.03 - Prevent users from entering duplicate cocktail names.
- 2025.08.02 - Added ability to backup and restore the cocktail data file.