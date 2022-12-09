from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.layout import Layout
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

#root = Builder.load_file('./gui/gui.kv')


FUNCTIONS = {
    "print": print,
    "gui_set_main_panel": None,
    "gui_set_secondary_panel": None,
    "gui_set_view" : None,
    "gui_open_modal": None,
    "gui_close_modal": None,
}

Builder.load_file("./gui/panel1.kv")
class panel1(BoxLayout):
    global FUNCTIONS

    def switch(self):
        FUNCTIONS["gui_set_view"](2, 'panel2', 'panel2')

    def close(self):
        FUNCTIONS["gui_close_modal"]()


Builder.load_file("./gui/panel2.kv")
class panel2(BoxLayout):
    global FUNCTIONS

    def switch(self):
        FUNCTIONS["gui_open_modal"]('panel1')


Builder.load_file("./gui/panel3.kv")
class panel3(BoxLayout):
    global FUNCTIONS

    def open(self):
        FUNCTIONS.open_modal('panel1')


PANELS_MAP = {
    'panel1': panel1,
    'panel2': panel2
}


class PlayBarPanel(BoxLayout):
    def __init__(self, **kwargs):
        super(PlayBarPanel, self).__init__(**kwargs)
        self.size_hint = (1, None)
        self.height = '35mm'
        self.add_widget(Label(text='play bar'))


class SearchBarPanel(BoxLayout):
    def __init__(self, **kwargs):
        super(SearchBarPanel, self).__init__(**kwargs)
        self.size_hint = (1, None)
        self.height = '20mm'
        self.anchor_x = 'center'
        self.anchor_y = 'center'
        self.add_widget(TextInput(size_hint=(None, 1), width='100mm', text='search bar', multiline=False))


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

        self.orientation = 'vertical'
        box1 = BoxLayout(orientation='horizontal')
        box2 = BoxLayout(orientation='vertical')
        box2.add_widget(SearchBarPanel())
        box2.add_widget(self._mainPanel)
        box1.add_widget(box2)
        if(self._secondaryPanel):
            box1.add_widget(self._secondaryPanel, self._secondaryPanelIdx)
        self.add_widget(box1)
        self.add_widget(PlayBarPanel())


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

    def open_modal(self, panel_n: str):
        if self._modal:
            raise Exception("attempting to open modal when one already exists")
        self._modal = Popup(auto_dismiss=False)
        self._modal.add_widget(PANELS_MAP[panel_n]())
        self._modal.open()

    def close_modal(self):
        if self._modal:
            self._modal.dismiss()
            self._modal = None

    def set_view(self, view_num: int, main_panel_n:str, secondary_panel_n:str=None):
        for child in self.children:
            self.remove_widget(child)
        match view_num:
            case 0:
                self.add_widget(View0Layout(
                    PANELS_MAP[main_panel_n]()
                ))
            case 1:
                if secondary_panel_n is None:
                    raise Exception("must provide secondary panel for view1")
                self.add_widget(View1Layout(
                    PANELS_MAP[main_panel_n](),
                    PANELS_MAP[secondary_panel_n]()
                ))
            case 2:
                if secondary_panel_n is None:
                    raise Exception("must provide secondary panel for view2")
                self.add_widget(View2Layout(
                    PANELS_MAP[main_panel_n](),
                    PANELS_MAP[secondary_panel_n]()
                ))


    def __init__(self, **kwargs):
        super(RootLayout, self).__init__(**kwargs)
        self.add_widget(
            View0Layout(
                panel1()
            )
        )
        self._modal = None
        FUNCTIONS["gui_set_view"] = self.set_view
        FUNCTIONS["gui_open_modal"] = self.open_modal
        FUNCTIONS["gui_close_modal"] = self.close_modal


class Gui(App):
    def build(self):
        return RootLayout()


if __name__ == '__main__':
    Gui().run()
