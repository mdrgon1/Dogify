from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.lang.builder import Builder
from kivy.properties import StringProperty


Builder.load_file("gui/panels/playbar.kv")
class PlayBarPanel(AnchorLayout):
    FUNCTIONS: dict = {}
    _playpause_button = None

    def update(self):
        audio_state = self.FUNCTIONS['audio_get_state']()
        mode = 'pause' if audio_state['playing'] else 'play'
        self.set_playpause(mode)

    def set_playpause(self, mode):
        idx = self.children.index(self._playpause_button)
        self.remove_widget(self._playpause_button)
        if mode == 'play':
            self._playpause_button = PlayButton()
        elif mode == 'pause':
            self._playpause_button = PauseButton()
        self.add_widget(self._playpause_button, idx)

    def __init__(self, **kwargs):
        super(PlayBarPanel, self).__init__(**kwargs)
        self._playpause_button = PlayButton()
        self.add_widget(self._playpause_button)


class PlayButton(Button):
    def on_press(self):
        self.parent.FUNCTIONS['echo']("PLAY")
        self.parent.FUNCTIONS['audio_play']()
        self.parent.set_playpause('pause')


class PauseButton(Button):
    def on_press(self):
        self.parent.FUNCTIONS['echo']("PAUSE")
        self.parent.FUNCTIONS['audio_pause']()
        self.parent.set_playpause('play')
