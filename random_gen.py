#!/usr/bin/env python3
"""
Advanced Random Value Generator
Generates random values with various patterns and exclusions
"""

import random
import string
import argparse
import sys
from typing import List, Optional, Set
import re


class RandomGenerator:
    """Generate various types of random values"""
    
    def __init__(self):
        self.hex_colors = True
        
    def generate_number(self, min_val: int = 1, max_val: int = 100, 
                       exclude: Optional[Set[int]] = None,
                       count: int = 1) -> List[int]:
        """Generate random numbers with exclusions"""
        exclude = exclude or set()
        available = [x for x in range(min_val, max_val + 1) if x not in exclude]
        
        if len(available) < count:
            raise ValueError(f"Not enough numbers available. Need {count}, have {len(available)}")
        
        return random.sample(available, count)
    
    def generate_float(self, min_val: float = 0.0, max_val: float = 1.0,
                      decimals: int = 2, count: int = 1) -> List[float]:
        """Generate random floating point numbers"""
        return [round(random.uniform(min_val, max_val), decimals) for _ in range(count)]
    
    def generate_color(self, format_type: str = "hex", count: int = 1) -> List[str]:
        """Generate random colors in various formats"""
        colors = []
        for _ in range(count):
            r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            
            if format_type == "hex":
                colors.append(f"#{r:02x}{g:02x}{b:02x}")
            elif format_type == "rgb":
                colors.append(f"rgb({r}, {g}, {b})")
            elif format_type == "hsl":
                h, s, l = self._rgb_to_hsl(r, g, b)
                colors.append(f"hsl({h}, {s}%, {l}%)")
            else:
                colors.append(f"#{r:02x}{g:02x}{b:02x}")
        
        return colors
    
    def _rgb_to_hsl(self, r: int, g: int, b: int) -> tuple:
        """Convert RGB to HSL"""
        r, g, b = r/255, g/255, b/255
        max_c = max(r, g, b)
        min_c = min(r, g, b)
        l = (max_c + min_c) / 2
        
        if max_c == min_c:
            h = s = 0
        else:
            d = max_c - min_c
            s = d / (2 - max_c - min_c) if l > 0.5 else d / (max_c + min_c)
            
            if max_c == r:
                h = (g - b) / d + (6 if g < b else 0)
            elif max_c == g:
                h = (b - r) / d + 2
            else:
                h = (r - g) / d + 4
            h /= 6
        
        return int(h * 360), int(s * 100), int(l * 100)
    
    def generate_string(self, length: int = 10, 
                       pattern: str = "alphanumeric",
                       exclude_chars: str = "",
                       count: int = 1) -> List[str]:
        """Generate random strings with patterns"""
        results = []
        
        # Define character sets
        patterns = {
            "alphanumeric": string.ascii_letters + string.digits,
            "alpha": string.ascii_letters,
            "numeric": string.digits,
            "lowercase": string.ascii_lowercase,
            "uppercase": string.ascii_uppercase,
            "hex": "0123456789abcdef",
            "symbols": string.punctuation,
            "alphanumeric_symbols": string.ascii_letters + string.digits + string.punctuation
        }
        
        charset = patterns.get(pattern, string.ascii_letters + string.digits)
        
        # Remove excluded characters
        if exclude_chars:
            charset = ''.join(c for c in charset if c not in exclude_chars)
        
        if not charset:
            raise ValueError("No characters available after exclusions")
        
        for _ in range(count):
            results.append(''.join(random.choices(charset, k=length)))
        
        return results
    
    def generate_custom(self, template: str, count: int = 1) -> List[str]:
        """
        Generate values based on custom template
        Template syntax:
            {d} - digit (0-9)
            {l} - lowercase letter
            {u} - uppercase letter
            {a} - any letter
            {x} - hexadecimal (0-9a-f)
            {s} - symbol
            {w} - word character (alphanumeric)
        """
        results = []
        replacements = {
            'd': string.digits,
            'l': string.ascii_lowercase,
            'u': string.ascii_uppercase,
            'a': string.ascii_letters,
            'x': '0123456789abcdef',
            's': string.punctuation,
            'w': string.ascii_letters + string.digits
        }
        
        for _ in range(count):
            result = template
            for key, charset in replacements.items():
                pattern = '{' + key + '}'
                while pattern in result:
                    result = result.replace(pattern, random.choice(charset), 1)
            results.append(result)
        
        return results
    
    def generate_from_list(self, items: List[str], count: int = 1, 
                          unique: bool = False) -> List[str]:
        """Generate random items from a list"""
        if unique:
            if count > len(items):
                raise ValueError(f"Cannot select {count} unique items from {len(items)} items")
            return random.sample(items, count)
        return random.choices(items, k=count)


