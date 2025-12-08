# Random Value Generator

A powerful and flexible Python script for generating random values with extensive customization options. Generate numbers, colors, strings, or custom patterns through an interactive TUI, graphical GUI, or command-line interface.

## Features

- 🎲 **Multiple Generation Types**: Numbers, floats, colors, strings, custom patterns, and list selection
- 🖥️ **Triple Interface**: Graphical GUI, interactive TUI, or direct command-line usage
- 🚫 **Exclusion Support**: Exclude specific values or characters
- 🎨 **Color Formats**: HEX, RGB, and HSL color generation
- 📝 **Custom Templates**: Create your own patterns with template syntax
- 🔢 **Range Control**: Full control over min/max values and counts
- ✨ **Pattern Presets**: Built-in patterns for common use cases
- 📋 **Copy to Clipboard**: Easy copying of results (GUI mode)

## Installation

### Requirements

- Python 3.6 or higher
- No external dependencies required (uses only standard library)
- **For GUI mode**: tkinter (usually pre-installed with Python)
  - **Linux users**: May need to install separately:
    ```bash
    # Debian/Ubuntu
    sudo apt-get install python3-tk
    
    # Fedora
    sudo dnf install python3-tkinter
    
    # Arch Linux
    sudo pacman -S tk
    ```
  - **Windows/Mac**: tkinter is included by default with Python

### Setup

1. Clone the repository:
```bash
git clone https://github.com/CookieShualon/random-generator.git
cd random-generator
```

2. Make it executable (Linux/Mac):
```bash
chmod +x random_gen.py
```

3. Run it:
```bash
python3 random_gen.py
```

## Usage

### GUI Mode (Graphical Interface)

Launch the graphical user interface for an intuitive point-and-click experience:

```bash
python3 random_gen.py --mode gui
```

**GUI Features:**
- 🎯 **Easy Selection**: Radio buttons for generation types
- 📊 **Visual Results**: Scrollable results area
- 📋 **One-Click Copy**: Copy all results to clipboard
- 🧹 **Quick Clear**: Clear results with a button
- 🎨 **Dynamic Forms**: Options change based on selection
- 💡 **Built-in Help**: Template syntax hints

**Perfect for:**
- Quick generation tasks
- Testing different parameters
- Users who prefer graphical interfaces
- Visual preview of results

### Interactive TUI Mode

Launch the interactive menu by running without arguments:

```bash
python3 random_gen.py
```

or explicitly:

```bash
python3 random_gen.py --mode tui
```

The TUI provides a user-friendly menu to guide you through all generation options.

**Perfect for:**
- Terminal-only environments
- Quick interactive sessions
- Learning the tool's capabilities

### Command-Line Mode

Generate values directly from the command line for scripting and automation.

**Perfect for:**
- Automation and scripting
- CI/CD pipelines
- Batch processing
- Integration with other tools

#### Generate Numbers

```bash
# Basic number generation
python3 random_gen.py --mode number --min 1 --max 100 --count 5

# With exclusions
python3 random_gen.py --mode number --min 1 --max 50 --count 10 --exclude "13,7,42"

# Single random number
python3 random_gen.py --mode number --min 1 --max 1000
```

**Output example:**
```
42
17
89
3
56
```

#### Generate Floating Point Numbers

```bash
# Basic float generation
python3 random_gen.py --mode float --min 0.0 --max 1.0 --count 3

# With custom precision
python3 random_gen.py --mode float --min 10.0 --max 50.0 --decimals 4 --count 5
```

**Output example:**
```
0.7234
0.1892
0.9456
```

#### Generate Colors

```bash
# Hexadecimal colors
python3 random_gen.py --mode color --format hex --count 5

# RGB colors
python3 random_gen.py --mode color --format rgb --count 3

# HSL colors
python3 random_gen.py --mode color --format hsl --count 3
```

**Output example:**
```
#ff5733
#33c4ff
#8e44ad
```

#### Generate Strings

