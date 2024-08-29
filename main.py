import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from Utils.file_picker import FilePickerPopup
#from Utils.converter import convert_single_word_to_pdf

# Master Widget
class OriginWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Add other widgets or logic here

        # Create and add MyBoxLayout
        my_box_layout = MyBoxLayout()
        self.add_widget(my_box_layout)

class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        
        global file_selected, selection_pos
        file_selected = ""
        selection_pos = ""

        left_pane = BoxLayout(orientation='vertical', spacing=0, size_hint_x=None, width=200)
        # Left pane (single Doc convtr)
        single_doc_convtr_button = Button(text='Convert Single Doc')
        single_doc_convtr_button.bind(on_press=self.on_single_convtr_click)
        left_pane.add_widget(single_doc_convtr_button)
        # Left pane (Mltpl Doc Convtr)
        mltpl_doc_convtr_button = Button(text='Convert Multiple Docs')
        mltpl_doc_convtr_button.bind(on_press=self.on_mltpl_convtr_click)
        left_pane.add_widget(mltpl_doc_convtr_button)
        # Left pane (settings)
        settings_button = Button(text='Settings')
        settings_button.bind(on_press=self.on_settings_click)
        left_pane.add_widget(settings_button)
        # Left pane (utilities)
        utilities_button = Button(text='Utilities')
        utilities_button.bind(on_press=self.on_utilities_click)
        left_pane.add_widget(utilities_button)
        # Left Pane (history)
        history_button = Button(text='History')
        history_button.bind(on_press=self.on_history_click)
        left_pane.add_widget(history_button)
        # Right pane (content)
        right_pane = BoxLayout(orientation='horizontal')

        # Initial Right Pane View
        right_pane.add_widget(Label(text='Welcome', bold=True, italic=True, color=(1, 0.65, 0, 1), markup=True, font_size='40sp'))

        self.add_widget(left_pane)
        self.add_widget(right_pane)

        self.right_pane = right_pane
        self.current_option = None

    def on_single_convtr_click(self, instance):
        self.current_option = 'single'
        self.update_right_pane()

    def on_mltpl_convtr_click(self, instance):
        self.current_option = 'multiple'
        self.update_right_pane()

    def on_settings_click(self, instance):
        self.current_option = 'settings'
        self.update_right_pane()

    def on_utilities_click(self, instance):
        self.current_option = 'utilities'
        self.update_right_pane()

    def on_history_click(self, instance):
        self.current_option = 'history'
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
        if self.current_option == 'single':
            handle_file_selection = lambda selected_file: (
                file_selected := selected_file, 
                print(f"Selected file: {selected_file}\n\t")
                ) if selected_file else None
            single_doc_label = Button(text='Convert Single Doc', color=(1, 0.65, 0, 1), bold=True,
                                      italic=True, font_size='20sp', size_hint=(0.5, 0.10),
                                      pos_hint={'center_x': 0.5, 'center_y': 0.5})
            single_doc_label.bind(on_press=lambda instance: FilePickerPopup(handle_file_selection).open())
            self.right_pane.add_widget(single_doc_label)
            

        if self.current_option == 'multiple':
            mltpl_label = Button(text='Convert Multiple Docs to PDF')
            self.right_pane.add_widget(mltpl_label)

        if self.current_option == 'history':
            hst_label = Button(text='Converted Docs History')
            self.right_pane.add_widget(hst_label)

class MyApp(App):
    title = "USB Halt"
    #icon = "logo1.jpeg"
    #user_data = {'version': '1.0'}

    def build(self):
        return OriginWidget()
    def on_start(self):
        #Add Spinner function/window
        pass
    def on_stop(self):
        #Add "Want to close?" window
        pass


if __name__ == '__main__':
    MyApp().run()
