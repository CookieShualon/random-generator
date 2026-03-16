"""List selection generator screen."""

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Static, Button, Input, TextArea, Checkbox
from textual.reactive import reactive
from textual_tui.widgets.result_display import ResultDisplay
from textual_tui.utils import validation


class ListGeneratorScreen(Container):
    """Screen for selecting random items from a list."""
    
    DEFAULT_CSS = """
    ListGeneratorScreen {
        padding: 2 4;
        height: 100%;
        overflow-y: auto;
    }
    
    ListGeneratorScreen .screen-title {
        text-style: bold;
        color: $primary;
        text-align: center;
        margin-bottom: 2;
    }
    
    ListGeneratorScreen .form-group {
        margin-bottom: 1;
        height: auto;
    }
    
    ListGeneratorScreen .textarea-group {
        margin-bottom: 2;
        height: auto;
    }
    
    ListGeneratorScreen .form-label {
        color: $text;
        margin-bottom: 0;
    }
    
    ListGeneratorScreen .input-hint {
        color: $text-muted;
        text-style: italic;
    }
    
    ListGeneratorScreen .error-message {
        color: $error;
        text-style: bold;
    }
    
    ListGeneratorScreen .button-group {
        layout: horizontal;
        height: auto;
        align: center middle;
        margin-top: 2;
    }
    
    ListGeneratorScreen #items-textarea {
        height: 10;
        min-height: 10;
        max-height: 10;
        margin-bottom: 2;
    }
    """
    
    items_text = reactive("")
    count = reactive("3")
    unique = reactive(True)
    
    def __init__(self, generator, history_manager) -> None:
        super().__init__()
        self.generator = generator
        self.history_manager = history_manager
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Static("Select from List", classes="screen-title")
        
        # Form inputs
        with Vertical(classes="textarea-group"):
            yield Static("Items (one per line):", classes="form-label")
            textarea = TextArea(id="items-textarea")
            textarea.show_vertical_scrollbar = True
            textarea.styles.height = 10
            textarea.styles.min_height = 10
            textarea.styles.max_height = 10
            yield textarea
            yield Static("Enter items, one per line", classes="input-hint")
            yield Static("", id="items-error", classes="error-message")
        
        with Vertical(classes="form-group"):
            yield Static("Count:", classes="form-label")
            yield Input(value="3", placeholder="3", id="count-input")
            yield Static("", id="count-error", classes="error-message")
        
        with Vertical(classes="form-group"):
            yield Checkbox("Unique selections (no duplicates)", value=True, id="unique-checkbox")
        
        # Buttons
        with Horizontal(classes="button-group"):
            yield Button("Generate", id="generate-btn", variant="primary")
            yield Button("Clear", id="clear-btn")
        
        # Results
        yield ResultDisplay()
    
    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        """Handle textarea changes."""
        if event.text_area.id == "items-textarea":
            self.items_text = event.text_area.text
    
    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes."""
        if event.input.id == "count-input":
            self.count = event.value
    
    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        """Handle checkbox changes."""
        if event.checkbox.id == "unique-checkbox":
            self.unique = event.value
    
    def validate_inputs(self) -> bool:
        """Validate all inputs and show errors."""
        is_valid = True
        
        # Clear all errors
        self.query_one("#items-error", Static).update("")
        self.query_one("#count-error", Static).update("")
        
        # Validate items
        items = [line.strip() for line in self.items_text.split('\n') if line.strip()]
        if not items:
            self.query_one("#items-error", Static).update("Please enter at least one item")
            is_valid = False
        
        # Validate count
        if self.count:
            valid, error = validation.validate_count(self.count)
            if not valid:
                self.query_one("#count-error", Static).update(error)
                is_valid = False
            else:
                try:
                    count_int = int(self.count)
                    if self.unique and count_int > len(items):
                        self.query_one("#count-error", Static).update(
                            f"Cannot select {count_int} unique items from {len(items)} items"
                        )
                        is_valid = False
                except ValueError:
                    pass
        
        return is_valid
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "generate-btn":
            self.generate_from_list()
        elif event.button.id == "clear-btn":
            self.clear_form()
    
    def generate_from_list(self) -> None:
        """Generate random selections from list."""
        if not self.validate_inputs():
            self.notify("Please fix validation errors", severity="error")
            return
        
        try:
            items = [line.strip() for line in self.items_text.split('\n') if line.strip()]
            count_int = int(self.count)
            
            # Generate selections
            results = self.generator.generate_from_list(items, count_int, self.unique)
            
            # Display results
            result_display = self.query_one(ResultDisplay)
            result_display.set_results(results)
            
            # Add to history
            self.history_manager.add_entry(
                "list",
                {
                    "items_count": len(items),
                    "count": count_int,
                    "unique": self.unique
                },
                results
            )
            
            self.notify(f"Selected {len(results)} items", severity="information")
            
        except Exception as e:
            self.notify(f"Error: {str(e)}", severity="error")
    
    def clear_form(self) -> None:
        """Clear the form."""
        self.query_one("#items-textarea", TextArea).text = ""
        self.query_one("#count-input", Input).value = "3"
        self.query_one("#unique-checkbox", Checkbox).value = True
        
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
