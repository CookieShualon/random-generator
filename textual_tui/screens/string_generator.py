"""String generator screen."""

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Static, Button, Input, RadioSet, RadioButton
from textual.reactive import reactive
from textual_tui.widgets.result_display import ResultDisplay
from textual_tui.utils import validation


class StringGeneratorScreen(Container):
    """Screen for generating random strings."""
    
    DEFAULT_CSS = """
    StringGeneratorScreen {
        padding: 2 4;
        height: 100%;
        overflow-y: auto;
    }
    
    StringGeneratorScreen .screen-title {
        text-style: bold;
        color: $primary;
        text-align: center;
        margin-bottom: 2;
    }
    
    StringGeneratorScreen .form-group {
        margin-bottom: 1;
    }
    
    StringGeneratorScreen .form-label {
        color: $text;
        margin-bottom: 0;
    }
    
    StringGeneratorScreen .input-hint {
        color: $text-muted;
        text-style: italic;
    }
    
    StringGeneratorScreen .error-message {
        color: $error;
        text-style: bold;
    }
    
    StringGeneratorScreen .button-group {
        layout: horizontal;
        height: auto;
        align: center middle;
        margin-top: 2;
    }
    
    StringGeneratorScreen RadioSet {
        background: transparent;
        border: none;
        padding: 0;
    }
    
    StringGeneratorScreen RadioButton {
        margin-bottom: 0;
    }
    """
    
    length = reactive("10")
    pattern = reactive("alphanumeric")
    exclude_chars = reactive("")
    count = reactive("5")
    
    def __init__(self, generator, history_manager) -> None:
        super().__init__()
        self.generator = generator
        self.history_manager = history_manager
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Static("Generate Strings", classes="screen-title")
        
        # Form inputs
        with Vertical(classes="form-group"):
            yield Static("String Length:", classes="form-label")
            yield Input(value="10", placeholder="10", id="length-input")
            yield Static("", id="length-error", classes="error-message")
        
        with Vertical(classes="form-group"):
            yield Static("Pattern:", classes="form-label")
            with RadioSet(id="pattern-radio"):
                yield RadioButton("Alphanumeric (A-Z, a-z, 0-9)", value=True, id="alphanumeric-radio")
                yield RadioButton("Alpha (A-Z, a-z)", id="alpha-radio")
                yield RadioButton("Numeric (0-9)", id="numeric-radio")
                yield RadioButton("Lowercase (a-z)", id="lowercase-radio")
                yield RadioButton("Uppercase (A-Z)", id="uppercase-radio")
                yield RadioButton("Hex (0-9, a-f)", id="hex-radio")
                yield RadioButton("Symbols (!@#$%...)", id="symbols-radio")
                yield RadioButton("Alphanumeric + Symbols", id="alphanumeric_symbols-radio")
        
        with Vertical(classes="form-group"):
            yield Static("Exclude Characters:", classes="form-label")
            yield Input(value="", placeholder="O0Il1", id="exclude-input")
            yield Static("Optional: characters to exclude", classes="input-hint")
        
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
        radio_id = event.pressed.id
        if radio_id == "alphanumeric-radio":
            self.pattern = "alphanumeric"
        elif radio_id == "alpha-radio":
            self.pattern = "alpha"
        elif radio_id == "numeric-radio":
            self.pattern = "numeric"
        elif radio_id == "lowercase-radio":
            self.pattern = "lowercase"
        elif radio_id == "uppercase-radio":
            self.pattern = "uppercase"
        elif radio_id == "hex-radio":
            self.pattern = "hex"
        elif radio_id == "symbols-radio":
            self.pattern = "symbols"
        elif radio_id == "alphanumeric_symbols-radio":
            self.pattern = "alphanumeric_symbols"
    
    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes."""
        input_id = event.input.id
        
        if input_id == "length-input":
            self.length = event.value
        elif input_id == "exclude-input":
            self.exclude_chars = event.value
        elif input_id == "count-input":
            self.count = event.value
        
        self.validate_inputs()
    
    def validate_inputs(self) -> bool:
        """Validate all inputs and show errors."""
        is_valid = True
        
        # Clear all errors
        self.query_one("#length-error", Static).update("")
        self.query_one("#count-error", Static).update("")
        
        # Validate length
        if self.length:
            try:
                length_int = int(self.length)
                if length_int < 1 or length_int > 1000:
                    self.query_one("#length-error", Static).update("Length must be between 1 and 1000")
                    is_valid = False
            except ValueError:
                self.query_one("#length-error", Static).update("Must be a valid integer")
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
            self.generate_strings()
        elif event.button.id == "clear-btn":
            self.clear_form()
    
    def generate_strings(self) -> None:
        """Generate random strings."""
        if not self.validate_inputs():
            self.notify("Please fix validation errors", severity="error")
            return
        
        try:
            length_int = int(self.length)
            count_int = int(self.count)
            
            # Generate strings
            results = self.generator.generate_string(
                length_int,
                self.pattern,
                self.exclude_chars,
                count_int
            )
            
            # Display results
            result_display = self.query_one(ResultDisplay)
            result_display.set_results(results)
            
            # Add to history
            self.history_manager.add_entry(
                "string",
                {
                    "length": length_int,
                    "pattern": self.pattern,
                    "exclude_chars": self.exclude_chars,
                    "count": count_int
                },
                results
            )
            
            self.notify(f"Generated {len(results)} strings", severity="information")
            
        except Exception as e:
            self.notify(f"Error: {str(e)}", severity="error")
    
    def clear_form(self) -> None:
        """Clear the form."""
        self.query_one("#length-input", Input).value = "10"
        self.query_one("#exclude-input", Input).value = ""
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
