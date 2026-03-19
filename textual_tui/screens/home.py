"""Home screen with quick actions and recent history."""

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Static, Button
from textual.screen import Screen
from textual.message import Message


class QuickActionCard(Container):
    """A clickable card for quick actions."""
    
    DEFAULT_CSS = """
    QuickActionCard {
        border: tall $primary;
        background: $surface-darken-1;
        padding: 1 2;
        width: 1fr;
        min-width: 16;
        max-width: 28;
        height: auto;
        min-height: 5;
        margin: 0 1;
    }
    
    QuickActionCard:hover {
        background: $primary-darken-2;
        border: tall $accent;
    }
    
    QuickActionCard .icon {
        text-align: center;
        color: $primary;
        text-style: bold;
        content-align: center middle;
    }
    
    QuickActionCard .title {
        text-align: center;
        color: $text;
        text-style: bold;
        margin-top: 1;
    }
    
    QuickActionCard .subtitle {
        text-align: center;
        color: $text-muted;
    }
    """
    
    class Clicked(Message):
        """Message sent when card is clicked."""
        
        def __init__(self, action_id: str) -> None:
            self.action_id = action_id
            super().__init__()
    
    def __init__(self, icon: str, title: str, subtitle: str, action_id: str) -> None:
        super().__init__()
        self.icon = icon
        self.title_text = title
        self.subtitle_text = subtitle
        self.action_id = action_id
        self.can_focus = True
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Static(self.icon, classes="icon")
        yield Static(self.title_text, classes="title")
        yield Static(self.subtitle_text, classes="subtitle")
    
    def on_click(self) -> None:
        """Handle click event."""
        self.post_message(self.Clicked(self.action_id))


class HomeScreen(Container):
    """Home screen with welcome message and quick actions."""
    
    DEFAULT_CSS = """
    HomeScreen {
        padding: 2 4;
        height: auto;
        overflow-y: auto;
    }
    
    HomeScreen .welcome-title {
        text-style: bold;
        color: $primary;
        text-align: center;
        margin-bottom: 2;
    }
    
    HomeScreen .section-title {
        color: $primary;
        text-style: bold;
        margin-top: 2;
        margin-bottom: 1;
    }
    
    HomeScreen .quick-actions {
        layout: horizontal;
        height: auto;
        align: center top;
        margin-bottom: 2;
    }
    
    HomeScreen .recent-item {
        color: $text;
        margin-bottom: 0;
    }
    
    HomeScreen .tip {
        color: $text-muted;
        text-style: italic;
        margin-top: 2;
        text-align: center;
    }
    """
    
    def __init__(self, history_manager) -> None:
        super().__init__()
        self.history_manager = history_manager
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Static("Welcome to Random Generator", classes="welcome-title")
        
        yield Static("Quick Actions:", classes="section-title")
        with Horizontal(classes="quick-actions"):
            yield QuickActionCard("🎲", "Numbers", "1-100", "number")
            yield QuickActionCard("🎨", "Colors", "#HEX", "color")
            yield QuickActionCard("📝", "Strings", "A-Z0-9", "string")
        
        yield Static("Recent Generations:", classes="section-title")
        yield Container(id="recent-history")
        
        yield Static("Tip: Press F1-F6 for quick access to generators", classes="tip")
    
    def on_mount(self) -> None:
        """Called when screen is mounted."""
        self.log("HomeScreen mounted - updating recent history")
        self.log(f"Container size: {self.size}")
        self.update_recent_history()
    
    def on_quick_action_card_clicked(self, message: QuickActionCard.Clicked) -> None:
        """Handle quick action card click."""
        # This will be handled by the parent app
        pass
    
    def update_recent_history(self) -> None:
        """Update the recent history display."""
        recent_container = self.query_one("#recent-history")
        recent_container.remove_children()
        
        recent_entries = self.history_manager.get_recent(5)
        self.log(f"Recent entries count: {len(recent_entries)}")
        
        if not recent_entries:
            self.log("No recent entries - showing placeholder")
            recent_container.mount(Static("No recent generations yet.", classes="recent-item"))
        else:
            self.log(f"Mounting {len(recent_entries)} recent entries")
            for entry in recent_entries:
                time_str = self.history_manager.format_timestamp(entry.timestamp)
                results_str = self.history_manager.format_results(entry)
                text = f"• {results_str} ({entry.gen_type.title()}, {time_str})"
                self.log(f"Adding entry: {text}")
                recent_container.mount(Static(text, classes="recent-item"))
