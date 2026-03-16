# Enhanced TUI Mode - Installation & Usage Guide

## Overview

The Random Value Generator now features an enhanced Text User Interface (TUI) mode built with the [Textual framework](https://textual.textualize.io/). This provides a modern, visually appealing terminal interface with advanced features.

## Features

### Visual Enhancements
- 🎨 **Modern Color Scheme** - Cyan/blue theme with high contrast
- 📐 **Responsive Layout** - Sidebar navigation with main content area
- ✨ **Visual Feedback** - Notifications and loading indicators
- 🌈 **Color Swatches** - Visual color preview for color generation
- 📏 **Responsive Inputs** - Full-width input fields that adapt to content

### User Experience
- ⌨️ **Full Keyboard Navigation** - Navigate entirely with keyboard
- 🖱️ **Mouse Support** - Click buttons and scroll results
- 🔥 **Keyboard Shortcuts** - F1-F6 for quick access, Ctrl+H for help
- 📋 **Copy to Clipboard** - One-click copy of results
- 📜 **Generation History** - Automatic history tracking
- ❓ **Built-in Help** - Comprehensive documentation within the app

### Functionality
- ✅ **Input Validation** - Validation on generation to prevent errors
- 💾 **History Management** - Automatic tracking of all generations
- 📊 **Result Display** - Comma-separated, formatted results
- 🎲 **Multiple Generators** - Numbers, floats, colors, strings, custom patterns, lists
- 📋 **Clipboard Integration** - One-click copy of results

## Installation

### Option 1: Enhanced TUI (Recommended)

Install the required dependencies:

```bash
pip install -r requirements.txt
```

This installs:
- `textual>=0.50.0` - Modern TUI framework
- `pyperclip>=1.8.2` - Clipboard support (optional)

### Option 2: Classic TUI (No Dependencies)

The app will automatically fall back to the classic TUI if Textual is not installed. No additional dependencies required.

## Usage

### Launch Enhanced TUI

Simply run the script without arguments:

```bash
python3 random_gen.py
```

Or explicitly specify TUI mode:

```bash
python3 random_gen.py --mode tui
```

If Textual is installed, the enhanced TUI will launch automatically. Otherwise, it falls back to the classic TUI.

### Keyboard Shortcuts

#### Navigation
- **↑↓ / hjkl** - Navigate menu items and fields
- **Tab / Shift+Tab** - Move between input fields
- **Enter** - Confirm selection / Generate
- **Esc** - Go back / Cancel
- **Ctrl+Q** - Exit application

#### Quick Access
- **F1** - Numbers Generator
- **F2** - Floats Generator
- **F3** - Colors Generator
- **F4** - Strings Generator
- **F5** - Custom Pattern Generator
- **F6** - List Selection
- **Ctrl+H** - Show Help
- **Ctrl+R** - View History

### Screen Overview

#### Home Screen
- Welcome message
- Quick action cards for common generators
- Recent generation history
- Tips and shortcuts

#### Number Generator
- Min/max value inputs
- Count selector
- Exclusion list (comma-separated)
- Generate button
- Results display with copy/export options

#### Float Generator
- Min/max value inputs
- Decimal places selector (0-10)
- Count selector
- Results display with copy/export options

#### Color Generator
- Format selector (HEX, RGB, HSL)
- Count selector
- Color swatches in results
- Results display with copy/export options

#### String Generator
- Length input
- Pattern selector (8 options: alphanumeric, alpha, numeric, lowercase, uppercase, hex, symbols, alphanumeric+symbols)
- Character exclusion
- Count selector
- Results display with copy/export options

#### Custom Pattern Generator
- Template input with placeholder syntax
- Syntax reference box
- Count selector
- Results display with copy/export options
- Supported placeholders: {d}, {l}, {u}, {a}, {x}, {s}, {w}

#### List Selection
- Multi-line textarea for items (one per line)
- Count selector
- Unique/non-unique selection option
- Scrollable textarea for large lists
- Results display with copy/export options

#### Help Screen
- Complete keyboard shortcuts reference
- Generator type documentation
- Template syntax guide
- Tips and troubleshooting

## Project Structure

```
random-generator/
├── random_gen.py              # Main application
├── requirements.txt           # Python dependencies
├── textual_tui/              # Enhanced TUI implementation
│   ├── __init__.py
│   ├── app.py                # Main Textual app
│   ├── screens/              # Screen components
│   │   ├── __init__.py
│   │   ├── home.py           # Home screen
│   │   ├── number_generator.py  # Number generator screen
│   │   ├── float_generator.py   # Float generator screen
│   │   ├── color_generator.py   # Color generator screen
│   │   ├── string_generator.py  # String generator screen
│   │   ├── custom_generator.py  # Custom pattern generator screen
│   │   ├── list_generator.py    # List selection screen
│   │   └── help.py           # Help screen
│   ├── widgets/              # Reusable widgets
│   │   ├── __init__.py
│   │   ├── navigation.py     # Sidebar navigation
│   │   └── result_display.py # Results display widget
│   ├── styles/               # CSS styling
│   │   └── theme.tcss        # Textual CSS theme
│   └── utils/                # Utility modules
│       ├── __init__.py
│       ├── validation.py     # Input validation
│       ├── history_manager.py # History tracking
│       └── clipboard.py      # Clipboard operations
└── plans/
    └── tui-improvement-plan.md  # Detailed implementation plan
```

## Current Implementation Status

### ✅ Completed
- [x] Project structure and dependencies
- [x] Textual CSS theme with responsive inputs
- [x] Validation utilities
- [x] History manager
- [x] Clipboard support
- [x] Navigation widget
- [x] Result display widget (comma-separated format)
- [x] Home screen with quick actions
- [x] Number generator screen
- [x] Float generator screen
- [x] Color generator screen with color swatches
- [x] String generator screen with 8 pattern options
- [x] Custom pattern generator with template syntax
- [x] List selection screen with scrollable textarea
- [x] Help screen with documentation
- [x] Main Textual app with keyboard shortcuts
- [x] Integration with main script
- [x] Fallback mechanism to classic TUI

### 🚧 Coming Soon
- [ ] History screen with search and filtering
- [ ] Settings screen
- [ ] Export functionality (JSON, CSV, TXT)
- [ ] Additional visual animations

## Development

### Adding New Screens

1. Create a new screen file in `textual_tui/screens/`:

```python
from textual.containers import Container
from textual.widgets import Static

class MyNewScreen(Container):
    def compose(self):
        yield Static("My New Screen")
```

2. Import and register in `textual_tui/app.py`:

```python
from textual_tui.screens.my_new_screen import MyNewScreen

# In action_show_screen method:
elif screen_id == "mynew":
    content_container.mount(MyNewScreen())
```

3. Add navigation button in `textual_tui/widgets/navigation.py`

### Customizing Styles

Edit `textual_tui/styles/theme.tcss` to customize colors, layouts, and styling:

```css
Button {
    background: $primary;
    color: $text;
}

Button:hover {
    background: $primary-lighten-1;
}
```

## Troubleshooting

### Textual Not Found

If you see "Enhanced TUI mode available with 'pip install textual'":

```bash
pip install textual
```

### Clipboard Not Working

Install pyperclip for clipboard support:

```bash
pip install pyperclip
```

### Colors Not Displaying

Ensure your terminal supports colors:
- Use a modern terminal emulator (iTerm2, Windows Terminal, GNOME Terminal)
- Check terminal color settings
- Try setting `TERM=xterm-256color`

### Layout Issues

- Minimum recommended terminal size: 80x24
- Resize your terminal window
- Try maximizing the terminal

### Import Errors

If you get import errors, ensure you're running from the project root:

```bash
cd /path/to/random-generator
python3 random_gen.py
```

## Testing

### Manual Testing

1. Launch the enhanced TUI:
   ```bash
   python3 random_gen.py
   ```

2. Test navigation:
   - Use arrow keys to navigate menu
   - Press F1 to jump to Numbers generator
   - Press Ctrl+H to view help

3. Test number generation:
   - Enter min: 1, max: 100, count: 5
   - Click Generate or press Enter
   - Verify results display
   - Click Copy to test clipboard

4. Test keyboard shortcuts:
   - Press F1-F6 to switch screens
   - Press Ctrl+Q to exit

### Testing Fallback

To test the fallback to classic TUI:

```bash
# Temporarily rename textual_tui directory
mv textual_tui textual_tui_backup

# Run the app
python3 random_gen.py

# Should see: "Using classic TUI mode"

# Restore
mv textual_tui_backup textual_tui
```

## Performance

The enhanced TUI is optimized for performance:
- Lazy loading of screens
- Efficient rendering with Textual's reactive system
- Minimal memory footprint
- Fast startup time

## Contributing

To contribute to the enhanced TUI:

1. Follow the architecture in `plans/tui-improvement-plan.md`
2. Use the existing screen templates as examples
3. Follow Textual best practices
4. Test on multiple terminal emulators
5. Update this README with new features

## Resources

- [Textual Documentation](https://textual.textualize.io/)
- [Textual GitHub](https://github.com/Textualize/textual)
- [Project Plan](plans/tui-improvement-plan.md)
- [Main README](README.md)

## License

Same as the main project (see LICENSE file).

## Support

For issues or questions:
1. Check the Help screen (Ctrl+H in the app)
2. Review the troubleshooting section above
3. Check the main README.md
4. Open an issue on GitHub
