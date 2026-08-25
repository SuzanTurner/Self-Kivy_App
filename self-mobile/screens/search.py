from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

from widgets.user_card import UserCard


class SearchScreen(BoxLayout):

    def __init__(
        self,
        api,
        on_profile_click=None,
        **kwargs
    ):
        super().__init__(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10),
            **kwargs
        )

        self.api = api
        self.on_profile_click = on_profile_click

        # -------------------------
        # SEARCH BAR
        # -------------------------

        search_row = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10)
        )

        self.search_input = TextInput(
            hint_text="Search people...",
            multiline=False
        )

        search_button = Button(
            text="Search",
            size_hint_x=None,
            width=dp(100)
        )

        search_button.bind(
            on_press=self.search
        )

        self.search_input.bind(
            on_text_validate=self.search
        )

        search_row.add_widget(
            self.search_input
        )

        search_row.add_widget(
            search_button
        )

        self.add_widget(search_row)

        # -------------------------
        # RESULTS
        # -------------------------

        scroll = ScrollView()

        self.results = BoxLayout(
            orientation="vertical",
            spacing=dp(5),
            size_hint_y=None
        )

        self.results.bind(
            minimum_height=self.results.setter("height")
        )

        scroll.add_widget(self.results)

        self.add_widget(scroll)

    # -------------------------
    # SEARCH
    # -------------------------

    def search(self, *args):

        query = self.search_input.text.strip()

        self.results.clear_widgets()

        if not query:
            self.results.add_widget(
                Label(
                    text="Enter a username.",
                    size_hint_y=None,
                    height=dp(50)
                )
            )
            return

        success, data = self.api.search_users(query)

        if not success:
            self.results.add_widget(
                Label(
                    text=f"Error: {data}",
                    size_hint_y=None,
                    height=dp(50)
                )
            )
            return

        if not data:
            self.results.add_widget(
                Label(
                    text="No users found.",
                    size_hint_y=None,
                    height=dp(50)
                )
            )
            return

        for user in data:
            self.add_user_result(user)

    # -------------------------
    # USER RESULT
    # -------------------------

    def add_user_result(self, user):

        card = UserCard(user)

        card.bind(
            on_press=lambda instance:
            self.open_profile(
                user["username"]
            )
        )

        self.results.add_widget(card)

    # -------------------------
    # OPEN PROFILE
    # -------------------------

    def open_profile(self, username):

        if self.on_profile_click:
            self.on_profile_click(
                username
            )