```bash
# Alphanumeric string
python3 random_gen.py --mode string --length 12 --pattern alphanumeric --count 3

# Uppercase only
python3 random_gen.py --mode string --length 8 --pattern uppercase --count 5

# With character exclusions (avoiding confusing characters)
python3 random_gen.py --mode string --length 16 --pattern alphanumeric --exclude-chars "0oO1lI" --count 1

# Hexadecimal string
python3 random_gen.py --mode string --length 32 --pattern hex --count 1
```

**Available patterns:**
- `alphanumeric` - Letters and numbers
- `alpha` - Letters only
- `numeric` - Numbers only
- `lowercase` - Lowercase letters only
- `uppercase` - Uppercase letters only
- `hex` - Hexadecimal characters (0-9, a-f)
- `symbols` - Special characters/symbols
- `alphanumeric_symbols` - Letters, numbers, and symbols

**Output example:**
```
aB3xK9mP2nQ5
```

#### Generate Custom Patterns

Create custom patterns using template syntax:

```bash
# License plate format (ABC-123)
python3 random_gen.py --mode custom --template "{u}{u}{u}-{d}{d}{d}" --count 5

# Product code (PROD-abc123-XY)
python3 random_gen.py --mode custom --template "PROD-{l}{l}{l}{d}{d}{d}-{u}{u}" --count 3

# MAC address format
python3 random_gen.py --mode custom --template "{x}{x}:{x}{x}:{x}{x}:{x}{x}:{x}{x}:{x}{x}" --count 1

# Password-like (8 chars with variety)
python3 random_gen.py --mode custom --template "{u}{l}{l}{d}{d}{s}{w}{w}" --count 10
```

**Template syntax:**
- `{d}` - Random digit (0-9)
- `{l}` - Random lowercase letter (a-z)
- `{u}` - Random uppercase letter (A-Z)
- `{a}` - Random letter (any case)
- `{x}` - Random hexadecimal character (0-9, a-f)
- `{s}` - Random symbol/special character
- `{w}` - Random word character (alphanumeric)

**Output example:**
```
XYZ-789
ABC-123
DEF-456
```

#### Generate from Custom List

Select random items from your own list:

```bash
# Random selection (with duplicates possible)
python3 random_gen.py --mode list --items "red,blue,green,yellow,purple" --count 3

# Unique selection (no duplicates)
python3 random_gen.py --mode list --items "Alice,Bob,Charlie,David,Eve" --count 2 --unique

# Random choice from options
python3 random_gen.py --mode list --items "yes,no,maybe" --count 1
```

**Output example:**
```
blue
red
green
```

## Command-Line Arguments Reference

### Global Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--mode` | choice | `tui` | Generation mode: `gui`, `tui`, `number`, `float`, `color`, `string`, `custom`, `list` |
| `--count` | int | `1` | Number of values to generate |

### Number Mode Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--min` | float | `1` | Minimum value |
| `--max` | float | `100` | Maximum value |
| `--exclude` | string | - | Comma-separated values to exclude |

### Float Mode Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--min` | float | `0.0` | Minimum value |
| `--max` | float | `1.0` | Maximum value |
| `--decimals` | int | `2` | Number of decimal places |

### Color Mode Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--format` | choice | `hex` | Color format: `hex`, `rgb`, `hsl` |

### String Mode Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--length` | int | `10` | Length of generated string |
| `--pattern` | choice | `alphanumeric` | Character pattern (see available patterns above) |
| `--exclude-chars` | string | - | Characters to exclude from generation |

### Custom Mode Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--template` | string | - | Custom template pattern (required) |

### List Mode Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--items` | string | - | Comma-separated list of items (required) |
| `--unique` | flag | `false` | Select unique items only (no duplicates) |

## Practical Examples

### GUI Mode Examples

```bash
# Launch GUI for visual generation
python3 random_gen.py --mode gui

# Then use the interface to:
# 1. Select generation type (radio buttons)
# 2. Configure options in the form
# 3. Click "Generate"
# 4. Copy results with "Copy to Clipboard"
```

### Web Development

Generate random hex colors for design:
```bash
python3 random_gen.py --mode color --format hex --count 10 > colors.txt
```

### Security & Passwords

