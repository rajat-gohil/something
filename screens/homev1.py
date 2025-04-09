
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from utils.tmdb import fetch_movies

def update_movie(self):
    if self.index >= len(shared_movie_list):
        self.poster.source = ""
        self.title_label.text = "No more movies!"
        self.description_label.text = ""
        return

    movie = shared_movie_list[self.index]
    self.poster.source = movie["poster"]
    self.title_label.text = movie["title"]
    self.description_label.text = movie["overview"]

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        tab_layout = BoxLayout(size_hint=(1, 0.1))
        tab_layout.add_widget(Button(text="❤️ Favorites"))
        tab_layout.add_widget(Button(text="📜 History", on_press=self.go_to_history))
        tab_layout.add_widget(Button(text="🧍 Following"))
        layout.add_widget(tab_layout)
        layout.add_widget(Image(source="assets/images/placeholder.png", size_hint=(1, 0.6)))
        buttons = BoxLayout(size_hint=(1, 0.2))
        buttons.add_widget(Button(text="💔", font_size=40))
        buttons.add_widget(Button(text="❤️", font_size=40))
        layout.add_widget(buttons)
        self.add_widget(layout)
        self.poster = AsyncImage(size_hint=(1, 0.6))
        self.title_label = Label(size_hint=(1, 0.1), font_size='18sp')
        self.description_label = Label(size_hint=(1, 0.3), font_size='14sp')

    def go_to_history(self, instance):
        self.manager.current = "history"
