from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from Utils.converter import convert_single_word_to_pdf
from Utils.error_pop import ErrorPopup
from Utils.progress_bar_widget import ProgressBarPopup
from kivy.clock import Clock
import os, json
from datetime import datetime
from kivy.graphics import Color, Rectangle



class MultiFilePickerPopup(Popup):
    last_directory_file = "last_directory.json"
    history_file = "conversion_history.json"

    def __init__(self, file_selected_callback, **kwargs):
        super().__init__(**kwargs)
        self.title = "Select Files"
        self.size_hint = (0.9, 0.9)
        self.file_selected_callback = file_selected_callback

        layout = BoxLayout(orientation='vertical')
        initial_directory = self.load_last_directory() or "/"
        
        # Enable multi-file selection by setting multiselect=True
        self.filechooser = FileChooserListView(path=initial_directory, multiselect=True)
        layout.add_widget(self.filechooser)

        # FileChooser background color customization (optional)
        with self.filechooser.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Light gray background
            self.bg_rect = Rectangle(size=self.filechooser.size, pos=self.filechooser.pos)

        buttons_layout = BoxLayout(size_hint_y=0.1)
        select_button = Button(text="Select", on_press=self.on_select)
        cancel_button = Button(text="Cancel", on_press=self.dismiss)
        buttons_layout.add_widget(select_button)
        buttons_layout.add_widget(cancel_button)

        layout.add_widget(buttons_layout)
        self.content = layout

    def on_select(self, instance):
        try:
            selected_files = self.filechooser.selection
            if not selected_files:
                raise ValueError("No files selected")
            
            # Save the directory of the selected files
            self.save_last_directory(os.path.dirname(selected_files[0]))

            progress_popup = ProgressBarPopup()
            progress_popup.open()

            # Simulate the conversion process for multiple files
            def simulate_conversion(*args):
                if progress_popup.progress_bar.value >= progress_popup.progress_bar.max:
                    progress_popup.stop()
                    return False
                progress_popup.update_progress(progress_popup.progress_bar.value + 10)

            Clock.schedule_interval(simulate_conversion, 0.5)

            for selected_file in selected_files:
                file_extension = os.path.splitext(selected_file)[1].lower()
                doc_title = os.path.splitext(selected_file)[0]

                if file_extension in ['.docx', '.doc']:
                    convert_single_word_to_pdf(selected_file, f"{doc_title}.pdf")
                    self.save_conversion_history(selected_file, f"{doc_title}.pdf")
                else:
                    progress_popup.stop()
                    raise ValueError(f"{selected_file} is not a Word document")
            
            self.dismiss()
            if self.file_selected_callback:
                self.file_selected_callback(selected_files)

        except ValueError as e:
            self.show_error_popup(str(e))

    def show_error_popup(self, message):
        popup = ErrorPopup(message)
        popup.open()

    def save_last_directory(self, directory):
        # Only save if the last directory is different
        try:
            last_dir = self.load_last_directory()
            if last_dir != directory:
                with open(self.last_directory_file, 'w') as f:
                    json.dump({'last_directory': directory}, f)
        except IOError as e:
            print(f"Error saving last directory: {str(e)}")

    def load_last_directory(self):
        try:
            if os.path.exists(self.last_directory_file):
                with open(self.last_directory_file, 'r') as f:
                    data = json.load(f)
                    return data.get('last_directory')
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading last directory: {str(e)}")
        return None

    def save_conversion_history(self, source_file, output_file):
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
