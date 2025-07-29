import unittest
import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from drinkdb_gui import load_drinks

test_json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/drinks.json'))

class TestDrinkDB(unittest.TestCase):
    def test_load_drinks_returns_list(self):
        drinks = load_drinks(test_json_path)
        self.assertIsInstance(drinks, list)

    def test_drink_structure(self):
        drinks = load_drinks(test_json_path)
        for drink in drinks:
            self.assertIn('name', drink)
            self.assertIn('ingredients', drink)
            self.assertIn('instructions', drink)
            self.assertIsInstance(drink['ingredients'], list)
            for ing in drink['ingredients']:
                self.assertIn('name', ing)
                self.assertIn('amount', ing)

    def test_drink_names(self):
        drinks = load_drinks(test_json_path)
        names = [drink['name'] for drink in drinks]
        self.assertIn('Mojito', names)
        self.assertIn('Margarita', names)
        self.assertIn('Old Fashioned', names)
        self.assertIn('Cosmopolitan', names)

if __name__ == '__main__':
    unittest.main()
