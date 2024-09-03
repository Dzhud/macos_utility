from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from Utils.converter import convert_single_word_to_pdf
from Utils.error_pop import ErrorPopup
from Utils.progress_bar_widget import ProgressBarPopup
from kivy.clock import Clock
import os, json
from datetime import datetime



class FilePickerPopup(Popup):
    last_directory_file = "last_directory.json"  # To store Last Directory
    history_file = "conversion_history.json"  # File to save conversion history


    def __init__(self, file_selected_callback, **kwargs):
        super().__init__(**kwargs)
        self.title = "Select a File"
        self.size_hint = (0.9, 0.9)
        self.file_selected_callback = file_selected_callback

        layout = BoxLayout(orientation='vertical')
        # Use the last directory if it exists, otherwise default to root
        ##initial_directory = FilePickerPopup.last_directory or "/"
        initial_directory = self.load_last_directory() or "/"

        # Initialize the FileChooserListView with the last used directory or default to root
        self.filechooser = FileChooserListView(path=initial_directory)
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
             # Save the directory of the selected file
            self.save_last_directory(os.path.dirname(selected_file))

            progress_popup = ProgressBarPopup()
            progress_popup.open()
            # Simulate the conversion process
            def simulate_conversion(*args):
                if progress_popup.progress_bar.value >= progress_popup.progress_bar.max:
                    progress_popup.stop()
                    return False
                progress_popup.update_progress(progress_popup.progress_bar.value + 10)
            
            Clock.schedule_interval(simulate_conversion, 0.5)


            # Removes selected file's extension and assigns to `doc_title`
            file_extension = os.path.splitext(selected_file)[1].lower()
            doc_title = os.path.splitext(selected_file)[0]

            if file_extension in ['.docx', '.doc']:
                convert_single_word_to_pdf(selected_file, f"{doc_title}.pdf")
                # Save conversion details to history
                self.save_conversion_history(selected_file, f"{doc_title}.pdf")

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
        # Save the last directory to a file.
        try:
            with open(self.last_directory_file, 'w') as f:
                json.dump({'last_directory': directory}, f)
        except IOError as e:
            print(f"Error saving last directory: {str(e)}")

    def load_last_directory(self):
        # Load the last directory from a file.
        try:
            if os.path.exists(self.last_directory_file):
                with open(self.last_directory_file, 'r') as f:
                    data = json.load(f)
                    print(f"Loaded directory: {data.get('last_directory')}")
                    return data.get('last_directory')
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading last directory: {str(e)}")
        return None
    
    def save_conversion_history(self, source_file, output_file):
        # Save conversion details to the history file.
        conversion_record = {
            'source_file': source_file,
            'output_file': output_file,
            'directory': os.path.dirname(output_file),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        try:
            history = []
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    history = json.load(f)
            
            history.append(conversion_record)

            with open(self.history_file, 'w') as f:
                json.dump(history, f, indent=4)
        except IOError as e:
            print(f"Error saving conversion history: {str(e)}")

# Function to show the file picker popup
'''
def show_file_picker(file_selected_callback):
    popup = FilePickerPopup(file_selected_callback)
    popup.open()
'''
