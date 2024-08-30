from kivy.uix.popup import Popup
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class ErrorPopup(Popup):
    def __init__(self, message, **kwargs):
        super().__init__(**kwargs)
        self.title = "Error"
        self.size_hint = (0.4, 0.3)

        layout = BoxLayout(orientation='vertical', padding=10)

        label = Label(text=message)
        close_button = Button(text="Close", size_hint_y=None, height=40)
        close_button.bind(on_press=self.dismiss)

        layout.add_widget(label)
        layout.add_widget(close_button)

        self.content = layout