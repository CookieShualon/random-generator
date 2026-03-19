"""Result display widget with copy functionality."""

from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Button, Static, RichLog
from textual.message import Message
from rich.text import Text
from typing import List, Optional


class ResultDisplay(Container):
    """Widget for displaying generation results with actions."""
    
    DEFAULT_CSS = """
    ResultDisplay {
        height: auto;
        margin-top: 2;
    }
    
    ResultDisplay .results-header {
        color: $primary;
        text-style: bold;
        margin-bottom: 1;
    }
    
    ResultDisplay #results-container {
        border: tall $primary;
        background: $surface-darken-1;
        padding: 1;
        min-height: 5;
        max-height: 20;
        overflow-y: auto;
    }
    
    ResultDisplay .button-group {
        layout: horizontal;
        height: auto;
        margin-top: 1;
        padding-right: 2;
    }
    
    ResultDisplay Button {
        margin-right: 1;
    }
    """
    
    class CopyRequested(Message):
        """Message sent when copy button is clicked."""
        pass
    
    class ExportRequested(Message):
        """Message sent when export button is clicked."""
        pass
    
    def __init__(self) -> None:
        super().__init__()
        self.results: List[str] = []
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Static("Results:", classes="results-header")
        yield RichLog(id="results-container", wrap=True, highlight=True)
        with Horizontal(classes="button-group"):
            yield Button("📋 Copy", id="copy-btn", variant="primary")
            yield Button("💾 Export", id="export-btn")
            yield Button("🗑️  Clear", id="results-clear-btn", variant="default")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "copy-btn":
            self.post_message(self.CopyRequested())
        elif event.button.id == "export-btn":
            self.post_message(self.ExportRequested())
        elif event.button.id == "results-clear-btn":
            self.clear_results()
    
    def set_results(self, results: List[str], result_type: Optional[str] = None) -> None:
        """
        Set and display results.
        
        Args:
            results: List of results to display
            result_type: Type of results for formatting (color, number, etc.)
        """
        self.results = results
        results_log = self.query_one("#results-container", RichLog)
        results_log.clear()
        
        if not results:
            results_log.write("No results yet. Click Generate to create values.")
            return
        
        # Format results based on type
        if result_type == "color":
            self._display_colors(results, results_log)
        else:
            self._display_generic(results, results_log)
    
    def _display_colors(self, results: List[str], log: RichLog) -> None:
        """Display color results with swatches."""
        for color in results:
            # Try to parse color for swatch
            if color.startswith('#'):
                # Hex color
                try:
                    hex_color = color.lstrip('#')
                    r = int(hex_color[0:2], 16)
                    g = int(hex_color[2:4], 16)
                    b = int(hex_color[4:6], 16)
                    
                    # Create colored text
                    text = Text()
                    text.append("██ ", style=f"rgb({r},{g},{b})")
                    text.append(color)
                    log.write(text)
                except:
                    log.write(color)
            elif color.startswith('rgb('):
                # RGB color
                try:
                    rgb_str = color[4:-1]  # Remove 'rgb(' and ')'
                    r, g, b = map(int, rgb_str.split(','))
                    
                    text = Text()
                    text.append("██ ", style=f"rgb({r},{g},{b})")
                    text.append(color)
                    log.write(text)
                except:
                    log.write(color)
            else:
                log.write(color)
    
    def _display_generic(self, results: List[str], log: RichLog) -> None:
        """Display generic results."""
        # Display as comma-separated list on one line
        result_text = ", ".join(str(result) for result in results)
        log.write(result_text)
    
    def clear_results(self) -> None:
        """Clear displayed results."""
        self.results = []
        results_log = self.query_one("#results-container", RichLog)
        results_log.clear()
        results_log.write("Results cleared.")
    
    def get_results(self) -> List[str]:
        """Get current results."""
        return self.results
    
    def has_results(self) -> bool:
        """Check if there are results."""
        return len(self.results) > 0
