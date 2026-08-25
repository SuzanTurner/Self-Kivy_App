from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp


class UserCard(ButtonBehavior, BoxLayout):

    def __init__(self, user, **kwargs):
        super().__init__(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(75),
            spacing=dp(12),
            padding=dp(10),
            **kwargs
        )

        self.user = user

        # -------------------------
        # PROFILE PICTURE
        # -------------------------

        profile_picture = user.get("profile_picture")

        if profile_picture:
            picture = AsyncImage(
                source=profile_picture,
                size_hint=(None, None),
                size=(dp(55), dp(55)),
                fit_mode="cover"
            )
        else:
            picture = Label(
                text="○",
                font_size=dp(35),
                size_hint=(None, None),
                size=(dp(55), dp(55))
            )

        self.add_widget(picture)

        # -------------------------
        # USER INFORMATION
        # -------------------------

        info = BoxLayout(
            orientation="vertical"
        )

        username = Label(
            text=user["username"],
            font_size=dp(18),
            bold=True,
            halign="left",
            valign="middle"
        )

        username.bind(
            size=lambda instance, value:
            setattr(instance, "text_size", value)
        )

        info.add_widget(username)

        bio = user.get("bio", "")

        if bio:
            bio_label = Label(
                text=bio,
                font_size=dp(13),
                halign="left",
                valign="middle"
            )

            bio_label.bind(
                size=lambda instance, value:
                setattr(instance, "text_size", value)
            )

            info.add_widget(bio_label)

        self.add_widget(info)