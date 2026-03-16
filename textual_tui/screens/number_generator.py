"""Number generator screen with live preview."""

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Static, Button, Input
from textual.reactive import reactive
from typing import Set, Optional
from textual_tui.widgets.result_display import ResultDisplay
from textual_tui.utils import validation


class NumberGeneratorScreen(Container):
    """Screen for generating random numbers."""
    
    DEFAULT_CSS = """
    NumberGeneratorScreen {
        padding: 2 4;
        height: 100%;
        overflow-y: auto;
    }
    
    NumberGeneratorScreen .screen-title {
        text-style: bold;
        color: $primary;
        text-align: center;
        margin-bottom: 2;
    }
    
    NumberGeneratorScreen .form-group {
        margin-bottom: 1;
    }
    
    NumberGeneratorScreen .form-label {
        color: $text;
        margin-bottom: 0;
    }
    
    NumberGeneratorScreen .input-hint {
        color: $text-muted;
        text-style: italic;
    }
    
    NumberGeneratorScreen .error-message {
        color: $error;
        text-style: bold;
    }
    
    NumberGeneratorScreen .button-group {
        layout: horizontal;
        height: auto;
        align: center middle;
        margin-top: 2;
    }
    """
    
    min_val = reactive("1")
    max_val = reactive("100")
    count = reactive("5")
    exclude = reactive("")
    
    def __init__(self, generator, history_manager) -> None:
        super().__init__()
        self.generator = generator
        self.history_manager = history_manager
        self.error_message = ""
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Static("Generate Numbers", classes="screen-title")
        
        # Form inputs
        with Vertical(classes="form-group"):
            yield Static("Minimum Value:", classes="form-label")
            yield Input(value="1", placeholder="1", id="min-input")
            yield Static("", id="min-error", classes="error-message")
        
        with Vertical(classes="form-group"):
            yield Static("Maximum Value:", classes="form-label")
            yield Input(value="100", placeholder="100", id="max-input")
            yield Static("", id="max-error", classes="error-message")
        
        with Vertical(classes="form-group"):
            yield Static("Count:", classes="form-label")
            yield Input(value="5", placeholder="5", id="count-input")
            yield Static("", id="count-error", classes="error-message")
        
        with Vertical(classes="form-group"):
            yield Static("Exclude (comma-separated):", classes="form-label")
            yield Input(value="", placeholder="13,7,42", id="exclude-input")
            yield Static("Optional: numbers to exclude", classes="input-hint")
            yield Static("", id="exclude-error", classes="error-message")
        
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
        elif input_id == "count-input":
            self.count = event.value
        elif input_id == "exclude-input":
            self.exclude = event.value
        
        self.validate_inputs()
    
    def validate_inputs(self) -> bool:
        """Validate all inputs and show errors."""
        is_valid = True
        
        # Clear all errors
        self.query_one("#min-error", Static).update("")
        self.query_one("#max-error", Static).update("")
        self.query_one("#count-error", Static).update("")
        self.query_one("#exclude-error", Static).update("")
        
        # Validate min/max range
        if self.min_val and self.max_val:
            valid, error = validation.validate_number_range(self.min_val, self.max_val)
            if not valid:
                self.query_one("#max-error", Static).update(error)
                is_valid = False
        
        # Validate count
        if self.count:
            valid, error = validation.validate_count(self.count)
            if not valid:
                self.query_one("#count-error", Static).update(error)
                is_valid = False
        
        # Validate exclude
        if self.exclude:
            valid, excluded_set, error = validation.parse_exclude_numbers(self.exclude)
            if not valid:
                self.query_one("#exclude-error", Static).update(error)
                is_valid = False
        
        return is_valid
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "generate-btn":
            self.generate_numbers()
        elif event.button.id == "clear-btn":
            self.clear_form()
    
    def generate_numbers(self) -> None:
        """Generate random numbers."""
        if not self.validate_inputs():
            self.notify("Please fix validation errors", severity="error")
            return
        
        try:
            min_int = int(self.min_val)
            max_int = int(self.max_val)
            count_int = int(self.count)
            
            # Parse exclusions
            excluded = set()
            if self.exclude:
                _, excluded, _ = validation.parse_exclude_numbers(self.exclude)
            
            # Validate generation is possible
            valid, error = validation.validate_number_generation(min_int, max_int, excluded, count_int)
            if not valid:
                self.notify(error, severity="error")
                return
            
            # Generate numbers
            results = self.generator.generate_number(min_int, max_int, excluded, count_int)
            
            # Display results
            result_display = self.query_one(ResultDisplay)
            result_display.set_results([str(r) for r in results])
            
            # Add to history
            self.history_manager.add_entry(
                "number",
                {
                    "min": min_int,
                    "max": max_int,
                    "exclude": list(excluded),
                    "count": count_int
                },
                [str(r) for r in results]
            )
            
            self.notify(f"Generated {len(results)} numbers", severity="information")
            
        except Exception as e:
            self.notify(f"Error: {str(e)}", severity="error")
    
    def clear_form(self) -> None:
        """Clear the form."""
        self.query_one("#min-input", Input).value = "1"
        self.query_one("#max-input", Input).value = "100"
        self.query_one("#count-input", Input).value = "5"
        self.query_one("#exclude-input", Input).value = ""
        
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
