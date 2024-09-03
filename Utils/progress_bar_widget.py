from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.clock import Clock

class ProgressBarPopup(Popup):
    def __init__(self, max_value=100, **kwargs):
        super().__init__(**kwargs)
        self.progress_bar = ProgressBar(max=max_value)
        self.content = self.progress_bar
        self.title = "Converting File(s)..."
        self.size_hint = (0.5, 0.2)
    
    def update_progress(self, value):
        self.progress_bar.value = value

    def start(self, update_interval=0.1):
        self.progress_bar.value = 0
        Clock.schedule_interval(self._progress_update, update_interval)

    def _progress_update(self, dt):
        if self.progress_bar.value >= self.progress_bar.max:
            Clock.unschedule(self._progress_update)
            self.dismiss()  # Close the popup when the progress reaches the max
        else:
            self.progress_bar.value += 1  # Increment by 1 for demonstration

    def stop(self):
        Clock.unschedule(self._progress_update)
        self.dismiss()