Generate secure random strings:
```bash
python3 random_gen.py --mode string --length 20 --pattern alphanumeric_symbols --count 5
```

### Testing & QA

Generate test data:
```bash
# Random user IDs
python3 random_gen.py --mode custom --template "USER-{d}{d}{d}{d}{d}" --count 100

# Random email-like strings
python3 random_gen.py --mode custom --template "{l}{l}{l}{l}{l}{d}{d}@test.com" --count 50
```

### Game Development

Generate random loot quantities:
```bash
python3 random_gen.py --mode number --min 1 --max 100 --count 1
```

### Data Science

Generate random float datasets:
```bash
python3 random_gen.py --mode float --min -10.0 --max 10.0 --decimals 3 --count 1000 > dataset.csv
```

### System Administration

Generate random MAC addresses:
```bash
python3 random_gen.py --mode custom --template "{x}{x}:{x}{x}:{x}{x}:{x}{x}:{x}{x}:{x}{x}" --count 1
```

## Use in Scripts

### GUI Mode in Scripts

```python
import subprocess

# Launch GUI for user to generate values
subprocess.run(['python3', 'random_gen.py', '--mode', 'gui'])
```

### Bash Script Example

```bash
#!/bin/bash

# Generate 5 random ports
for i in {1..5}; do
    PORT=$(python3 random_gen.py --mode number --min 3000 --max 9000)
    echo "Starting service on port $PORT"
done
```

### Python Script Example

```python
import subprocess

def get_random_color():
    result = subprocess.run(
        ['python3', 'random_gen.py', '--mode', 'color', '--format', 'hex'],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

color = get_random_color()
print(f"Random color: {color}")
```

## Screenshots

### GUI Mode
The graphical interface provides an intuitive way to generate random values with visual feedback:

- **Generation Type Selection**: Radio buttons for easy switching
- **Dynamic Options**: Form fields adapt to selected type
- **Results Display**: Scrollable text area with all generated values
- **Action Buttons**: Generate, Clear, and Copy to Clipboard

### TUI Mode
Text-based interactive menu for terminal environments:

- **Menu-Driven**: Numbered options for each generation type
- **Guided Input**: Prompts for all parameters
- **Immediate Results**: Display results after generation

### CLI Mode
Direct command-line usage for automation and scripting.

## Error Handling

The script provides clear error messages:

```bash
# Not enough available numbers
python3 random_gen.py --mode number --min 1 --max 5 --count 10 --exclude "1,2,3,4,5"
# Error: Not enough numbers available. Need 10, have 0

# Invalid format
python3 random_gen.py --mode color --format invalid
# Error: invalid choice: 'invalid' (choose from 'hex', 'rgb', 'hsl')
```

## Tips & Best Practices

1. **GUI Mode for Quick Tasks**: Use `--mode gui` when you need to experiment with different parameters visually

2. **Avoiding Confusing Characters**: When generating passwords or codes, exclude similar-looking characters:
   ```bash
   --exclude-chars "0oO1lI"
   ```

2. **TUI for Terminal Work**: Use TUI mode when working in SSH sessions or terminal-only environments

3. **CLI for Automation**: Use command-line mode in scripts and automated workflows

4. **Unique Random Selection**: Use `--unique` flag when you need distinct items from a list

5. **Reproducible Results**: For testing, you can seed Python's random before running

6. **Piping Output**: Combine with other tools:
   ```bash
   python3 random_gen.py --mode number --count 100 | sort -n | uniq
   ```

7. **Batch Generation**: Generate large datasets efficiently:
   ```bash
   python3 random_gen.py --mode float --count 10000 > data.txt
   ```

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Author

Created as a flexible tool for developers, testers, and anyone needing random value generation.

## Changelog

### Version 1.1
- ✨ Added GUI mode with tkinter
- 📋 Copy to clipboard functionality
- 🎨 Visual interface with dynamic forms
- 💡 Built-in help text for templates

### Version 1.0
- Initial release
- TUI and CLI support
- Number, float, color, string, custom pattern, and list generation
- Exclusion support
- Multiple color formats
- Template syntax for custom patterns
