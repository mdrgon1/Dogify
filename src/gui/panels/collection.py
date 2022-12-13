from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.lang.builder import Builder
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.core.window import Window

Builder.load_file("gui/panels/collection.kv")
class CollectionPanel(BoxLayout):

    FUNCTIONS = {}
    songs = ListProperty([])
    db_id = NumericProperty(0)
    media = StringProperty("")

    def on_songs(self, instance, value):
        song_container = self.ids.song_container
        song_container.clear_widgets()
        for song in value:
            song_container.add_widget(song)

    def add_song(self, song_id):
        self.songs.append(Song(self.FUNCTIONS, song_id))

    def remove_song(self):
        self.songs.pop()

    def set_db_id(self, db_id):
        self.db_id = db_id
        ids = [song_id for song_id in self.FUNCTIONS['db_get_songs_in_col'](db_id, 'id', '*')]
        self.songs = [Song(self.FUNCTIONS, song_id) for song_id in ids]
        self.media, = self.FUNCTIONS['db_get_col']('media_path', 'id={}'.format(db_id))[0]
        print(self.ids.song_container.children)

    def click_add_song(self):
        self.FUNCTIONS['gui_update_panel']('searchresults')
        self.FUNCTIONS['gui_bind_results_callback'](song=self.add_song)
        self.FUNCTIONS['gui_open_modal']('searchresults')

    def add_song(self, song_id):
        self.FUNCTIONS['db_insert_into_col'](self.db_id, [song_id])
        self.FUNCTIONS['gui_close_modal']()
        self.FUNCTIONS['gui_update_panel']('collection')

    def update(self):
        self.set_db_id(self.db_id)

    def __init__(self, **kwargs):
        super(CollectionPanel, self).__init__(**kwargs)


class Song(AnchorLayout):
    FUNCTIONS = {}

    def get_name(self):
        name, = self.FUNCTIONS['db_get_songs']('name', 'id={}'.format(self.db_id))[0]
        return name

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return
        pos = args[1]
        if self.hovered != self.collide_point(*self.to_widget(*pos)):
            self.hovered = not self.hovered
            button = self.ids.button
            if self.hovered:
                button.background_normal = 'gui/img/button_dark_hover.png'
            else:
                button.background_normal = 'gui/img/button_dark_normal.png'

    def on_play(self):
        self.FUNCTIONS['audio_play_new'](self.db_id)
        self.FUNCTIONS['gui_update_panel']('playbar')

    def __init__(self, FUNCTIONS, db_id, **kwargs):
        self.FUNCTIONS = FUNCTIONS
        self.db_id = db_id
        super(Song, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos)
        self.hovered = False
