# screens/history.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ListProperty
import kivy.utils
dp = kivy.utils.dp # Import the dp function

class HistoryScreen(Screen):
    """The screen displaying the user's movie history and ratings."""

    history_items = ListProperty([])  # List to store history data (will be populated later)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scroll_view = ScrollView()
        self.history_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=dp(10))
        self.history_layout.bind(minimum_height=self.history_layout.setter('height'))
        self.scroll_view.add_widget(self.history_layout)

        main_layout = BoxLayout(orientation='vertical')
        main_layout.add_widget(self.scroll_view)

        home_button = Button(text="🏠 Home", size_hint=(1, 0.1))
        home_button.bind(on_press=self.go_home)
        main_layout.add_widget(home_button)

        self.add_widget(main_layout)

        # For initial testing, populate with dummy data
        self.populate_dummy_history()

    def populate_dummy_history(self):
        """Populates the history screen with dummy data for testing."""
        for i in range(10):
            movie_data = {
                'title': f"Movie Name {i+1}",
                'description': f"Description of movie {i+1}",
                'rating': '⭐⭐⭐⭐⭐',
                'poster': "assets/images/placeholder.png"
            }
            self.history_items.append(movie_data)
        self.update_history_display()

    def update_history_display(self):
        """Updates the history layout with the current history items."""
        self.history_layout.clear_widgets()
        for item in self.history_items:
            row = BoxLayout(size_hint_y=None, height=dp(100), spacing=dp(10))
            row.add_widget(Image(source=item['poster'], size_hint_x=0.3))
            details_column = BoxLayout(orientation='vertical', size_hint_x=0.7)
            details_column.add_widget(Label(text=item['title'], bold=True, font_size='16sp', halign='left'))
            details_column.add_widget(Label(text=item['description'], font_size='12sp', halign='left', valign='top', text_size=(self.width * 0.7, None)))
            details_column.add_widget(Label(text=item['rating'], font_size='14sp', halign='left'))
            row.add_widget(details_column)
            self.history_layout.add_widget(row)

    def go_home(self, instance):
        """Navigates back to the home screen."""
        self.manager.current = 'home'

    # TODO: Implement logic to load actual history data
    def load_history(self):
        """Loads the user's movie history from storage (e.g., database, local file)."""
        print("Loading movie history...")
        # Replace the dummy data population with actual data loading
        # self.history_items = ... (load data here)
        # self.update_history_display()
        pass