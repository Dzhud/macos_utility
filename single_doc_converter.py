''''
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class SingleDocConverterLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'

upper_pane = BoxLayout(orientation='vertical', spacing=0, size_hint_x=None, width=200)
single_doc_convtr_button = Button(text='Convert Single Doc')
'''
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup

kivy.require('2.1.0')  # replace with your kivy version

class FileChooserScreen(Screen):
    file_chooser = ObjectProperty(None)
    file_path = StringProperty(None)
    default_dir = StringProperty('./')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.file_chooser = FileChooserIconView()
        self.file_chooser.size_hint = (0.8, 0.8)
        self.file_chooser.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.file_chooser.bind(selection=self.selected)

        load_button = Button(text='Load', size_hint=(0.2, 0.1), pos_hint={'x': 0.8, 'y': 0.1})
        load_button.bind(on_press=self.load_file)

        file_path_label = Label(text='No file selected', size_hint=(0.8, 0.1), pos_hint={'center_x': 0.5, 'y': 0.1})
        self.file_path_label = file_path_label

        set_default_dir_button = Button(text='Set Default Directory', size_hint=(0.2, 0.1), pos_hint={'x': 0.2, 'y': 0.1})
        set_default_dir_button.bind(on_press=self.set_default_dir)

        navigation_bar = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        home_button = Button(text='Home', size_hint_x=0.2)
        navigation_bar.add_widget(home_button)

        self.add_widget(navigation_bar)
        self.add_widget(self.file_chooser)
        self.add_widget(load_button)
        self.add_widget(file_path_label)
        self.add_widget(set_default_dir_button)

    def load_file(self, instance):
        if self.file_chooser.selection:
            self.file_path = self.file_chooser.selection[0]
            self.file_path_label.text = self.file_path
            # Add your logic to process the selected file here
            print(f"Selected file: {self.file_path}")
        else:
            print("No file selected")

    def selected(self, filechooser, selection):
        if selection:
            path = selection[0]
            print(f"Selected: {path}")

    def set_default_dir(self, instance):
        content = FileChooserIconView()
        content.bind(on_success=self.set_default_directory)
        popup = Popup(title='Select Default Directory', content=content, size_hint=(0.9, 0.9))
        popup.open()

    def set_default_directory(self, instance, selection):
        if selection:
            self.default_dir = selection[0]
            self.file_chooser.path = self.default_dir
            instance.parent.parent.dismiss()  # Close the popup

class MainScreen(Screen):
    pass  # Define your main screen content here

class ScreenManagerApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FileChooserScreen(name='file_chooser'))
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    ScreenManagerApp().run()