from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.lang.builder import Builder
from kivy.properties import ListProperty, NumericProperty, StringProperty, ColorProperty
from kivy.core.window import Window

Builder.load_file("gui/panels/browse.kv")
class BrowsePanel(BoxLayout):

    FUNCTIONS = {}
    song_items = ListProperty([])
    col_items = ListProperty([])
    song_query = StringProperty('')
    col_query = StringProperty('')

    def on_song_query(self, instance, query):
        self.song_query = query
        song_ids = []
        for song_id, in self.FUNCTIONS['db_get_songs']('id', query):
            song_ids.append(song_id)
        self.song_items = (Item(self.FUNCTIONS, song_id, 'song') for song_id in song_ids)
        self.update()

    def on_col_query(self, instance, query):
        self.col_query = query
        col_ids = []
        for col_id, in self.FUNCTIONS['db_get_col']('id', query):
            col_ids.append(col_id)
        self.col_items = (Item(self.FUNCTIONS, col_id, 'collection') for col_id in col_ids)
        self.update()

    def update(self):
        container = self.ids.item_container
        container.clear_widgets()
        for item in self.song_items + self.col_items:
            container.add_widget(item)

    def on_click_song(self, db_id):
        pass

    def on_click_col(self, db_id):
        pass

    def bind_on_click_song(self, bind=None):
        if bind is None:
            for song in self.song_items:
                song.on_click = song.on_click_default
        else:
            for song in self.song_items:
                song.on_click = bind

    def bind_on_click_col(self, bind=None):
        if bind is None:
            for song in self.song_items:
                song.on_click = song.on_click_default
        else:
            for song in self.song_items:
                song.on_click = bind

    def __init__(self, **kwargs):
        super(BrowsePanel, self).__init__(**kwargs)


class Item(AnchorLayout):
    FUNCTIONS = {}
    text = StringProperty()
    media_path = StringProperty('')
    color = ColorProperty((1, 1, 1))
    rad = NumericProperty(0)

    def get_name(self):
        name = ''
        if self.type == 'collection':
            name, = self.FUNCTIONS['db_get_col']('name', 'id={}'.format(self.db_id))[0]
        elif self.type == 'song':
            name, = self.FUNCTIONS['db_get_songs']('name', 'id={}'.format(self.db_id))[0]
        return name

    def get_media(self):
        media = ''
        if self.type == 'collection':
            media, = self.FUNCTIONS['db_get_col']('media_path', 'id={}'.format(self.db_id))[0]
        return media

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return
        pos = args[1]
        if self.hovered != self.collide_point(*self.to_widget(*pos)):
            self.set_hovered(not self.hovered)

    def set_hovered(self, hovered):
        self.hovered = hovered
        if self.hovered:
            self.text = self.get_name()
            self.color = (0.922, 0.812, 0.204)
            self.media_path = ''
        else:
            if self.type == 'song':
                self.text = self.get_name()
                self.color = (0.922, 0.812, 0.204)
            elif self.type == 'collection':
                self.text = ''
                self.color = (1, 1, 1)
            self.media_path = self.get_media()

    def on_click_default(self):
        if self.type == 'collection':
            self.FUNCTIONS['gui_select_collection'](self.db_id)
        elif self.type == 'song':
            self.FUNCTIONS['gui_select_song'](self.db_id)

    def on_click(self, db_id):
        self.on_click_default()

    def __init__(self, FUNCTIONS={}, db_id=-1, type='', **kwargs):
        self.FUNCTIONS = FUNCTIONS
        self.db_id = db_id
        self.hovered = False
        self.type = type
        self.media_path = self.get_media()
        if type == 'collection':
            self.rad = 30
        elif type == 'song':
            self.rad = 100
        super(Item, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos)
        self.set_hovered(False)
