from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image


def top_bar(self):
        layout = BoxLayout(orientation='vertical')

        # Create a custom title bar (you can style this further)
        title_bar = BoxLayout(size_hint_y=None, height=48)
        icon = Image(source="logo1.jpeg", size_hint_x=None, width=48)
        search_bar = TextInput(hint_text='Search', size_hint_x=None, width=200)

        title_bar.add_widget(icon)
        title_bar.add_widget(search_bar)

        layout.add_widget(title_bar)
        return layout
