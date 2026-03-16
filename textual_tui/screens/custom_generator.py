"""Custom pattern generator screen."""

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Static, Button, Input
from textual.reactive import reactive
from textual_tui.widgets.result_display import ResultDisplay
from textual_tui.utils import validation


class CustomGeneratorScreen(Container):
    """Screen for generating values from custom templates."""
    
    DEFAULT_CSS = """
    CustomGeneratorScreen {
        padding: 2 4;
        height: 100%;
    }
    
    CustomGeneratorScreen .screen-title {
        text-style: bold;
        color: $primary;
        text-align: center;
        margin-bottom: 2;
    }
    
    CustomGeneratorScreen .form-group {
        margin-bottom: 1;
    }
    
    CustomGeneratorScreen .form-label {
        color: $text;
        margin-bottom: 0;
    }
    
    CustomGeneratorScreen .input-hint {
        color: $text-muted;
        text-style: italic;
    }
    
    CustomGeneratorScreen .error-message {
        color: $error;
        text-style: bold;
    }
    
    CustomGeneratorScreen .button-group {
        layout: horizontal;
        height: auto;
        align: center middle;
        margin-top: 2;
    }
    
    CustomGeneratorScreen .syntax-box {
        border: tall $accent;
        background: $surface-darken-2;
        padding: 1;
        margin: 1 0;
    }
    
    CustomGeneratorScreen .syntax-title {
        color: $accent;
        text-style: bold;
        margin-bottom: 1;
    }
    
    CustomGeneratorScreen .syntax-item {
        color: $text;
        margin-left: 2;
    }
    """
    
    template = reactive("")
    count = reactive("5")
    
    def __init__(self, generator, history_manager) -> None:
        super().__init__()
        self.generator = generator
        self.history_manager = history_manager
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Static("Generate Custom Pattern", classes="screen-title")
        
        # Syntax help
        with Container(classes="syntax-box"):
            yield Static("Template Syntax:", classes="syntax-title")
            yield Static("{d} - digit (0-9)", classes="syntax-item")
            yield Static("{l} - lowercase letter (a-z)", classes="syntax-item")
            yield Static("{u} - uppercase letter (A-Z)", classes="syntax-item")
            yield Static("{a} - any letter (A-Z, a-z)", classes="syntax-item")
            yield Static("{x} - hexadecimal (0-9, a-f)", classes="syntax-item")
            yield Static("{s} - symbol (!@#$%...)", classes="syntax-item")
            yield Static("{w} - word character (A-Z, a-z, 0-9)", classes="syntax-item")
        
        # Form inputs
        with Vertical(classes="form-group"):
            yield Static("Template:", classes="form-label")
            yield Input(value="", placeholder="USER-{d}{d}{d}{d}", id="template-input")
            yield Static("Example: USER-{d}{d}{d}{d} → USER-1234", classes="input-hint")
            yield Static("", id="template-error", classes="error-message")
        
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
        
        if input_id == "template-input":
            self.template = event.value
        elif input_id == "count-input":
            self.count = event.value
        
        self.validate_inputs()
    
    def validate_inputs(self) -> bool:
        """Validate all inputs and show errors."""
        is_valid = True
        
        # Clear all errors
        self.query_one("#template-error", Static).update("")
        self.query_one("#count-error", Static).update("")
        
        # Validate template
        if not self.template:
            self.query_one("#template-error", Static).update("Template is required")
            is_valid = False
        elif not any(placeholder in self.template for placeholder in ['{d}', '{l}', '{u}', '{a}', '{x}', '{s}', '{w}']):
            self.query_one("#template-error", Static).update("Template must contain at least one placeholder")
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
            self.generate_custom()
        elif event.button.id == "clear-btn":
            self.clear_form()
    
    def generate_custom(self) -> None:
        """Generate custom pattern values."""
        if not self.validate_inputs():
            self.notify("Please fix validation errors", severity="error")
            return
        
        try:
            count_int = int(self.count)
            
            # Generate custom values
            results = self.generator.generate_custom(self.template, count_int)
            
            # Display results
            result_display = self.query_one(ResultDisplay)
            result_display.set_results(results)
            
            # Add to history
            self.history_manager.add_entry(
                "custom",
                {
                    "template": self.template,
                    "count": count_int
                },
                results
            )
            
            self.notify(f"Generated {len(results)} values", severity="information")
            
        except Exception as e:
            self.notify(f"Error: {str(e)}", severity="error")
    
    def clear_form(self) -> None:
        """Clear the form."""
        self.query_one("#template-input", Input).value = ""
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
