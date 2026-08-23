from kivy.uix.image import AsyncImage
from kivy.metrics import dp


class PostThumbnail(AsyncImage):

    def __init__(self, post, **kwargs):
        super().__init__(
            source=post["image"],
            size_hint=(None, None),
            width=dp(110),
            height=dp(110),
            fit_mode="cover",
            **kwargs
        )

        self.post = post