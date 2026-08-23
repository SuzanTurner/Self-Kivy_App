from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.metrics import dp


class CreatePostScreen(BoxLayout):

    def __init__(self, api, on_post_created, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(15),
            **kwargs
        )

        self.api = api
        self.on_post_created = on_post_created
        self.selected_file = None

        # -------------------------
        # HEADER
        # -------------------------

        self.add_widget(
            Label(
                text="Create",
                font_size=dp(28),
                bold=True,
                size_hint_y=None,
                height=dp(60)
            )
        )

        # -------------------------
        # PREVIEW
        # -------------------------

        self.preview = Image(
            size_hint=(1, 0.65),
            allow_stretch=True,
            keep_ratio=True
        )

        self.add_widget(self.preview)

        # -------------------------
        # STATUS
        # -------------------------

        self.status = Label(
            text="Choose a photo",
            size_hint_y=None,
            height=dp(40)
        )

        self.add_widget(self.status)

        # -------------------------
        # CHOOSE PHOTO
        # -------------------------

        choose_button = Button(
            text="Choose Photo",
            size_hint_y=None,
            height=dp(55)
        )

        choose_button.bind(
            on_press=self.open_file_picker
        )

        self.add_widget(choose_button)

        # -------------------------
        # UPLOAD
        # -------------------------

        upload_button = Button(
            text="Upload",
            size_hint_y=None,
            height=dp(55)
        )

        upload_button.bind(
            on_press=self.upload_image
        )

        self.add_widget(upload_button)

    # -------------------------
    # FILE PICKER
    # -------------------------

    def open_file_picker(self, *args):

        chooser = FileChooserListView(
            filters=[
                "*.png",
                "*.jpg",
                "*.jpeg",
                "*.webp"
            ],
            path=".",
        )

        buttons = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10)
        )

        cancel_button = Button(
            text="Cancel"
        )

        select_button = Button(
            text="Select"
        )

        buttons.add_widget(cancel_button)
        buttons.add_widget(select_button)

        layout = BoxLayout(
            orientation="vertical"
        )

        layout.add_widget(chooser)
        layout.add_widget(buttons)

        popup = Popup(
            title="Choose Photo",
            content=layout,
            size_hint=(0.9, 0.9)
        )

        cancel_button.bind(
            on_press=popup.dismiss
        )

        select_button.bind(
            on_press=lambda instance: self.select_file(
                chooser,
                popup
            )
        )

        popup.open()

    # -------------------------
    # SELECT FILE
    # -------------------------

    def select_file(self, chooser, popup):

        if not chooser.selection:
            self.status.text = "Select a photo first."
            return

        self.selected_file = chooser.selection[0]

        self.preview.source = self.selected_file
        self.preview.reload()

        self.status.text = "Photo selected."

        popup.dismiss()

    # -------------------------
    # UPLOAD
    # -------------------------

    def upload_image(self, *args):

        if not self.selected_file:
            self.status.text = "Choose a photo first."
            return

        self.status.text = "Uploading..."

        success, data = self.api.upload_post(
            self.selected_file
        )

        if success:
            self.status.text = "Uploaded!"

            self.on_post_created()

        else:
            self.status.text = str(
                data.get(
                    "detail",
                    "Upload failed."
                )
            )