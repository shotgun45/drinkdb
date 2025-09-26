import unittest
import os
import sys
import json
import logging
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from drink_utils import load_drinks

test_json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/drinks.json'))

# Configure logging for test output
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestDrinkDB(unittest.TestCase):

    def test_json_file_is_valid(self):
        """Test JSON file validity with detailed success reporting."""
        import sys
        
        # Ensure output goes to stdout for pytest capture
        sys.stdout.write("🧪 Testing JSON file validity...\n")
        sys.stdout.flush()
        
        with open(test_json_path, 'r') as f:
            try:
                data = json.load(f)
                sys.stdout.write(f"✓ JSON file loaded successfully with {len(data)} entries\n")
                sys.stdout.flush()
            except Exception as e:
                sys.stderr.write(f"❌ JSON file is invalid: {e}\n")
                sys.stderr.flush()
                self.fail(f"drinks.json is not valid JSON: {e}")
            
            self.assertIsInstance(data, list)
            sys.stdout.write("✓ JSON data is a valid list structure\n")
            sys.stdout.write(f"SUCCESS: JSON validation passed - found {len(data)} drink records\n")
            sys.stdout.flush()

    def test_drink_and_ingredient_names_nonempty(self):
        drinks = load_drinks(test_json_path)
        
        valid_drinks = 0
        valid_ingredients = 0
        
        # Use pytest's extra for better HTML reporting
        extra_info = []
        extra_info.append(f"Testing {len(drinks)} drinks for valid names")
        
        for drink in drinks:
            self.assertTrue(
                isinstance(drink['name'], str) and drink['name'].strip(),
                f"Drink has empty or invalid name: {drink}"
            )
            valid_drinks += 1
            extra_info.append(f"✓ Drink '{drink['name']}' has valid name")
            
            for ing in drink['ingredients']:
                self.assertTrue(
                    isinstance(ing['name'], str) and ing['name'].strip(),
                    f"Ingredient has empty or invalid name: {ing}"
                )
                valid_ingredients += 1
        
        # Add success summary to pytest extra
        extra_info.append(f"✓ All {valid_drinks} drinks have valid names")
        extra_info.append(f"✓ All {valid_ingredients} ingredients have valid names")
        extra_info.append("✓ Test completed successfully!")
        
        # This will appear in the HTML report
        if hasattr(pytest, 'current_request') and hasattr(pytest.current_request.node, 'user_properties'):
            for info in extra_info:
                pytest.current_request.node.user_properties.append(("test_info", info))
        
        # Also use logging which sometimes works better
        for info in extra_info:
            logger.info(info)
            print(info)  # This should definitely show up with -s flag

    def test_load_drinks_returns_list(self):
        """Test that load_drinks function returns a list with detailed reporting."""
        drinks = load_drinks(test_json_path)
        self.assertIsInstance(drinks, list)
        
        # Add detailed success reporting
        print(f"SUCCESS: load_drinks() returned a list with {len(drinks)} items")
        print("✓ Function behavior validated")
        
        # You can also use pytest's built-in extra reporting
        if hasattr(self, '_testMethodDoc'):
            print(f"Test purpose: {self._testMethodDoc}")

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

    def test_no_duplicate_drink_names(self):
        drinks = load_drinks(test_json_path)
        names = [drink['name'] for drink in drinks]
        self.assertEqual(len(names), len(set(names)), "Duplicate drink names found.")

    def test_no_empty_ingredients(self):
        drinks = load_drinks(test_json_path)
        for drink in drinks:
            self.assertTrue(
                len(drink['ingredients']) > 0,
                f"Drink '{drink['name']}' has no ingredients."
            )
            for ing in drink['ingredients']:
                self.assertTrue(
                    ing['name'].strip(),
                    f"Drink '{drink['name']}' has ingredient with empty name."
                )
                self.assertTrue(
                    ing['amount'].strip(),
                    f"Drink '{drink['name']}' has ingredient with empty amount."
                )

    def test_instructions_not_empty(self):
        drinks = load_drinks(test_json_path)
        for drink in drinks:
            self.assertTrue(drink['instructions'].strip(), f"Drink '{drink['name']}' has empty instructions.")

    def test_no_case_insensitive_duplicate_names(self):
        drinks = load_drinks(test_json_path)
        names = [drink['name'].lower() for drink in drinks]
        self.assertEqual(len(names), len(set(names)), "Case-insensitive duplicate drink names found.")

    def test_ingredient_amounts_nonempty(self):
        drinks = load_drinks(test_json_path)
        for drink in drinks:
            for ing in drink['ingredients']:
                self.assertTrue(
                    isinstance(ing['amount'], str) and ing['amount'].strip(),
                    f"Ingredient in '{drink['name']}' has empty or invalid amount: {ing}"
                )

    def test_instructions_minimum_length(self):
        drinks = load_drinks(test_json_path)
        for drink in drinks:
            self.assertGreaterEqual(
                len(drink['instructions'].strip()),
                5,
                f"Instructions for '{drink['name']}' are too short."
            )

    def test_filter_allows_only_extended_ascii(self):
        def is_extended_ascii(s):
            return all(0 <= ord(c) <= 255 for c in s)

        valid_ascii = ''.join(chr(i) for i in range(256))
        self.assertTrue(is_extended_ascii(valid_ascii), "Filter should allow all extended ASCII (0-255)")

        invalid = 'hello\u20ac'  # Euro sign is 8364
        self.assertFalse(is_extended_ascii(invalid), "Filter should not allow non-ASCII (>255) characters")

    def test_intentional_failure_for_demo(self):
        """This test is designed to fail for demonstration purposes."""
        drinks = load_drinks(test_json_path)
        # Intentionally failing assertion to show how failures appear in HTML report
        self.assertEqual(len(drinks), 999, "This test is intentionally designed to fail - expected 999 drinks but found fewer")
        
    def test_another_failing_test(self):
        """Another failing test to show multiple failures in the report."""
        self.assertTrue(False, "This assertion will always fail - demonstrating test failure reporting")


if __name__ == '__main__':
    unittest.main()
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
