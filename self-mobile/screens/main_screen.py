from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp


class MainScreen(BoxLayout):

    def __init__(self, api, **kwargs):
        super().__init__(
            orientation="vertical",
            **kwargs
        )

        self.api = api

        # Main content area
        self.content = BoxLayout()

        self.add_widget(self.content)

        # Bottom navigation
        navigation = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(60)
        )

        self.home_button = Button(
            text="Home"
        )

        self.search_button = Button(
            text="Search"
        )

        self.create_button = Button(
            text="+"
        )

        self.life_button = Button(
            text="Life"
        )

        self.profile_button = Button(
            text="Me"
        )

        navigation.add_widget(self.home_button)
        navigation.add_widget(self.search_button)
        navigation.add_widget(self.create_button)
        navigation.add_widget(self.life_button)
        navigation.add_widget(self.profile_button)

        self.add_widget(navigation)

        # Navigation events
        self.home_button.bind(
            on_press=self.show_home
        )

        self.search_button.bind(
            on_press=self.show_search
        )

        self.create_button.bind(
            on_press=self.show_create
        )

        self.life_button.bind(
            on_press=self.show_life
        )

        self.profile_button.bind(
            on_press=self.show_my_profile
        )

        self.show_home()

    # -------------------------
    # HOME
    # -------------------------

    def show_home(self, *args):
        from screens.home import HomeScreen

        self.content.clear_widgets()
        self.content.add_widget(
    HomeScreen(
        api=self.api,
        on_profile_click=self.show_profile
    )
)

    # -------------------------
    # SEARCH
    # -------------------------
    def show_search(self, *args):
        from screens.search import SearchScreen

        self.content.clear_widgets()

        self.content.add_widget(
            SearchScreen(
                api=self.api,
                on_profile_click=self.show_profile
            )
        )

    # -------------------------
    # CREATE
    # -------------------------

    def show_create(self, *args):
        from screens.create_post import CreatePostScreen

        self.content.clear_widgets()

        self.content.add_widget(
            CreatePostScreen(
                api=self.api,
                on_post_created=self.show_home
            )
        )

    # -------------------------
    # LIFE
    # -------------------------

    def show_life(self, *args):
        self.content.clear_widgets()

        self.content.add_widget(
            Label(
                text="Life",
                font_size=dp(30)
            )
        )
 
    # -------------------------
    # MY PROFILE
    # -------------------------

    def show_my_profile(self, *args):
        from screens.profile import ProfileScreen

        self.content.clear_widgets()

        self.content.add_widget(
            ProfileScreen(
                api=self.api
            )
        )


    # -------------------------
    # OTHER USER PROFILE
    # -------------------------

    def show_profile(self, username=None, *args):
        from screens.profile import ProfileScreen

        if not username:
            return

        self.content.clear_widgets()

        self.content.add_widget(
            ProfileScreen(
                api=self.api,
                username=username
            )
        )