import kivy
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.lang import Builder      # using this no need of having main class same as kivy
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.widget import Widget
from kivy.properties import StringProperty

# transitioning from kivy to kivymd
from kivymd.app import MDApp
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.scrollview import ScrollView
from kivymd.uix.gridlayout import MDGridLayout

# giving main window size similiar to a phone screen
Window.size= (320,500)

class MDScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class ResultDisp(Screen):
    pass

class ProfileScoller(ScrollView):
    pass

sm = ScreenManager()
sm.add_widget(MainScreen(name='main'))
sm.add_widget(ResultDisp(name='result'))

class OgImageCard():
    pass

class FilterImageCard():
    pass

class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        # self.theme_cls.primary_palette = "BlueGray"

if __name__ == "__main__":
    MyApp().run()