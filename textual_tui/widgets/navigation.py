"""Navigation sidebar widget."""

from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Button, Static
from textual.message import Message


class Navigation(Container):
    """Navigation sidebar with menu items."""
    
    DEFAULT_CSS = """
    Navigation {
        width: 22;
        dock: left;
        background: $panel;
        border-right: tall $primary;
        padding: 1;
    }
    
    Navigation Button {
        width: 100%;
        margin-bottom: 1;
        background: transparent;
        border: none;
        text-align: left;
        color: $text;
    }
    
    Navigation Button:hover {
        background: $primary-darken-1;
    }
    
    Navigation Button.-active {
        background: $primary;
        text-style: bold;
    }
    
    Navigation .separator {
        height: 1;
        margin: 1 0;
        border-bottom: solid $primary;
    }
    """
    
    class MenuSelected(Message):
        """Message sent when a menu item is selected."""
        
        def __init__(self, menu_id: str) -> None:
            self.menu_id = menu_id
            super().__init__()
    
    def __init__(self) -> None:
        super().__init__(id="navigation")
        self.active_menu = "home"
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Button("🏠 Home", id="menu-home", classes="-active")
        yield Button("🎲 Numbers", id="menu-number")
        yield Button("📊 Floats", id="menu-float")
        yield Button("🎨 Colors", id="menu-color")
        yield Button("📝 Strings", id="menu-string")
        yield Button("⚙️  Custom", id="menu-custom")
        yield Button("📋 List", id="menu-list")
        yield Static("", classes="separator")
        yield Button("📜 History", id="menu-history")
        yield Button("❓ Help", id="menu-help")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        button_id = event.button.id
        if button_id and button_id.startswith("menu-"):
            menu_id = button_id.replace("menu-", "")
            self.set_active(menu_id)
            self.post_message(self.MenuSelected(menu_id))
    
    def set_active(self, menu_id: str) -> None:
        """Set the active menu item."""
        self.active_menu = menu_id
        
        # Update button styles
        for button in self.query(Button):
            if button.id == f"menu-{menu_id}":
                button.add_class("-active")
            else:
                button.remove_class("-active")
