from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.button import Button
from kivy.metrics import dp


class PostCard(BoxLayout):

    def __init__(self, post, on_profile_click=None, **kwargs):
        super().__init__(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(5),
            padding=dp(10),
            **kwargs
        )

        self.post = post
        self.on_profile_click = on_profile_click

        # -------------------------
        # HEADER
        # ------------------------- 

        header = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(45)
        )

        username = Button(
            text=post["username"],
            font_size=dp(18),
            bold=True,
            size_hint_x=1,
            background_normal="",
            background_color=(0, 0, 0, 0),
        )

        if self.on_profile_click:
            username.bind(
                on_press=lambda instance:
                self.on_profile_click(
                    post["username"]
                )
            )

        header.add_widget(username)

        self.add_widget(header)

        # -------------------------
        # IMAGE
        # -------------------------

        image = AsyncImage(
            source=post["image"],
            size_hint=(1, None),
            height=dp(400),
            fit_mode="contain"
        )

        self.add_widget(image)

        # -------------------------
        # ACTIONS
        # -------------------------

        actions = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(45),
            spacing=dp(5)
        )

        like_button = Button(
            text=(
                "Unlike"
                if post["liked_by_me"]
                else "Like"
            ),
            size_hint_x=None,
            width=dp(100)
        )

        likes = Label(
            text=f"{post['likes']} likes",
            halign="left",
            valign="middle"
        )

        likes.bind(
            size=lambda instance, value:
            setattr(instance, "text_size", value)
        )

        comment_button = Button(
            text="Comment",
            size_hint_x=None,
            width=dp(120)
        )

        actions.add_widget(like_button)
        actions.add_widget(likes)
        actions.add_widget(comment_button)

        self.add_widget(actions)

        # -------------------------
        # CARD HEIGHT
        # -------------------------

        self.height = (
            dp(45) +
            dp(400) +
            dp(45) +
            dp(25)
        )