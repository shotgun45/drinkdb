import unittest
import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from drink_utils import load_drinks

test_json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/drinks.json'))


class TestDrinkDB(unittest.TestCase):

    def test_json_file_is_valid(self):
        # Ensure the JSON file is valid and can be loaded directly
        with open(test_json_path, 'r') as f:
            try:
                data = json.load(f)
            except Exception as e:
                self.fail(f"drinks.json is not valid JSON: {e}")
            self.assertIsInstance(data, list)

    def test_drink_and_ingredient_names_nonempty(self):
        drinks = load_drinks(test_json_path)
        for drink in drinks:
            self.assertTrue(isinstance(drink['name'], str) and drink['name'].strip(), f"Drink has empty or invalid name: {drink}")
            for ing in drink['ingredients']:
                self.assertTrue(isinstance(ing['name'], str) and ing['name'].strip(), f"Ingredient has empty or invalid name: {ing}")

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

    def test_no_duplicate_drink_names(self):
        drinks = load_drinks(test_json_path)
        names = [drink['name'] for drink in drinks]
        self.assertEqual(len(names), len(set(names)), "Duplicate drink names found.")

    def test_no_empty_ingredients(self):
        drinks = load_drinks(test_json_path)
        for drink in drinks:
            self.assertTrue(len(drink['ingredients']) > 0, f"Drink '{drink['name']}' has no ingredients.")
            for ing in drink['ingredients']:
                self.assertTrue(ing['name'].strip(), f"Drink '{drink['name']}' has ingredient with empty name.")
                self.assertTrue(ing['amount'].strip(), f"Drink '{drink['name']}' has ingredient with empty amount.")

    def test_instructions_not_empty(self):
        drinks = load_drinks(test_json_path)
        for drink in drinks:
            self.assertTrue(drink['instructions'].strip(), f"Drink '{drink['name']}' has empty instructions.")


if __name__ == '__main__':
    unittest.main()
