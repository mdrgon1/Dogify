from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.properties import StringProperty
import re

Builder.load_file("gui/panels/newcol.kv")
class NewColModal(BoxLayout):

    FUNCTIONS = {}

    media_filepath = StringProperty('')
    name = StringProperty('')

    def browse_files(self):
        dialog_output = self.FUNCTIONS['open_filedialog']()
        if dialog_output:
            self.media_filepath = dialog_output
        if self.name == '' and dialog_output != '':
            self.name = re.findall('[^/\\\\]{4,}', dialog_output)[-1]
            self.name = re.sub('\\..{3}$', '', self.name)

    def on_name(self, instance, value):
        self.name = value

    def on_media_filepath(self, instance, value):
        self.media_filepath = value

    def submit(self):
        self.FUNCTIONS['db_create_col'](self.name, self.media_filepath)
        self.FUNCTIONS['gui_update_panel']('browse')
        self.FUNCTIONS['gui_close_modal']()

    def __init__(self, **kwargs):
        super(NewColModal, self).__init__(**kwargs)
        self.ids.media_filepath_input.bind(text=self.on_media_filepath)
        self.ids.name_input.bind(text=self.on_name)