class TUI:
    """Text User Interface for the generator"""
    
    def __init__(self):
        self.generator = RandomGenerator()
        
    def clear_screen(self):
        """Clear terminal screen"""
        print("\n" * 50)
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("    RANDOM VALUE GENERATOR")
        print("="*50)
        print("\n1. Generate Numbers")
        print("2. Generate Floating Point Numbers")
        print("3. Generate Colors")
        print("4. Generate Strings")
        print("5. Generate Custom Pattern")
        print("6. Generate from Custom List")
        print("0. Exit")
        print("\n" + "="*50)
    
    def get_input(self, prompt: str, default: any = None, input_type: type = str):
        """Get user input with default value"""
        if default is not None:
            prompt = f"{prompt} [{default}]: "
        else:
            prompt = f"{prompt}: "
        
        value = input(prompt).strip()
        
        if not value and default is not None:
            return default
        
        if input_type == int:
            return int(value) if value else default
        elif input_type == float:
            return float(value) if value else default
        
        return value
    
    def generate_numbers_ui(self):
        """UI for number generation"""
        print("\n--- Generate Numbers ---")
        min_val = self.get_input("Minimum value", 1, int)
        max_val = self.get_input("Maximum value", 100, int)
        count = self.get_input("How many numbers", 1, int)
        
        exclude_input = self.get_input("Numbers to exclude (comma-separated, or leave empty)", "")
        exclude = set()
        if exclude_input:
            exclude = {int(x.strip()) for x in exclude_input.split(',')}
        
        try:
            results = self.generator.generate_number(min_val, max_val, exclude, count)
            print(f"\nGenerated numbers: {results}")
        except ValueError as e:
            print(f"\nError: {e}")
    
    def generate_floats_ui(self):
        """UI for float generation"""
        print("\n--- Generate Floating Point Numbers ---")
        min_val = self.get_input("Minimum value", 0.0, float)
        max_val = self.get_input("Maximum value", 1.0, float)
        decimals = self.get_input("Decimal places", 2, int)
        count = self.get_input("How many numbers", 1, int)
        
        results = self.generator.generate_float(min_val, max_val, decimals, count)
        print(f"\nGenerated floats: {results}")
    
    def generate_colors_ui(self):
        """UI for color generation"""
        print("\n--- Generate Colors ---")
        print("Formats: hex, rgb, hsl")
        format_type = self.get_input("Color format", "hex")
        count = self.get_input("How many colors", 1, int)
        
        results = self.generator.generate_color(format_type, count)
        print(f"\nGenerated colors:")
        for color in results:
            print(f"  {color}")
    
    def generate_strings_ui(self):
        """UI for string generation"""
        print("\n--- Generate Strings ---")
        print("Patterns: alphanumeric, alpha, numeric, lowercase, uppercase, hex, symbols, alphanumeric_symbols")
        length = self.get_input("String length", 10, int)
        pattern = self.get_input("Pattern", "alphanumeric")
        exclude_chars = self.get_input("Characters to exclude", "")
        count = self.get_input("How many strings", 1, int)
        
        try:
            results = self.generator.generate_string(length, pattern, exclude_chars, count)
            print(f"\nGenerated strings:")
            for s in results:
                print(f"  {s}")
        except ValueError as e:
            print(f"\nError: {e}")
    
    def generate_custom_ui(self):
        """UI for custom pattern generation"""
        print("\n--- Generate Custom Pattern ---")
        print("Template syntax:")
        print("  {d} - digit, {l} - lowercase, {u} - uppercase")
        print("  {a} - any letter, {x} - hex, {s} - symbol, {w} - alphanumeric")
        print("Example: {u}{u}{u}-{d}{d}{d} → ABC-123")
        
        template = self.get_input("Template")
        count = self.get_input("How many", 1, int)
        
        results = self.generator.generate_custom(template, count)
        print(f"\nGenerated values:")
        for value in results:
            print(f"  {value}")
    
    def generate_from_list_ui(self):
        """UI for list-based generation"""
        print("\n--- Generate from Custom List ---")
        items_input = self.get_input("Enter items (comma-separated)")
        items = [x.strip() for x in items_input.split(',')]
        
        count = self.get_input("How many items", 1, int)
        unique_input = self.get_input("Unique items only? (y/n)", "n")
        unique = unique_input.lower() == 'y'
        
        try:
            results = self.generator.generate_from_list(items, count, unique)
            print(f"\nSelected items: {results}")
        except ValueError as e:
            print(f"\nError: {e}")
    
    def run(self):
        """Main TUI loop"""
        while True:
            self.display_menu()
            choice = input("\nSelect option: ").strip()
            
            if choice == '0':
                print("\nGoodbye!")
                break
            elif choice == '1':
                self.generate_numbers_ui()
            elif choice == '2':
                self.generate_floats_ui()
            elif choice == '3':
                self.generate_colors_ui()
            elif choice == '4':
                self.generate_strings_ui()
            elif choice == '5':
                self.generate_custom_ui()
            elif choice == '6':
                self.generate_from_list_ui()
            else:
                print("\nInvalid option!")
            
            input("\nPress Enter to continue...")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Advanced Random Value Generator')
    parser.add_argument('--mode', choices=['tui', 'number', 'float', 'color', 'string', 'custom', 'list'],
                       help='Generation mode')
    
    # Number options
    parser.add_argument('--min', type=float, default=1, help='Minimum value')
    parser.add_argument('--max', type=float, default=100, help='Maximum value')
    parser.add_argument('--exclude', type=str, help='Values to exclude (comma-separated)')
    parser.add_argument('--count', type=int, default=1, help='Number of values to generate')
    
    # Float options
    parser.add_argument('--decimals', type=int, default=2, help='Decimal places for floats')
    
    # Color options
    parser.add_argument('--format', choices=['hex', 'rgb', 'hsl'], default='hex', 
                       help='Color format')
    
    # String options
    parser.add_argument('--length', type=int, default=10, help='String length')
    parser.add_argument('--pattern', 
                       choices=['alphanumeric', 'alpha', 'numeric', 'lowercase', 'uppercase', 
                               'hex', 'symbols', 'alphanumeric_symbols'],
                       default='alphanumeric', help='String pattern')
    parser.add_argument('--exclude-chars', type=str, default='', help='Characters to exclude from string')
    
    # Custom pattern options
    parser.add_argument('--template', type=str, help='Custom template pattern')
    
    # List options
    parser.add_argument('--items', type=str, help='Comma-separated list of items')
    parser.add_argument('--unique', action='store_true', help='Select unique items only')
    
    args = parser.parse_args()
    
    generator = RandomGenerator()
    
    # If no mode specified, start TUI
    if not args.mode or args.mode == 'tui':
        tui = TUI()
        tui.run()
        return
    
    # Command-line mode
    try:
        if args.mode == 'number':
            exclude = set()
            if args.exclude:
                exclude = {int(x.strip()) for x in args.exclude.split(',')}
            results = generator.generate_number(int(args.min), int(args.max), exclude, args.count)
            
        elif args.mode == 'float':
            results = generator.generate_float(args.min, args.max, args.decimals, args.count)
            
        elif args.mode == 'color':
            results = generator.generate_color(args.format, args.count)
            
        elif args.mode == 'string':
            results = generator.generate_string(args.length, args.pattern, args.exclude_chars, args.count)
            
        elif args.mode == 'custom':
            if not args.template:
                print("Error: --template required for custom mode")
                return
            results = generator.generate_custom(args.template, args.count)
            
        elif args.mode == 'list':
            if not args.items:
                print("Error: --items required for list mode")
                return
            items = [x.strip() for x in args.items.split(',')]
            results = generator.generate_from_list(items, args.count, args.unique)
        
        # Print results
        for result in results:
            print(result)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
