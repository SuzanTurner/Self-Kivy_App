from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

from widgets.post_thumbnail import PostThumbnail


class ProfileScreen(BoxLayout):

    def __init__(self, api, username=None, **kwargs):
        super().__init__(
            orientation="vertical",
            **kwargs
        )

        self.api = api
        self.username = username

        self.load_profile()

    def load_profile(self):

        if self.username:
            success, data = self.api.get_profile(
                self.username
        )
        else:
            success, data = self.api.get_my_profile()

        if not success:
            self.add_widget(
                Label(
                    text=f"Error: {data}"
                )
            )
            return

        # -------------------------
        # SCROLLABLE PROFILE
        # -------------------------

        scroll = ScrollView()

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(15),
            size_hint_y=None
        )

        content.bind(
            minimum_height=content.setter("height")
        )

        # -------------------------
        # PROFILE PICTURE
        # -------------------------

        profile_picture = data.get(
            "profile_picture"
        )

        if profile_picture:
            picture = AsyncImage(
                source=profile_picture,
                size_hint_y=None,
                height=dp(140),
                fit_mode="contain"
            )
        else:
            picture = Label(
                text="No profile picture",
                size_hint_y=None,
                height=dp(140)
            )

        content.add_widget(picture)

        # -------------------------
        # USERNAME
        # -------------------------

        content.add_widget(
            Label(
                text=data["username"],
                font_size=dp(25),
                bold=True,
                size_hint_y=None,
                height=dp(45)
            )
        )

        # -------------------------
        # BIO
        # -------------------------

        bio = data.get("bio", "")

        if bio:
            content.add_widget(
                Label(
                    text=bio,
                    size_hint_y=None,
                    height=dp(50)
                )
            )

        # -------------------------
        # POST COUNT
        # -------------------------

        content.add_widget(
            Label(
                text=f"{data['post_count']} posts",
                size_hint_y=None,
                height=dp(40)
            )
        )

        # -------------------------
        # POSTS
        # -------------------------

        content.add_widget(
            Label(
                text="Posts",
                font_size=dp(20),
                bold=True,
                size_hint_y=None,
                height=dp(40)
            )
        )

        posts = data.get("posts", [])

        if not posts:

            content.add_widget(
                Label(
                    text="No posts yet.",
                    size_hint_y=None,
                    height=dp(50)
                )
            )

        else:

            grid = GridLayout(
                cols=3,
                spacing=dp(5),
                size_hint_y=None
            )

            # Three columns of 110px thumbnails.
            rows = (len(posts) + 2) // 3

            grid.height = (
                rows * dp(110) +
                max(0, rows - 1) * dp(5)
            )

            for post in posts:
                grid.add_widget(
                    PostThumbnail(post)
                )

            content.add_widget(grid)

        scroll.add_widget(content)

        self.add_widget(scroll)