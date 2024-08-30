# file_picker.py
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
#from kivy.uix.label import Label
from Utils.converter import convert_single_word_to_pdf
import os


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
        selected_file = self.filechooser.selection and self.filechooser.selection[0]
        doc_title = os.path.splitext(selected_file)[0]
        try:
            if os.path.splitext(selected_file)[1] == 'docx' or 'doc':
                convert_single_word_to_pdf(selected_file, f"{doc_title}.pdf")
                self.dismiss()
                if self.file_selected_callback:
                    self.file_selected_callback(selected_file)
        except:
            print("\n Ensure You Select A Word Document")


# Function to show the file picker popup
'''
def show_file_picker(file_selected_callback):
    popup = FilePickerPopup(file_selected_callback)
    popup.open()
'''
