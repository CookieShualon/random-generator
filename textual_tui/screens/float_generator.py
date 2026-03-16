"""Float generator screen."""

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Static, Button, Input
from textual.reactive import reactive
from textual_tui.widgets.result_display import ResultDisplay
from textual_tui.utils import validation


class FloatGeneratorScreen(Container):
    """Screen for generating random floating point numbers."""
    
    DEFAULT_CSS = """
    FloatGeneratorScreen {
        padding: 2 4;
        height: 100%;
    }
    
    FloatGeneratorScreen .screen-title {
        text-style: bold;
        color: $primary;
        text-align: center;
        margin-bottom: 2;
    }
    
    FloatGeneratorScreen .form-group {
        margin-bottom: 1;
    }
    
    FloatGeneratorScreen .form-label {
        color: $text;
        margin-bottom: 0;
    }
    
    FloatGeneratorScreen .input-hint {
        color: $text-muted;
        text-style: italic;
    }
    
    FloatGeneratorScreen .error-message {
        color: $error;
        text-style: bold;
    }
    
    FloatGeneratorScreen .button-group {
        layout: horizontal;
        height: auto;
        align: center middle;
        margin-top: 2;
    }
    """
    
    min_val = reactive("0.0")
    max_val = reactive("1.0")
    decimals = reactive("2")
    count = reactive("5")
    
    def __init__(self, generator, history_manager) -> None:
        super().__init__()
        self.generator = generator
        self.history_manager = history_manager
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Static("Generate Floats", classes="screen-title")
        
        # Form inputs
        with Vertical(classes="form-group"):
            yield Static("Minimum Value:", classes="form-label")
            yield Input(value="0.0", placeholder="0.0", id="min-input")
            yield Static("", id="min-error", classes="error-message")
        
        with Vertical(classes="form-group"):
            yield Static("Maximum Value:", classes="form-label")
            yield Input(value="1.0", placeholder="1.0", id="max-input")
            yield Static("", id="max-error", classes="error-message")
        
        with Vertical(classes="form-group"):
            yield Static("Decimal Places:", classes="form-label")
            yield Input(value="2", placeholder="2", id="decimals-input")
            yield Static("Number of decimal places (0-10)", classes="input-hint")
            yield Static("", id="decimals-error", classes="error-message")
        
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
    
    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes."""
        input_id = event.input.id
        
        if input_id == "min-input":
            self.min_val = event.value
        elif input_id == "max-input":
            self.max_val = event.value
        elif input_id == "decimals-input":
            self.decimals = event.value
        elif input_id == "count-input":
            self.count = event.value
        
        self.validate_inputs()
    
    def validate_inputs(self) -> bool:
        """Validate all inputs and show errors."""
        is_valid = True
        
        # Clear all errors
        self.query_one("#min-error", Static).update("")
        self.query_one("#max-error", Static).update("")
        self.query_one("#decimals-error", Static).update("")
        self.query_one("#count-error", Static).update("")
        
        # Validate min/max range
        if self.min_val and self.max_val:
            try:
                min_float = float(self.min_val)
                max_float = float(self.max_val)
                if min_float >= max_float:
                    self.query_one("#max-error", Static).update("Maximum must be greater than minimum")
                    is_valid = False
            except ValueError:
                self.query_one("#max-error", Static).update("Invalid number format")
                is_valid = False
        
        # Validate decimals
        if self.decimals:
            try:
                dec_int = int(self.decimals)
                if dec_int < 0 or dec_int > 10:
                    self.query_one("#decimals-error", Static).update("Decimals must be between 0 and 10")
                    is_valid = False
            except ValueError:
                self.query_one("#decimals-error", Static).update("Must be a valid integer")
                is_valid = False
        
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
            self.generate_floats()
        elif event.button.id == "clear-btn":
            self.clear_form()
    
    def generate_floats(self) -> None:
        """Generate random floats."""
        if not self.validate_inputs():
            self.notify("Please fix validation errors", severity="error")
            return
        
        try:
            min_float = float(self.min_val)
            max_float = float(self.max_val)
            decimals_int = int(self.decimals)
            count_int = int(self.count)
            
            # Generate floats
            results = self.generator.generate_float(min_float, max_float, decimals_int, count_int)
            
            # Display results
            result_display = self.query_one(ResultDisplay)
            result_display.set_results([str(r) for r in results])
            
            # Add to history
            self.history_manager.add_entry(
                "float",
                {
                    "min": min_float,
                    "max": max_float,
                    "decimals": decimals_int,
                    "count": count_int
                },
                [str(r) for r in results]
            )
            
            self.notify(f"Generated {len(results)} floats", severity="information")
            
        except Exception as e:
            self.notify(f"Error: {str(e)}", severity="error")
    
    def clear_form(self) -> None:
        """Clear the form."""
        self.query_one("#min-input", Input).value = "0.0"
        self.query_one("#max-input", Input).value = "1.0"
        self.query_one("#decimals-input", Input).value = "2"
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
