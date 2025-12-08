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
try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False


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


class GUI:
    """Graphical User Interface for the generator"""
    
    def __init__(self):
        if not GUI_AVAILABLE:
            print("Error: tkinter not available. GUI mode requires tkinter.")
            sys.exit(1)
            
        self.generator = RandomGenerator()
        self.root = tk.Tk()
        self.root.title("Random Value Generator")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the GUI layout"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Random Value Generator", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Generation Type
        ttk.Label(main_frame, text="Generation Type:", font=('Arial', 10, 'bold')).grid(
            row=1, column=0, sticky=tk.W, pady=5)
        
        self.gen_type = tk.StringVar(value="number")
        gen_types = [
            ("Numbers", "number"),
            ("Floats", "float"),
            ("Colors", "color"),
            ("Strings", "string"),
            ("Custom Pattern", "custom"),
            ("From List", "list")
        ]
        
        type_frame = ttk.Frame(main_frame)
        type_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        for i, (text, value) in enumerate(gen_types):
            ttk.Radiobutton(type_frame, text=text, variable=self.gen_type, 
                           value=value, command=self.on_type_change).grid(
                row=0, column=i, padx=5)
        
        # Options Frame (will change based on type)
        self.options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        self.options_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), 
                               pady=10)
        self.options_frame.columnconfigure(1, weight=1)
        
        # Results Frame
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), 
                          pady=10)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=10, 
                                                      font=('Courier', 10))
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Buttons Frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(buttons_frame, text="Generate", command=self.generate,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Clear Results", 
                  command=self.clear_results).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Copy to Clipboard", 
                  command=self.copy_to_clipboard).pack(side=tk.LEFT, padx=5)
        
        # Initialize with number options
        self.on_type_change()
    
    def clear_options_frame(self):
        """Clear all widgets from options frame"""
        for widget in self.options_frame.winfo_children():
            widget.destroy()
    
    def on_type_change(self):
        """Handle generation type change"""
        self.clear_options_frame()
        gen_type = self.gen_type.get()
        
        if gen_type == "number":
            self.setup_number_options()
        elif gen_type == "float":
            self.setup_float_options()
        elif gen_type == "color":
            self.setup_color_options()
        elif gen_type == "string":
            self.setup_string_options()
        elif gen_type == "custom":
            self.setup_custom_options()
        elif gen_type == "list":
            self.setup_list_options()
    
    def setup_number_options(self):
        """Setup options for number generation"""
        ttk.Label(self.options_frame, text="Min:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.num_min = ttk.Entry(self.options_frame, width=15)
        self.num_min.insert(0, "1")
        self.num_min.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(self.options_frame, text="Max:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.num_max = ttk.Entry(self.options_frame, width=15)
        self.num_max.insert(0, "100")
        self.num_max.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(self.options_frame, text="Count:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.num_count = ttk.Entry(self.options_frame, width=15)
        self.num_count.insert(0, "5")
        self.num_count.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(self.options_frame, text="Exclude (comma-separated):").grid(
            row=3, column=0, sticky=tk.W, pady=5)
        self.num_exclude = ttk.Entry(self.options_frame, width=30)
        self.num_exclude.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
    
    def setup_float_options(self):
        """Setup options for float generation"""
        ttk.Label(self.options_frame, text="Min:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.float_min = ttk.Entry(self.options_frame, width=15)
        self.float_min.insert(0, "0.0")
        self.float_min.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(self.options_frame, text="Max:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.float_max = ttk.Entry(self.options_frame, width=15)
        self.float_max.insert(0, "1.0")
        self.float_max.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(self.options_frame, text="Decimals:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.float_decimals = ttk.Entry(self.options_frame, width=15)
        self.float_decimals.insert(0, "2")
        self.float_decimals.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(self.options_frame, text="Count:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.float_count = ttk.Entry(self.options_frame, width=15)
        self.float_count.insert(0, "5")
        self.float_count.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
    
    def setup_color_options(self):
        """Setup options for color generation"""
        ttk.Label(self.options_frame, text="Format:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.color_format = ttk.Combobox(self.options_frame, values=["hex", "rgb", "hsl"], 
                                         width=13, state="readonly")
        self.color_format.set("hex")
        self.color_format.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(self.options_frame, text="Count:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.color_count = ttk.Entry(self.options_frame, width=15)
        self.color_count.insert(0, "5")
        self.color_count.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
    
    def setup_string_options(self):
        """Setup options for string generation"""
        ttk.Label(self.options_frame, text="Length:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.str_length = ttk.Entry(self.options_frame, width=15)
        self.str_length.insert(0, "10")
        self.str_length.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(self.options_frame, text="Pattern:").grid(row=1, column=0, sticky=tk.W, pady=5)
        patterns = ["alphanumeric", "alpha", "numeric", "lowercase", "uppercase", 
                   "hex", "symbols", "alphanumeric_symbols"]
        self.str_pattern = ttk.Combobox(self.options_frame, values=patterns, 
                                        width=20, state="readonly")
        self.str_pattern.set("alphanumeric")
        self.str_pattern.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(self.options_frame, text="Exclude chars:").grid(
            row=2, column=0, sticky=tk.W, pady=5)
        self.str_exclude = ttk.Entry(self.options_frame, width=30)
        self.str_exclude.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        ttk.Label(self.options_frame, text="Count:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.str_count = ttk.Entry(self.options_frame, width=15)
        self.str_count.insert(0, "5")
        self.str_count.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
    
    def setup_custom_options(self):
        """Setup options for custom pattern generation"""
        ttk.Label(self.options_frame, text="Template:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.custom_template = ttk.Entry(self.options_frame, width=40)
        self.custom_template.insert(0, "{u}{u}{u}-{d}{d}{d}")
        self.custom_template.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        ttk.Label(self.options_frame, text="Count:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.custom_count = ttk.Entry(self.options_frame, width=15)
        self.custom_count.insert(0, "5")
        self.custom_count.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Help text
        help_text = ttk.Label(self.options_frame, 
                             text="{d}=digit {l}=lowercase {u}=uppercase {a}=letter {x}=hex {s}=symbol",
                             font=('Arial', 8), foreground='gray')
        help_text.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
    
    def setup_list_options(self):
        """Setup options for list-based generation"""
        ttk.Label(self.options_frame, text="Items (comma-separated):").grid(
            row=0, column=0, sticky=tk.W, pady=5)
        self.list_items = ttk.Entry(self.options_frame, width=40)
        self.list_items.insert(0, "red,blue,green,yellow,purple")
        self.list_items.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        ttk.Label(self.options_frame, text="Count:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.list_count = ttk.Entry(self.options_frame, width=15)
        self.list_count.insert(0, "3")
        self.list_count.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.list_unique = tk.BooleanVar()
        ttk.Checkbutton(self.options_frame, text="Unique items only", 
                       variable=self.list_unique).grid(row=2, column=0, columnspan=2, 
                                                       sticky=tk.W, pady=5)
    
    def generate(self):
        """Generate values based on current settings"""
        try:
            gen_type = self.gen_type.get()
            results = []
            
            if gen_type == "number":
                min_val = int(self.num_min.get())
                max_val = int(self.num_max.get())
                count = int(self.num_count.get())
                exclude_str = self.num_exclude.get().strip()
                exclude = set()
                if exclude_str:
                    exclude = {int(x.strip()) for x in exclude_str.split(',')}
                results = self.generator.generate_number(min_val, max_val, exclude, count)
            
            elif gen_type == "float":
                min_val = float(self.float_min.get())
                max_val = float(self.float_max.get())
                decimals = int(self.float_decimals.get())
                count = int(self.float_count.get())
                results = self.generator.generate_float(min_val, max_val, decimals, count)
            
            elif gen_type == "color":
                format_type = self.color_format.get()
                count = int(self.color_count.get())
                results = self.generator.generate_color(format_type, count)
            
            elif gen_type == "string":
                length = int(self.str_length.get())
                pattern = self.str_pattern.get()
                exclude_chars = self.str_exclude.get()
                count = int(self.str_count.get())
                results = self.generator.generate_string(length, pattern, exclude_chars, count)
            
            elif gen_type == "custom":
                template = self.custom_template.get()
                count = int(self.custom_count.get())
                results = self.generator.generate_custom(template, count)
            
            elif gen_type == "list":
                items_str = self.list_items.get()
                items = [x.strip() for x in items_str.split(',')]
                count = int(self.list_count.get())
                unique = self.list_unique.get()
                results = self.generator.generate_from_list(items, count, unique)
            
            # Display results
            self.results_text.delete(1.0, tk.END)
            for result in results:
                self.results_text.insert(tk.END, f"{result}\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"Generation failed: {str(e)}")
    
    def clear_results(self):
        """Clear the results text area"""
        self.results_text.delete(1.0, tk.END)
    
    def copy_to_clipboard(self):
        """Copy results to clipboard"""
        results = self.results_text.get(1.0, tk.END).strip()
        if results:
            self.root.clipboard_clear()
            self.root.clipboard_append(results)
            messagebox.showinfo("Success", "Results copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No results to copy!")
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Advanced Random Value Generator')
    parser.add_argument('--mode', choices=['tui', 'gui', 'number', 'float', 'color', 'string', 'custom', 'list'],
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
    
    # GUI mode
    if args.mode == 'gui':
        gui = GUI()
        gui.run()
        return
    
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
