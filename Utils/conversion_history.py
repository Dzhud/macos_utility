import os
import json
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button

def show_conversion_history(right_pane, history_file="conversion_history.json"):

    # right_pane.clear_widgets()  # Clear any existing widgets in the right pane

    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            history = json.load(f)

        scroll_view = ScrollView(size_hint=(1, 1))
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=10)
        layout.bind(minimum_height=layout.setter('height'))

        for record in history:
            # Create a card-like layout for each record
            card = BoxLayout(orientation='horizontal', size_hint_y=None, height=120, padding=10)
            card_background = BoxLayout(size_hint=(None, None), size=(80, 80), pos_hint={'center_y': 0.5})
            
            # Add an icon to the left
            # icon = Image(source='static/logo2.jpeg', size_hint=(None, None), size=(60, 60))  # Placeholder for document icon
            icon = Image(source='atlas://data/images/defaulttheme/filechooser_file', size_hint=(None, None), size=(60, 60))
            card_background.add_widget(icon)
            
            # Text details
            text_layout = BoxLayout(orientation='vertical', padding=(10, 0), spacing=5)
            
            source_label = Label(
                text=f"[b]Source:[/b] {os.path.basename(record['source_file'])}",
                markup=True, size_hint_y=None, height=30, font_size='14sp', color=(0, 0, 0, 1)
            )
            output_label = Label(
                text=f"[b]Output:[/b] {os.path.basename(record['output_file'])}",
                markup=True, size_hint_y=None, height=30, font_size='14sp', color=(1, 0.65, 0, 1)
            )
            directory_label = Label(
                text=f"[b]Directory:[/b] {record['directory']}",
                markup=True, size_hint_y=None, height=30, font_size='14sp', color=(0.3, 0.3, 0.3, 1)
            )
            timestamp_label = Label(
                text=f"[b]Date:[/b] {record['timestamp']}",
                markup=True, size_hint_y=None, height=30, font_size='14sp', color=(0.5, 0.5, 0.5, 1)
            )
            
            text_layout.add_widget(source_label)
            text_layout.add_widget(output_label)
            text_layout.add_widget(directory_label)
            text_layout.add_widget(timestamp_label)
            
            card.add_widget(card_background)
            card.add_widget(text_layout)
            
            # Optional: Add a button to open the file or perform actions
            action_button = Button(
                text="Open",
                size_hint=(None, None),
                size=(80, 40),
                pos_hint={'center_y': 0.5},
                on_press=lambda x, file=record['output_file']: open_file(file)
            )
            card.add_widget(action_button)
            
            # Add shadow effect or rounded corners (use a Kivy canvas if you want more customization)
            card.canvas.before.clear()
            with card.canvas.before:
                from kivy.graphics import Color, RoundedRectangle
                Color(0.9, 0.9, 0.9, 1)
                RoundedRectangle(size=card.size, pos=card.pos, radius=[10])
            
            layout.add_widget(card)

        scroll_view.add_widget(layout)
        right_pane.add_widget(scroll_view)
    else:
        right_pane.add_widget(Label(text="No conversion history available"))


def open_file(filepath):
    """Opens the file. This function should be customized to handle different file types."""
    import subprocess
    try:
        subprocess.Popen(['open', filepath])  # For macOS, replace with 'xdg-open' for Linux or 'start' for Windows
    except Exception as e:
        print(f"Error opening file: {e}")