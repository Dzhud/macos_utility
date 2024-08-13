import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'

        # Left pane (settings)
        left_pane = BoxLayout(orientation='vertical', spacing=0, size_hint_x=None, width=200)
        settings_button = Button(text='Settings')
        settings_button.bind(on_press=self.on_settings_click)
        left_pane.add_widget(settings_button)
        # Add more buttons for other options
        # Left pane (utilities)
        utilities_button = Button(text='Utilities')
        utilities_button.bind(on_press=self.on_utilities_click)
        left_pane.add_widget(utilities_button)
        # Right pane (content)
        right_pane = BoxLayout(orientation='vertical')

        # Initial content
        right_pane.add_widget(Label(text='Welcome'))

        self.add_widget(left_pane)
        self.add_widget(right_pane)

        self.right_pane = right_pane
        self.current_option = None

    def on_settings_click(self, instance):
        self.current_option = 'settings'
        self.update_right_pane()

    def on_utilities_click(self, instance):
        self.current_option = 'utilities'
        self.update_right_pane()

    def update_right_pane(self):
        self.right_pane.clear_widgets()
        if self.current_option == 'settings':
            # Add settings content to the right pane
            settings_label = Label(text='Settings content')
            self.right_pane.add_widget(settings_label)
        # Add other options and their content here
        if self.current_option == 'utilities':
            utilities_label = Label(text='Utilities content')
            self.right_pane.add_widget(utilities_label)


class MyApp(App):
    def build(self):
        return MyBoxLayout()

if __name__ == '__main__':
    MyApp().run()
