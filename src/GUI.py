from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from gui.panels.playbar import PlayBarPanel
from gui.panels.searchbar import SearchBarPanel
from gui.panels.collection import CollectionPanel
from gui.panels.song import SongPanel
from gui.panels.browse import BrowsePanel
from gui.panels.newsong import NewSongModal
from gui.panels.newcol import NewColModal

Builder.load_file("./gui/panel1.kv")
class panel1(BoxLayout):
    global FUNCTIONS

    def switch(self):
        FUNCTIONS["gui_update_panel"]('playbar')

    def close(self):
        FUNCTIONS["gui_close_modal"]()


Builder.load_file("./gui/panel2.kv")
class panel2(BoxLayout):
    global FUNCTIONS

    def switch(self):
        FUNCTIONS["echo"]('YUH')


Builder.load_file("./gui/panel3.kv")
class panel3(BoxLayout):
    global FUNCTIONS

    def open(self):
        FUNCTIONS.open_modal('panel1')


PANELS_MAP = {
    'panel1': panel1(),
    'panel2': panel2(),
    'playbar': PlayBarPanel(),
    'searchbar': SearchBarPanel(),
    'collection': CollectionPanel(),
    'song': SongPanel(),
    'browse': BrowsePanel(),
    'searchresults': BrowsePanel(),
    'newsong': NewSongModal(),
    'newcol': NewColModal(),
}


class ViewLayout(BoxLayout):
    _mainPanel = None
    _secondaryPanel = None
    _secondaryPanelIdx = None

    def getMainPanel(self):
        return self._mainPanel

    def setMainPanel(self, panel):
        parent = self._mainPanel.parent
        if self._mainPanel:
            parent.remove_widget(self._mainPanel)
        self._mainPanel = panel()
        parent.add_widget(self._mainPanel)

    def getSecondaryPanel(self):
        return self._secondaryPanel

    def setSecondaryPanel(self, panel):
        parent = self._secondaryPanel.parent
        if self._secondaryPanel:
            parent.remove_widget(self._secondaryPanel)
        self._secondaryPanel = panel()
        parent.add_widget(self._secondaryPanel, self._secondaryPanelIdx)

    mainPanel = property(getMainPanel, setMainPanel)
    secondaryPanel = property(getSecondaryPanel, setSecondaryPanel)


    def __init__(self, **kwargs):
        super(ViewLayout, self).__init__(**kwargs)

        FUNCTIONS["gui_set_main_panel"] = self.setMainPanel
        FUNCTIONS["gui_set_secondary_panel"] = self.setSecondaryPanel

        searchbar = PANELS_MAP['searchbar']
        playbar = PANELS_MAP['playbar']

        self.orientation = 'vertical'
        box1 = BoxLayout(orientation='horizontal')
        box2 = BoxLayout(orientation='vertical', size_hint=(2, 1))
        box2.add_widget(searchbar)
        box2.add_widget(self._mainPanel)
        box1.add_widget(box2)
        if self._secondaryPanel:
            box1.add_widget(self._secondaryPanel, self._secondaryPanelIdx)
        self.add_widget(box1)
        self.add_widget(playbar)


class View0Layout(ViewLayout):

    def getSecondaryPanel(self):
        raise Exception("attempting to get secondary panel in view 1")

    def setSecondaryPanel(self, panel):
        raise Exception("attempting to set secondary panel in view 1")

    def __init__(self, main_panel, **kwargs):
        self._mainPanel = main_panel
        super(View0Layout, self).__init__(**kwargs)


class View1Layout(ViewLayout):
    _secondaryPanelIdx = 0

    def __init__(self, main_panel, secondary_panel, **kwargs):
        self._mainPanel = main_panel
        self._secondaryPanel = secondary_panel
        super(View1Layout, self).__init__(**kwargs)


class View2Layout(ViewLayout):
    _secondaryPanelIdx = 1

    def __init__(self, main_panel, secondary_panel, **kwargs):
        self._mainPanel = main_panel
        self._secondaryPanel = secondary_panel
        super(View2Layout, self).__init__(**kwargs)


class RootLayout(BoxLayout):

    def open_modal(self, panel_n: str, title: str = ''):
        if self._modal:
            self._modal.dismiss()
        content = PANELS_MAP[panel_n]
        if content.parent:
            content.parent.remove_widget(content)
        self._modal = Popup(
            title=title,
            content=content,
            size_hint=(None, None),
            size=(600, 400),
            pos_hint={'top': 0.9},
            background='gui/img/button_dark_hover.png',
            border=(16, 16, 16, 16),
            separator_color=(0.5, 0.5, 0.5, 1.0))
        self._modal.open()

    def close_modal(self):
        if self._modal:
            self._modal.dismiss()
            self._modal = None

    def set_view(self, view_num: int, main_panel_n: str, secondary_panel_n: str =None):
        for panel in PANELS_MAP.values():
            if panel.parent:
                panel.parent.remove_widget(panel)
        if self.children:
            self.remove_widget(self.children[0])
        match view_num:
            case 0:
                self.add_widget(View0Layout(
                    PANELS_MAP[main_panel_n]
                ))
            case 1:
                if secondary_panel_n is None:
                    raise Exception("must provide secondary panel for view1")
                self.add_widget(View1Layout(
                    PANELS_MAP[main_panel_n],
                    PANELS_MAP[secondary_panel_n]
                ))
            case 2:
                if secondary_panel_n is None:
                    raise Exception("must provide secondary panel for view2")
                self.add_widget(View2Layout(
                    PANELS_MAP[main_panel_n],
                    PANELS_MAP[secondary_panel_n]
                ))


    def __init__(self, **kwargs):
        super(RootLayout, self).__init__(**kwargs)
        self._modal = None
        FUNCTIONS["gui_set_view"] = self.set_view
        FUNCTIONS["gui_open_modal"] = self.open_modal
        FUNCTIONS["gui_close_modal"] = self.close_modal


root = None
class Gui(App):
    def build(self):
        return root


def init():

    global root
    root = RootLayout()

    FUNCTIONS['audio_play_new'](3)
    FUNCTIONS['audio_pause']()
#    select_song(3)
    PANELS_MAP['browse'].update()

    FUNCTIONS['gui_set_view'](0, 'browse')

    Gui().run()


def select_collection(db_id):
    PANELS_MAP['collection'].set_db_id(db_id)
    FUNCTIONS['gui_update_panel']('collection')
    FUNCTIONS['gui_set_view'](2, 'browse', 'collection')


def select_song(db_id):
    PANELS_MAP['song'].set_db_id(db_id)
    FUNCTIONS['gui_update_panel']('song')
    FUNCTIONS['gui_set_view'](1, 'browse', 'song')


def update_panel(panel_str):
    PANELS_MAP[panel_str].update()


def bind_results_callback(song=None, col=None):
    if song:
        PANELS_MAP['searchresults'].bind_on_click_song(song)
    if col:
        PANELS_MAP['searchresults'].bind_on_click_col(col)


FUNCTIONS = {
    "gui_set_main_panel": None,
    "gui_set_secondary_panel": None,
    "gui_set_view" : None,
    "gui_open_modal": None,
    "gui_close_modal": None,
    "gui_update_panel": update_panel,
    "gui_init": init,
    "gui_select_collection": select_collection,
    "gui_select_song": select_song,
    "gui_bind_results_callback": bind_results_callback
}


def link_functions(fun_map):
    global FUNCTIONS
    FUNCTIONS = fun_map
    for value in PANELS_MAP.values():
        type(value).FUNCTIONS = fun_map


CLI_FUNCTIONS = {}


if __name__ == '__main__':
    init()