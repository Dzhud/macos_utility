# file_picker.py
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from Utils.converter import convert_single_word_to_pdf
from Utils.error_pop import ErrorPopup
import os, json


class FilePickerPopup(Popup):
    last_directory_file = "last_directory.json"  # To store Last Directory

    def __init__(self, file_selected_callback, **kwargs):
        super().__init__(**kwargs)
        self.title = "Select a File"
        self.size_hint = (0.9, 0.9)
        self.file_selected_callback = file_selected_callback

        layout = BoxLayout(orientation='vertical')
        # Use the last directory if it exists, otherwise default to root
        ##initial_directory = FilePickerPopup.last_directory or "/"
        initial_directory = self.load_last_directory() or "/"


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
            # Update the last_directory with the directory of the selected file
            ##FilePickerPopup.last_directory = os.path.dirname(selected_file)
             # Save the directory of the selected file
            self.save_last_directory(os.path.dirname(selected_file))

            # Removes selected file's extension and assigns to `doc_title`
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

    def save_last_directory(self, directory):
        """Save the last directory to a file."""
        try:
            with open(self.last_directory_file, 'w') as f:
                json.dump({'last_directory': directory}, f)
        except IOError as e:
            print(f"Error saving last directory: {str(e)}")

    def load_last_directory(self):
        """Load the last directory from a file."""
        try:
            if os.path.exists(self.last_directory_file):
                with open(self.last_directory_file, 'r') as f:
                    data = json.load(f)
                    print(f"Loaded directory: {data.get('last_directory')}")
                    return data.get('last_directory')
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading last directory: {str(e)}")
        return None

# Function to show the file picker popup
'''
def show_file_picker(file_selected_callback):
    popup = FilePickerPopup(file_selected_callback)
    popup.open()
'''
