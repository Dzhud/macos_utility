# file_picker.py
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from Utils.converter import convert_single_word_to_pdf
import os


class ErrorPopup(Popup):
    def __init__(self, message, **kwargs):
        super().__init__(**kwargs)
        self.title = "Error"
        self.size_hint = (0.7, 0.3)

        layout = BoxLayout(orientation='vertical', padding=10)

        label = Label(text=message)
        close_button = Button(text="Close", size_hint_y=None, height=40)
        close_button.bind(on_press=self.dismiss)

        layout.add_widget(label)
        layout.add_widget(close_button)

        self.content = layout


class FilePickerPopup(Popup):
    def __init__(self, file_selected_callback, **kwargs):
        super().__init__(**kwargs)
        self.title = "Select a File"
        self.size_hint = (0.9, 0.9)
        self.file_selected_callback = file_selected_callback

        layout = BoxLayout(orientation='vertical')

        self.filechooser = FileChooserListView()
        layout.add_widget(self.filechooser)

        buttons_layout = BoxLayout(size_hint_y=0.1)

        select_button = Button(text="Select", on_press=self.on_select)
        cancel_button = Button(text="Cancel", on_press=self.dismiss)
        buttons_layout.add_widget(select_button)
        buttons_layout.add_widget(cancel_button)

        layout.add_widget(buttons_layout)

        self.content = layout

    def on_select(self, instance):
        try:
            selected_file = self.filechooser.selection and self.filechooser.selection[0]
            if not selected_file:
                raise ValueError("No file selected")

            file_extension = os.path.splitext(selected_file)[1].lower()
            doc_title = os.path.splitext(selected_file)[0]

            if file_extension in ['.docx', '.doc']:
                convert_single_word_to_pdf(selected_file, f"{doc_title}.pdf")
                self.dismiss()
                if self.file_selected_callback:
                    self.file_selected_callback(selected_file)
            else:
                raise ValueError("Selected file is not a Word document")

        except ValueError as e:
            self.show_error_popup(str(e))

    def show_error_popup(self, message):
        popup = ErrorPopup(message)
        popup.open()

# Function to show the file picker popup
'''
def show_file_picker(file_selected_callback):
    popup = FilePickerPopup(file_selected_callback)
    popup.open()
'''
