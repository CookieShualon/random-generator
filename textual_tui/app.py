"""Main Textual TUI application."""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Header, Footer
from textual.binding import Binding
from textual.css.query import NoMatches
from textual.events import Resize

# Import screens and widgets
from textual_tui.widgets.navigation import Navigation
from textual_tui.screens.home import HomeScreen, QuickActionCard
from textual_tui.screens.number_generator import NumberGeneratorScreen
from textual_tui.screens.float_generator import FloatGeneratorScreen
from textual_tui.screens.color_generator import ColorGeneratorScreen
from textual_tui.screens.string_generator import StringGeneratorScreen
from textual_tui.screens.custom_generator import CustomGeneratorScreen
from textual_tui.screens.list_generator import ListGeneratorScreen
from textual_tui.screens.help import HelpScreen
from textual_tui.utils.history_manager import HistoryManager


class TextualTUI(App):
    """Main Textual TUI application for Random Generator."""
    
    CSS_PATH = "styles/theme.tcss"
    
    BINDINGS = [
        Binding("f1", "show_screen('number')", "Numbers", show=True),
        Binding("f2", "show_screen('float')", "Floats", show=False),
        Binding("f3", "show_screen('color')", "Colors", show=False),
        Binding("f4", "show_screen('string')", "Strings", show=False),
        Binding("f5", "show_screen('custom')", "Custom", show=False),
        Binding("f6", "show_screen('list')", "List", show=False),
        Binding("ctrl+h", "show_screen('help')", "Help", show=True),
        Binding("ctrl+r", "show_screen('history')", "History", show=False),
        Binding("ctrl+q", "quit", "Quit", show=True),
    ]
    
    def __init__(self, generator):
        """
        Initialize the TUI app.
        
        Args:
            generator: RandomGenerator instance
        """
        super().__init__()
        self.generator = generator
        self.history_manager = HistoryManager()
        self.current_screen = "home"
        self.title = "Random Value Generator"
        self.sub_title = "Enhanced TUI Mode"
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()
        yield Navigation()
        yield Container(id="content-container")
        yield Footer()
    
    def on_mount(self) -> None:
        """Called when app is mounted."""
        self._update_responsive_classes()
        self.show_home_screen()

    def on_resize(self, event: Resize) -> None:
        """Update responsive classes when terminal is resized."""
        self._update_responsive_classes()

    def _update_responsive_classes(self) -> None:
        """Add/remove CSS classes based on terminal size."""
        width = self.size.width
        if width < 80:
            self.add_class("narrow")
        else:
            self.remove_class("narrow")
    
    def on_navigation_menu_selected(self, message: Navigation.MenuSelected) -> None:
        """Handle navigation menu selection."""
        self.action_show_screen(message.menu_id)
    
    def on_quick_action_card_clicked(self, message: QuickActionCard.Clicked) -> None:
        """Handle quick action card click."""
        self.action_show_screen(message.action_id)
    
    def action_show_screen(self, screen_id: str) -> None:
        """
        Show a specific screen.
        
        Args:
            screen_id: ID of screen to show
        """
        self.current_screen = screen_id
        
        # Update navigation
        nav = self.query_one(Navigation)
        nav.set_active(screen_id)
        
        # Clear current content
        content_container = self.query_one("#content-container")
        content_container.remove_children()
        
        # Mount new screen
        if screen_id == "home":
            self.show_home_screen()
        elif screen_id == "number":
            self.show_number_screen()
        elif screen_id == "float":
            self.show_float_screen()
        elif screen_id == "color":
            self.show_color_screen()
        elif screen_id == "string":
            self.show_string_screen()
        elif screen_id == "custom":
            self.show_custom_screen()
        elif screen_id == "list":
            self.show_list_screen()
        elif screen_id == "history":
            self.show_placeholder_screen("History", "Coming soon!")
        elif screen_id == "help":
            self.show_help_screen()
    
    def show_home_screen(self) -> None:
        """Show the home screen."""
        content_container = self.query_one("#content-container")
        self.log(f"Content container size: {content_container.size}")
        self.log(f"Content container styles: width={content_container.styles.width}, height={content_container.styles.height}")
        content_container.mount(HomeScreen(self.history_manager))
    
    def show_number_screen(self) -> None:
        """Show the number generator screen."""
        content_container = self.query_one("#content-container")
        content_container.mount(NumberGeneratorScreen(self.generator, self.history_manager))
    
    def show_float_screen(self) -> None:
        """Show the float generator screen."""
        content_container = self.query_one("#content-container")
        content_container.mount(FloatGeneratorScreen(self.generator, self.history_manager))
    
    def show_color_screen(self) -> None:
        """Show the color generator screen."""
        content_container = self.query_one("#content-container")
        content_container.mount(ColorGeneratorScreen(self.generator, self.history_manager))
    
    def show_string_screen(self) -> None:
        """Show the string generator screen."""
        content_container = self.query_one("#content-container")
        content_container.mount(StringGeneratorScreen(self.generator, self.history_manager))
    
    def show_custom_screen(self) -> None:
        """Show the custom pattern generator screen."""
        content_container = self.query_one("#content-container")
        content_container.mount(CustomGeneratorScreen(self.generator, self.history_manager))
    
    def show_list_screen(self) -> None:
        """Show the list selection screen."""
        content_container = self.query_one("#content-container")
        content_container.mount(ListGeneratorScreen(self.generator, self.history_manager))
    
    def show_help_screen(self) -> None:
        """Show the help screen."""
        content_container = self.query_one("#content-container")
        content_container.mount(HelpScreen())
    
    def show_placeholder_screen(self, title: str, message: str) -> None:
        """
        Show a placeholder screen for unimplemented features.
        
        Args:
            title: Screen title
            message: Placeholder message
        """
        from textual.widgets import Static
        from textual.containers import Vertical
        
        content_container = self.query_one("#content-container")
        
        # Create widgets first
        title_widget = Static(title)
        title_widget.styles.text_style = "bold"
        title_widget.styles.color = "cyan"
        title_widget.styles.text_align = "center"
        title_widget.styles.margin = (0, 0, 2, 0)
        
        message_widget = Static(message)
        message_widget.styles.text_align = "center"
        message_widget.styles.color = "yellow"
        
        # Create container with widgets
        placeholder = Container(title_widget, message_widget)
        placeholder.styles.padding = (2, 4)
        
        content_container.mount(placeholder)


def run_textual_tui(generator):
    """
    Run the Textual TUI application.
    
    Args:
        generator: RandomGenerator instance
    """
    app = TextualTUI(generator)
    app.run()
