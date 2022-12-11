from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder


Builder.load_file("gui/panels/searchbar.kv")
class SearchBarPanel(BoxLayout):
    FUNCTIONS: dict
