"""Help screen with keyboard shortcuts and documentation."""

from textual.app import ComposeResult
from textual.containers import Container, Vertical, ScrollableContainer
from textual.widgets import Static, Button, Markdown


HELP_CONTENT = """
# Random Generator Help

## Keyboard Shortcuts

### Navigation
- **↑↓ / hjkl** - Navigate menu items and fields
- **Tab / Shift+Tab** - Move between input fields
- **Enter** - Confirm selection / Generate
- **Esc** - Go back / Cancel
- **Ctrl+C** - Exit application

### Quick Actions
- **F1** - Numbers Generator
- **F2** - Floats Generator
- **F3** - Colors Generator
- **F4** - Strings Generator
- **F5** - Custom Pattern Generator
- **F6** - List Selection
- **Ctrl+H** - Show this help
- **Ctrl+R** - View history

## Generator Types

### Numbers
Generate random integers with exclusions.
- Set minimum and maximum values
- Specify how many numbers to generate
- Optionally exclude specific numbers

### Floats
Generate random decimal numbers with precision control.
- Set minimum and maximum values
- Control decimal places (0-10)
- Generate multiple values

### Colors
Generate random colors in various formats.
- **HEX**: #ff5733
- **RGB**: rgb(255, 87, 51)
- **HSL**: hsl(9, 100%, 60%)

### Strings
Generate random strings with pattern control.
- **Alphanumeric**: Letters and numbers
- **Alpha**: Letters only
- **Numeric**: Numbers only
- **Lowercase**: Lowercase letters
- **Uppercase**: Uppercase letters
- **Hexadecimal**: 0-9, a-f
- **Symbols**: Special characters
- **Alphanumeric + Symbols**: All characters

### Custom Pattern
Use templates for specific formats.

**Template Syntax:**
- `{d}` - Random digit (0-9)
- `{l}` - Random lowercase letter (a-z)
- `{u}` - Random uppercase letter (A-Z)
- `{a}` - Random letter (any case)
- `{x}` - Random hexadecimal (0-9, a-f)
- `{s}` - Random symbol
- `{w}` - Random word character (alphanumeric)

**Examples:**
- License Plate: `{u}{u}{u}-{d}{d}{d}` → ABC-123
- MAC Address: `{x}{x}:{x}{x}:{x}{x}:{x}{x}:{x}{x}:{x}{x}`
- Product Code: `PROD-{l}{l}{l}{d}{d}{d}-{u}{u}`

### List Selection
Select random items from your custom list.
- Enter items (comma or newline separated)
- Choose how many to select
- Option for unique selection (no duplicates)

## Features

### Live Preview
See a preview of your generation parameters before generating.

### History
All generations are automatically saved to history.
- View recent generations on home screen
- Access full history from History menu
- Regenerate previous results

### Copy to Clipboard
Click the "Copy" button to copy results to clipboard.
(Requires pyperclip: `pip install pyperclip`)

### Export
Export results to files (coming soon).

## Tips

1. **Avoid Confusing Characters**: When generating passwords or codes, exclude similar-looking characters:
   - Exclude: `0oO1lI`

2. **Quick Generation**: Use F1-F6 keys to quickly jump to any generator.

3. **Keyboard Navigation**: The entire interface can be navigated with just the keyboard.

4. **History**: Check your history to regenerate or reference previous results.

## Troubleshooting

**Clipboard not working?**
- Install pyperclip: `pip install pyperclip`

**Colors not displaying?**
- Ensure your terminal supports colors
- Try a modern terminal emulator

**Layout issues?**
- Resize your terminal window
- Minimum recommended size: 80x24

## About

Random Value Generator - Enhanced TUI Mode
Built with Textual framework

For more information, visit the GitHub repository.
"""


class HelpScreen(Container):
    """Help screen with documentation."""
    
    DEFAULT_CSS = """
    HelpScreen {
        padding: 2 4;
        height: 100%;
    }
    
    HelpScreen .screen-title {
        text-style: bold;
        color: $primary;
        text-align: center;
        margin-bottom: 2;
    }
    
    HelpScreen ScrollableContainer {
        height: 1fr;
        border: tall $primary;
        background: $surface-darken-1;
        padding: 1;
    }
    
    HelpScreen .button-group {
        layout: horizontal;
        height: auto;
        align: center middle;
        margin-top: 2;
    }
    """
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Static("Help & Documentation", classes="screen-title")
        
        with ScrollableContainer():
            yield Markdown(HELP_CONTENT)
        
        with Container(classes="button-group"):
            yield Button("Close", id="close-btn", variant="primary")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "close-btn":
            # Navigate back to home
            self.app.action_show_screen("home")
