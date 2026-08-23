from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class LoginScreen(BoxLayout):

    def __init__(self, api, on_login_success, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=40,
            spacing=15,
            **kwargs
        )

        self.api = api
        self.on_login_success = on_login_success

        self.add_widget(
            Label(
                text="SELF",
                font_size=40
            )
        )

        self.username = TextInput(
            hint_text="Username",
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.password = TextInput(
            hint_text="Password",
            password=True,
            multiline=False,
            size_hint_y=None,
            height=50
        )

        self.login_button = Button(
            text="Login",
            size_hint_y=None,
            height=50
        )

        self.status = Label(
            text="",
            size_hint_y=None,
            height=40
        )

        self.login_button.bind(
            on_press=self.login
        )

        self.add_widget(self.username)
        self.add_widget(self.password)
        self.add_widget(self.login_button)
        self.add_widget(self.status)

    def login(self, instance):
        username = self.username.text.strip()
        password = self.password.text

        if not username or not password:
            self.status.text = "Enter username and password."
            return

        self.status.text = "Logging in..."

        success, data = self.api.login(
            username,
            password
        )

        if success:
            self.status.text = ""
            self.on_login_success()
        else:
            self.status.text = str(
                data.get("detail", "Login failed.")
            )