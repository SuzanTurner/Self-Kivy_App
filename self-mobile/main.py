from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from services.api import API
from screens.login import LoginScreen
from screens.main_screen import MainScreen


class SelfApp(App):

    def build(self):

        self.api = API()

        self.manager = ScreenManager()

        # -------------------------
        # LOGIN
        # -------------------------

        login_screen = Screen(
            name="login"
        )

        login_screen.add_widget(
            LoginScreen(
                api=self.api,
                on_login_success=self.show_main
            )
        )

        self.manager.add_widget(
            login_screen
        )

        return self.manager

    def show_main(self):

        main_screen = Screen(
            name="main"
        )

        main_screen.add_widget(
            MainScreen(
                api=self.api
            )
        )

        self.manager.add_widget(
            main_screen
        )

        self.manager.current = "main"


if __name__ == "__main__":
    SelfApp().run()