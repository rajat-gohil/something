# screens/signup.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty

class SignupScreen(Screen):
    """The screen for user account creation."""

    email = StringProperty('')  # Property to store the entered email

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # App Title
        layout.add_widget(Label(text="Flick", font_size='32sp'))

        # Create Account Label
        layout.add_widget(Label(text="Create an account", font_size='16sp'))

        # Email Input
        self.email_input = TextInput(hint_text="email@domain.com")
        self.email_input.bind(text=self.on_email_input)
        layout.add_widget(self.email_input)

        # Continue Button (Email Signup)
        continue_button = Button(text="Continue", on_press=self.handle_email_signup)
        layout.add_widget(continue_button)

        # Separator
        layout.add_widget(Label(text="or", halign='center'))

        # Google Signup Button
        google_button = Button(text="Continue with Google", on_press=self.handle_google_signup)
        layout.add_widget(google_button)

        # Apple Signup Button
        apple_button = Button(text="Continue with Apple", on_press=self.handle_apple_signup)
        layout.add_widget(apple_button)

        self.add_widget(layout)

    def on_email_input(self, instance, value):
        """Updates the email property as the text input changes."""
        self.email = value

    def handle_email_signup(self, instance):
        """Handles the email signup process."""
        email = self.email.strip()
        if email:
            print(f"Attempting signup with email: {email}")
            # TODO: Implement email validation and signup logic
            self.manager.current = "home"  # For now, just navigate to home
        else:
            print("Please enter an email address.")
            # TODO: Display an error message to the user

    def handle_google_signup(self, instance):
        """Handles the Google signup process."""
        print("Initiating Google signup...")
        # TODO: Implement Google Sign-In integration
        self.manager.current = "home"  # For now, just navigate to home

    def handle_apple_signup(self, instance):
        """Handles the Apple signup process."""
        print("Initiating Apple signup...")
        # TODO: Implement Apple Sign-In integration
        self.manager.current = "home"  # For now, just navigate to home