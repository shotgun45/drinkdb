import json

def load_drinks(filename):
    with open(filename, 'r') as f:
        return json.load(f)
