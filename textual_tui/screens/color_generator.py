"""Color generator screen."""

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Static, Button, Input, RadioSet, RadioButton
from textual.reactive import reactive
from textual_tui.widgets.result_display import ResultDisplay
from textual_tui.utils import validation


class ColorGeneratorScreen(Container):
    """Screen for generating random colors."""
    
    DEFAULT_CSS = """
    ColorGeneratorScreen {
        padding: 2 4;
        height: 100%;
        overflow-y: auto;
    }
    
    ColorGeneratorScreen .screen-title {
        text-style: bold;
        color: $primary;
        text-align: center;
        margin-bottom: 2;
    }
    
    ColorGeneratorScreen .form-group {
        margin-bottom: 1;
    }
    
    ColorGeneratorScreen .form-label {
        color: $text;
        margin-bottom: 0;
    }
    
    ColorGeneratorScreen .input-hint {
        color: $text-muted;
        text-style: italic;
    }
    
    ColorGeneratorScreen .error-message {
        color: $error;
        text-style: bold;
    }
    
    ColorGeneratorScreen .button-group {
        layout: horizontal;
        height: auto;
        align: center middle;
        margin-top: 2;
    }
    
    ColorGeneratorScreen RadioSet {
        background: transparent;
        border: none;
        padding: 0;
    }
    
    ColorGeneratorScreen RadioButton {
        margin-bottom: 0;
    }
    """
    
    format_type = reactive("hex")
    count = reactive("5")
    
    def __init__(self, generator, history_manager) -> None:
        super().__init__()
        self.generator = generator
        self.history_manager = history_manager
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Static("Generate Colors", classes="screen-title")
        
        # Form inputs
        with Vertical(classes="form-group"):
            yield Static("Color Format:", classes="form-label")
            with RadioSet(id="format-radio"):
                yield RadioButton("HEX (#RRGGBB)", value=True, id="hex-radio")
                yield RadioButton("RGB (rgb(r, g, b))", id="rgb-radio")
                yield RadioButton("HSL (hsl(h, s%, l%))", id="hsl-radio")
        
        with Vertical(classes="form-group"):
            yield Static("Count:", classes="form-label")
            yield Input(value="5", placeholder="5", id="count-input")
            yield Static("", id="count-error", classes="error-message")
        
        # Buttons
        with Horizontal(classes="button-group"):
            yield Button("Generate", id="generate-btn", variant="primary")
            yield Button("Clear", id="clear-btn")
        
        # Results
        yield ResultDisplay()
    
    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        """Handle radio button changes."""
        if event.pressed.id == "hex-radio":
            self.format_type = "hex"
        elif event.pressed.id == "rgb-radio":
            self.format_type = "rgb"
        elif event.pressed.id == "hsl-radio":
            self.format_type = "hsl"
    
    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes."""
        if event.input.id == "count-input":
            self.count = event.value
            self.validate_inputs()
    
    def validate_inputs(self) -> bool:
        """Validate all inputs and show errors."""
        is_valid = True
        
        # Clear all errors
        self.query_one("#count-error", Static).update("")
        
        # Validate count
        if self.count:
            valid, error = validation.validate_count(self.count)
            if not valid:
                self.query_one("#count-error", Static).update(error)
                is_valid = False
        
        return is_valid
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "generate-btn":
            self.generate_colors()
        elif event.button.id == "clear-btn":
            self.clear_form()
    
    def generate_colors(self) -> None:
        """Generate random colors."""
        if not self.validate_inputs():
            self.notify("Please fix validation errors", severity="error")
            return
        
        try:
            count_int = int(self.count)
            
            # Generate colors
            results = self.generator.generate_color(self.format_type, count_int)
            
            # Display results with color type
            result_display = self.query_one(ResultDisplay)
            result_display.set_results(results, result_type="color")
            
            # Add to history
            self.history_manager.add_entry(
                "color",
                {
                    "format": self.format_type,
                    "count": count_int
                },
                results
            )
            
            self.notify(f"Generated {len(results)} colors", severity="information")
            
        except Exception as e:
            self.notify(f"Error: {str(e)}", severity="error")
    
    def clear_form(self) -> None:
        """Clear the form."""
        self.query_one("#count-input", Input).value = "5"
        
        result_display = self.query_one(ResultDisplay)
        result_display.clear_results()
    
    def on_result_display_copy_requested(self, message: ResultDisplay.CopyRequested) -> None:
        """Handle copy request from result display."""
        from textual_tui.utils import clipboard
        
        result_display = self.query_one(ResultDisplay)
        if result_display.has_results():
            if clipboard.copy_results(result_display.get_results(), ", "):
                self.notify("Copied to clipboard!", severity="information")
            else:
                self.notify("Clipboard not available", severity="warning")
    
    def on_result_display_export_requested(self, message: ResultDisplay.ExportRequested) -> None:
        """Handle export request from result display."""
        self.notify("Export feature coming soon!", severity="information")
