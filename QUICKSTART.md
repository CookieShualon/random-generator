# Quick Start Guide - Enhanced TUI Mode

## Installation (30 seconds)

```bash
# 1. Install dependencies
pip install textual pyperclip

# 2. Run the app
python3 random_gen.py
```

That's it! The enhanced TUI will launch automatically.

## First Steps

### 1. Navigate the Interface

```
┌─────────────────────────────────────────────────────────────┐
│ 🎲 Random Value Generator                                   │
├──────────┬──────────────────────────────────────────────────┤
│          │                                                  │
│  Menu    │           Main Content Area                     │
│          │                                                  │
│ • Home   │  [Your current screen appears here]             │
│ • Number │                                                  │
│ • Float  │                                                  │
│ • Color  │                                                  │
│ • String │                                                  │
│ • Custom │                                                  │
│ • List   │                                                  │
│ ─────    │                                                  │
│ • History│                                                  │
│ • Help   │                                                  │
│          │                                                  │
├──────────┴──────────────────────────────────────────────────┤
│ F1-F6: Quick Access  Ctrl+H: Help  Ctrl+Q: Quit            │
└─────────────────────────────────────────────────────────────┘
```

### 2. Generate Your First Random Numbers

**Option A: Using Quick Actions (Home Screen)**
1. You'll see three quick action cards on the home screen
2. Click or press Enter on "Numbers" card
3. The number generator screen opens

**Option B: Using Keyboard Shortcut**
1. Press `F1` from anywhere in the app
2. Number generator screen opens instantly

**Option C: Using Navigation Menu**
1. Click "Numbers" in the left sidebar
2. Or use arrow keys to navigate and press Enter

### 3. Configure and Generate

```
Generate Numbers
────────────────

Minimum Value:  [1        ]  ◄ Type your min value
Maximum Value:  [100      ]  ◄ Type your max value
Count:          [5        ]  ◄ How many numbers
Exclude:        [13,7,42  ]  ◄ Optional: numbers to skip

Preview:
Range: 1 to 100 (excluding 3 values)
Available: 97 numbers

[Generate]  [Clear]

Results:
┌────────────────────────────────────────────────────────────┐
│ 42                                                         │
│ 17                                                         │
│ 89                                                         │
│ 3                                                          │
│ 56                                                         │
│                                                            │
│ [📋 Copy] [💾 Export] [🗑️  Clear]                          │
└────────────────────────────────────────────────────────────┘
```

1. **Fill in the form:**
   - Use Tab to move between fields
   - Type your values
   - Watch the live preview update

2. **Generate:**
   - Click "Generate" button
   - Or press Enter when focused on a button
   - Results appear instantly below

3. **Copy Results:**
   - Click "📋 Copy" button
   - Results are copied to clipboard
   - Paste anywhere (Ctrl+V / Cmd+V)

## Essential Keyboard Shortcuts

### Navigation
- `↑↓` or `hjkl` - Move through menu/fields
- `Tab` - Next field
- `Enter` - Confirm/Generate
- `Esc` - Go back

### Quick Access
- `F1` - Numbers Generator
- `F2` - Floats Generator
- `F3` - Colors Generator
- `F4` - Strings Generator
- `F5` - Custom Pattern
- `F6` - List Selection

### Actions
- `Ctrl+H` - Show Help
- `Ctrl+R` - View History
- `Ctrl+Q` - Quit App

## Common Tasks

### Generate Random Password-like Strings

1. Press `F4` (Strings Generator)
2. Set length: `16`
3. Select pattern: `alphanumeric_symbols`
4. Exclude confusing chars: `0oO1lI`
5. Click Generate

### Generate Hex Colors for Design

1. Press `F3` (Colors Generator)
2. Select format: `HEX`
3. Set count: `5`
4. Click Generate
5. See color swatches with codes
6. Copy to clipboard

### Generate License Plate Format

1. Press `F5` (Custom Pattern)
2. Enter template: `{u}{u}{u}-{d}{d}{d}`
3. Set count: `10`
4. Click Generate
5. Results like: ABC-123, XYZ-789

## Tips

💡 **Live Preview**: Watch the preview section update as you type to see what you'll generate

💡 **History**: All generations are automatically saved. Check recent ones on the home screen

💡 **Clipboard**: Click Copy to instantly copy all results to clipboard

💡 **Keyboard Only**: The entire app can be used without a mouse

💡 **Help Anytime**: Press `Ctrl+H` to see full documentation

## Troubleshooting

### "Enhanced TUI mode available with 'pip install textual'"

You're seeing the classic TUI. Install Textual for the enhanced version:
```bash
pip install textual
```

### Clipboard Not Working

Install pyperclip:
```bash
pip install pyperclip
```

### Colors Look Wrong

Use a modern terminal:
- macOS: iTerm2 or Terminal.app
- Windows: Windows Terminal
- Linux: GNOME Terminal, Konsole

## Next Steps

- Press `Ctrl+H` to read full help documentation
- Try all generator types (F1-F6)
- Check your history (Ctrl+R)
- Explore keyboard shortcuts

## Need More Help?

- Press `Ctrl+H` in the app for complete documentation
- Read [TEXTUAL_TUI_README.md](TEXTUAL_TUI_README.md) for detailed info
- Check [plans/tui-improvement-plan.md](plans/tui-improvement-plan.md) for architecture

Enjoy generating random values! 🎲
