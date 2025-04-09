# screens/home.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.properties import ListProperty, NumericProperty
from utils.tmdb import fetch_movies  # Function to fetch movie data

class MovieCard(BoxLayout):
    """A widget to display a single movie card with poster, title, and overview."""
    def __init__(self, movie_data, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)
        self.movie_data = movie_data

        # Movie Poster
        self.poster = AsyncImage(
            source=f"https://image.tmdb.org/t/p/w500{movie_data.get('poster_path', '')}",
            size_hint=(1, 0.7),
            allow_stretch=True,
            keep_ratio=True,
            error_image="assets/placeholder.png"  # Show placeholder on error
        )

        # Movie Title
        self.title = Label(
            text=movie_data.get('title', 'No Title'),
            bold=True,
            size_hint=(1, 0.15),
            halign='center',
            valign='middle',
            text_size=(self.width, None)
        )

        # Movie Overview (shortened)
        overview = movie_data.get('overview', 'No overview available')
        self.overview = Label(
            text=overview[:100] + '...' if len(overview) > 100 else overview,
            size_hint=(1, 0.15),
            font_size='12sp',
            halign='left',
            valign='top',
            text_size=(self.width, None)
        )

        self.add_widget(self.poster)
        self.add_widget(self.title)
        self.add_widget(self.overview)

class HomeScreen(Screen):
    """The screen where users can swipe through movie suggestions."""
    movies = ListProperty([])  # List to store fetched movies
    current_movie_index = NumericProperty(-1) # Index of the currently displayed movie

    def on_enter(self):
        """Called when this screen is displayed."""
        if not self.movies:
            self.load_movies()
        elif self.current_movie_index < 0 and self.movies:
            self.show_current_movie() # Show the first movie if not already shown

    def load_movies(self):
        """Fetches movies from the API and initializes the display."""
        fetched_movies = fetch_movies()
        if fetched_movies:
            self.movies = fetched_movies
            self.current_movie_index = 0
            self.show_current_movie()
        else:
            print("Error: Could not load movies for the home screen.")
            # Optionally display an error message to the user

    def show_current_movie(self):
        """Displays the movie at the current_movie_index in the card container."""
        card_container = self.ids.card_container
        card_container.clear_widgets()
        if 0 <= self.current_movie_index < len(self.movies):
            movie = self.movies[self.current_movie_index]
            card = MovieCard(movie_data=movie)
            card_container.add_widget(card)
        elif self.movies:
            # If index is out of bounds but we have movies, maybe reset or show a "no more movies" message
            label = Label(text="No more movies to swipe!", halign='center', valign='middle')
            card_container.add_widget(label)
        else:
            label = Label(text="Loading movies...", halign='center', valign='middle')
            card_container.add_widget(label)

    def next_movie(self):
        """Moves to the next movie in the list."""
        if self.movies:
            self.current_movie_index += 1
            self.show_current_movie()

    def swipe_right(self):
        """Handles the 'like' action."""
        print(f"Liked: {self.movies[self.current_movie_index].get('title') if 0 <= self.current_movie_index < len(self.movies) else 'No movie'}")
        # TODO: Implement logic to record the liked movie for the user
        self.next_movie()

    def swipe_left(self):
        """Handles the 'dislike' action."""
        print(f"Disliked: {self.movies[self.current_movie_index].get('title') if 0 <= self.current_movie_index < len(self.movies) else 'No movie'}")
        # TODO: Implement logic to record the disliked movie for the user
        self.next_movie()

    def go_to_history(self):
        """Navigates to the history screen."""
        self.manager.current = "history"

    def go_to_favorites(self):
        """Placeholder for navigating to the favorites screen."""
        print("Navigating to Favorites (Not implemented yet)")
        # TODO: Implement navigation to the favorites screen

    def go_to_following(self):
        """Placeholder for navigating to the following screen."""
        print("Navigating to Following (Not implemented yet)")
        # TODO: Implement navigation to the following screen