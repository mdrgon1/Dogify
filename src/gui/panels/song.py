from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.lang.builder import Builder
from kivy.properties import ListProperty, NumericProperty, StringProperty, ColorProperty
from kivy.core.window import Window

Builder.load_file("gui/panels/song.kv")
class SongPanel(BoxLayout):

    FUNCTIONS = {}
    collections = ListProperty([])
    db_id = NumericProperty(-1)
    name = StringProperty('')

    def on_collections(self, instance, value):
        col_container = self.ids.song_container
        col_container.clear_widgets()
        for collection_wid in value:
            col_container.add_widget(collection_wid)

    def set_db_id(self, db_id):
        self.db_id = db_id
        ids = []
        for col_id, song_ids in self.FUNCTIONS['db_get_col']('id, song_ids', '*'):
            if self.db_id in song_ids:
                ids.append(col_id)
        self.collections = [Collection(self.FUNCTIONS, col_id) for col_id in ids]

    def get_name(self):
        name, = self.FUNCTIONS['db_get_songs']('name', 'id={}'.format(self.db_id))[0]
        return name

    def update(self):
        self.set_db_id(self.db_id)
        self.name = self.get_name()

    def __init__(self, **kwargs):
        super(SongPanel, self).__init__(**kwargs)


class Collection(AnchorLayout):
    FUNCTIONS = {}
    text = StringProperty('')
    media_path = StringProperty('')
    color = ColorProperty((1, 1, 1))

    def get_name(self):
        name, = self.FUNCTIONS['db_get_col']('name', 'id={}'.format(self.db_id))[0]
        return name

    def get_media(self):
        media, = self.FUNCTIONS['db_get_col']('media_path', 'id={}'.format(self.db_id))[0]
        return media

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return
        pos = args[1]
        if self.hovered != self.collide_point(*self.to_widget(*pos)):
            self.hovered = not self.hovered
            if self.hovered:
                self.text = self.get_name()
                self.color = (0.922, 0.812, 0.204)
                self.media_path = ''
            else:
                self.text = ''
                self.color = (1, 1, 1)
                self.media_path = self.get_media()

    def on_click(self):
        self.FUNCTIONS['gui_select_collection'](self.db_id)

    def __init__(self, FUNCTIONS, db_id, **kwargs):
        self.FUNCTIONS = FUNCTIONS
        self.db_id = db_id
        self.hovered = False
        self.media_path = self.get_media()
        super(Collection, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos)
