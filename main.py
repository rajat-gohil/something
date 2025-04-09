# main.py
import sys
print(sys.executable)
print(sys.path)
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.lang import Builder
from kivy.clock import Clock
import requests  # Ensure requests is imported if not already

# Load all KV files for UI layouts
Builder.load_file("kv/signup.kv")
Builder.load_file("kv/home.kv")
Builder.load_file("kv/history.kv")

# Import the Python logic for each screen
from screens.signup import SignupScreen
from screens.home import HomeScreen
from screens.history import HistoryScreen
from utils.tmdb import fetch_movies  # Function to fetch movie data

# Mapping of TMDB genre IDs to names
GENRE_MAP = {
    28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy",
    80: "Crime", 99: "Documentary", 18: "Drama", 10751: "Family",
    14: "Fantasy", 36: "History", 27: "Horror", 10402: "Music",
    9648: "Mystery", 10749: "Romance", 878: "Sci-Fi", 10770: "TV",
    53: "Thriller", 10752: "War", 37: "Western"
}

def get_genre_names(genre_ids):
    """Converts a list of genre IDs into a list of human-readable genre names."""
    return [GENRE_MAP.get(gid, "Unknown") for gid in genre_ids]

class FlickApp(App):
    """The main application class for the Flick movie matching app."""

    # --- 1. Theme Management ---
    theme = StringProperty("light")  # Current UI theme: 'light' or 'dark'

    # Color properties that update based on the current theme
    background_color = ListProperty()
    text_color = ListProperty()
    subtext_color = ListProperty()
    button_color = ListProperty()
    button_text_color = ListProperty()
    liked_color = ListProperty()
    disliked_color = ListProperty()
    input_bg_color = ListProperty()
    input_text_color = ListProperty()
    card_bg_color = ListProperty()
    tab_bg_color = ListProperty()
    tab_text_color = ListProperty()

    def update_theme_colors(self):
        """Sets the app's color properties based on the current theme."""
        if self.theme == "dark":
            self.background_color = [0.1, 0.1, 0.1, 1]
            self.text_color = [1, 1, 1, 1]
            self.subtext_color = [0.7, 0.7, 0.7, 1]
            self.button_color = [0.3, 0.3, 0.8, 1]
            self.button_text_color = [1, 1, 1, 1]
            self.input_bg_color = [0.2, 0.2, 0.2, 1]
            self.input_text_color = [1, 1, 1, 1]
            self.card_bg_color = [0.15, 0.15, 0.15, 1]
            self.tab_bg_color = [0.25, 0.25, 0.25, 1]
            self.tab_text_color = [1, 1, 1, 1]
            self.liked_color = [0.2, 0.9, 0.2, 1]
            self.disliked_color = [0.9, 0.2, 0.2, 1]
        else:  # Light theme (default)
            self.background_color = [1, 1, 1, 1]
            self.text_color = [0, 0, 0, 1]
            self.subtext_color = [0.4, 0.4, 0.4, 1]
            self.button_color = [0.2, 0.6, 0.86, 1]
            self.button_text_color = [1, 1, 1, 1]
            self.input_bg_color = [0.95, 0.95, 0.95, 1]
            self.input_text_color = [0, 0, 0, 1]
            self.card_bg_color = [0.98, 0.98, 0.98, 1]
            self.tab_bg_color = [0.9, 0.9, 0.9, 1]
            self.tab_text_color = [0, 0, 0, 1]
            self.liked_color = [0.0, 0.8, 0.2, 1]
            self.disliked_color = [0.9, 0.1, 0.1, 1]

    def toggle_theme(self):
        """Switches the app's theme between light and dark."""
        self.theme = "dark" if self.theme == "light" else "light"
        self.update_theme_colors()

    # --- 2. Screen Management ---
    def build(self):
        """Initializes the application and sets up the screen manager."""
        self.title = 'Flick'
        self.icon = 'assets/icon.png'

        self.update_theme_colors()  # Set the initial theme colors

        self.sm = ScreenManager(transition=FadeTransition())
        self.sm.add_widget(SignupScreen(name="signup"))
        self.sm.add_widget(HomeScreen(name="home"))
        self.sm.add_widget(HistoryScreen(name="history"))
        return self.sm

    # --- 3. Movie Display Logic ---
    movies = ListProperty([])  # Stores the list of movies fetched from the API
    movie_index = NumericProperty(0)  # Keeps track of the index of the movie currently displayed

    def on_start(self):
        """Called after the application has been initialized."""
        Clock.schedule_once(self.load_initial_movies, 1)

    def load_initial_movies(self, dt):
        """Fetches the initial list of movies from the TMDB API."""
        movies = fetch_movies()  # Calls the function from utils/tmdb.py
        if movies:
            self.movies = movies
            self.movie_index = 0
            self.show_next_movie()
        else:
            print("Error: Failed to load initial movies.")
            # Optionally display an error message to the user on the UI

    def show_next_movie(self):
        """Displays the movie at the current index on the home screen."""
        home_screen = self.sm.get_screen("home")
        if home_screen:
            if self.movies and self.movie_index < len(self.movies):
                movie = self.movies[self.movie_index]
                home_screen.ids.movie_title.text = movie.get("title", "No Title")
                home_screen.ids.genre.text = " | ".join(get_genre_names(movie.get("genre_ids", [])))
                poster_path = movie.get("poster_path")
                if poster_path:
                    home_screen.ids.poster_img.source = f"https://image.tmdb.org/t/p/w500{poster_path}"
                else:
                    home_screen.ids.poster_img.source = "assets/placeholder.png"  # Fallback image
                self.movie_index += 1
            else:
                home_screen.ids.movie_title.text = "No more movies to show!"
                home_screen.ids.genre.text = ""
                home_screen.ids.poster_img.source = "assets/placeholder.png"

    # --- 4. User Interaction: Swiping ---
    def swipe_right(self):
        """Handles the 'like' action when the user swipes right."""
        print("Liked!")
        # TODO: Implement logic to record the liked movie for the current user
        # This will likely involve storing user preferences and potentially checking for matches.
        self.show_next_movie()

    def swipe_left(self):
        """Handles the 'dislike' action when the user swipes left."""
        print("Disliked!")
        # TODO: Implement logic to record the disliked movie for the current user.
        self.show_next_movie()

    # --- 5. Tab Switching (Home Screen) ---
    def switch_tab(self, tab_name):
        """Handles the switching of tabs on the home screen."""
        print(f"Switched to tab: {tab_name}")
        if tab_name == "history":
            self.sm.current = "history"
        elif tab_name == "favorites":
            # TODO: Implement logic to display favorite movies
            pass
        elif tab_name == "following":
            # TODO: Implement logic to display followed users/their activity
            pass
        # By default, stay on the main movie swiping view
        elif tab_name == "main":
            pass # Potentially reload movies or reset view

if __name__ == "__main__":
    FlickApp().run()