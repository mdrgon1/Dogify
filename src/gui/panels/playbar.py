from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.lang.builder import Builder


class PlayButton(Button):
    def on_press(self):
        self.parent.FUNCTIONS['echo']("PLAY")
        self.parent.FUNCTIONS['audio_play']()
        self.parent.switch_playpause()


class PauseButton(Button):
    def on_press(self):
        self.parent.FUNCTIONS['echo']("PAUSE")
        self.parent.FUNCTIONS['audio_pause']()
        self.parent.switch_playpause()


Builder.load_file("gui/panels/playbar.kv")
class PlayBarPanel(AnchorLayout):
    FUNCTIONS: dict = {}
    _mode = 'play'
    _playpause_button = None

    def __init__(self, **kwargs):
        super(PlayBarPanel, self).__init__(**kwargs)
        self._playpause_button = PlayButton()
        self.add_widget(self._playpause_button)

    def switch_playpause(self):
        idx = self.children.index(self._playpause_button)
        self.remove_widget(self._playpause_button)
        if self._mode == 'play':
            self._playpause_button = PauseButton()
            self._mode = 'pause'
        elif self._mode == 'pause':
            self._playpause_button = PlayButton()
            self._mode = 'play'
        self.add_widget(self._playpause_button, idx)