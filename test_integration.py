#!/usr/bin/env python3
"""
Test script to verify the Textual TUI integration.
"""

import sys

print("=" * 60)
print("Testing Random Generator Integration")
print("=" * 60)

# Test 1: Check if random_gen.py can be imported
print("\n1. Testing random_gen.py import...")
try:
    import random_gen
    print("   ✓ random_gen.py imports successfully")
except Exception as e:
    print(f"   ✗ Failed to import: {e}")
    sys.exit(1)

# Test 2: Check RandomGenerator class
print("\n2. Testing RandomGenerator class...")
try:
    generator = random_gen.RandomGenerator()
    results = generator.generate_number(1, 10, set(), 3)
    print(f"   ✓ Generated numbers: {results}")
except Exception as e:
    print(f"   ✗ Failed: {e}")
    sys.exit(1)

# Test 3: Check Textual availability
print("\n3. Checking Textual availability...")
try:
    from textual_tui.app import run_textual_tui
    print("   ✓ Textual TUI is available")
    textual_available = True
except ImportError:
    print("   ⚠ Textual TUI not available (install with: pip install textual)")
    textual_available = False

# Test 4: Check classic TUI availability
print("\n4. Checking classic TUI availability...")
try:
    tui = random_gen.TUI()
    print("   ✓ Classic TUI is available")
except Exception as e:
    print(f"   ✗ Failed: {e}")
    sys.exit(1)

# Test 5: Check GUI availability
print("\n5. Checking GUI availability...")
if random_gen.GUI_AVAILABLE:
    print("   ✓ GUI is available")
else:
    print("   ⚠ GUI not available (tkinter not installed)")

# Test 6: Verify textual_tui structure
print("\n6. Checking textual_tui structure...")
try:
    from textual_tui.utils import validation, history_manager, clipboard
    from textual_tui.widgets import navigation, result_display
    from textual_tui.screens import home, number_generator, help
    print("   ✓ All textual_tui modules import successfully")
except ImportError as e:
    print(f"   ⚠ Some modules not available: {e}")

# Summary
print("\n" + "=" * 60)
print("Integration Test Summary")
print("=" * 60)
print(f"✓ Core functionality: Working")
print(f"✓ Classic TUI: Available")
print(f"{'✓' if textual_available else '⚠'} Enhanced TUI: {'Available' if textual_available else 'Not installed'}")
print(f"{'✓' if random_gen.GUI_AVAILABLE else '⚠'} GUI: {'Available' if random_gen.GUI_AVAILABLE else 'Not available'}")

if not textual_available:
    print("\nTo enable enhanced TUI:")
    print("  pip install textual pyperclip")

print("\nHow to run:")
print("  python3 random_gen.py              # Launches TUI (enhanced if available)")
print("  python3 random_gen.py --mode gui   # Launches GUI")
print("  python3 random_gen.py --mode number --min 1 --max 100 --count 5")
print("\n" + "=" * 60)
