from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

from widgets.postcard import PostCard


class HomeScreen(BoxLayout):

    def __init__(self, api, on_profile_click=None, **kwargs):
        super().__init__(
            orientation="vertical",
            **kwargs
        )

        self.api = api
        
        self.on_profile_click = on_profile_click

        # -------------------------
        # HEADER
        # -------------------------

        header = BoxLayout(
            size_hint_y=None,
            height=dp(60),
            padding=(dp(15), 0)
        )

        title = Label(
            text="SELF",
            font_size=dp(28),
            bold=True
        )

        header.add_widget(title)

        self.add_widget(header)

        # -------------------------
        # FEED
        # -------------------------

        scroll = ScrollView()

        self.feed = BoxLayout(
            orientation="vertical",
            spacing=dp(15),
            padding=dp(10),
            size_hint_y=None
        )

        self.feed.bind(
            minimum_height=self.feed.setter("height")
        )

        scroll.add_widget(self.feed)

        self.add_widget(scroll)

        self.load_feed()

    def load_feed(self):

        success, data = self.api.get_feed()

        if not success:

            self.feed.add_widget(
                Label(
                    text=f"Error: {data}",
                    size_hint_y=None,
                    height=dp(50)
                )
            )

            return

        if not data:

            self.feed.add_widget(
                Label(
                    text="No posts yet.",
                    size_hint_y=None,
                    height=dp(50)
                )
            )

            return

        for post in data:

            self.feed.add_widget(
                PostCard(
    post,
    on_profile_click=self.on_profile_click
)
            )