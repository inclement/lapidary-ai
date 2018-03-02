
from kivy.app import App
from kivy.core.window import Window

from kivy.properties import (NumericProperty, ObjectProperty,
                             BooleanProperty, StringProperty,
                             ListProperty)

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout

from nn import H50AI_TDlam
from game import GameState
from data import colours, colours_dict

class Root(ScreenManager):
    pass

class Card(FloatLayout):
    white = NumericProperty(0)
    blue = NumericProperty(0)
    green = NumericProperty(0)
    red = NumericProperty(0)
    black = NumericProperty(0)

    colour = StringProperty('white')
    colour_list = ListProperty([0, 1, 1, 1])

    points = NumericProperty(0)

class NumberCircle(Label):
    number = NumericProperty(0)
    bg_colour = ListProperty([0, 0, 0, 1])
    border_colour = ListProperty([0, 0, 0, 1])
    hide_zeros = BooleanProperty(False)
    hidden = BooleanProperty(False)

class TierDisplay(AnchorLayout):
    cards = ListProperty([])

    def on_cards(self, instance, value):
        self.ids.boxlayout.clear_widgets()
        for card in self.cards:
            self.ids.boxlayout.add_widget(Card(
                white=card.white,
                blue=card.blue,
                green=card.green,
                red=card.red,
                black=card.black,
                points=card.points,
                colour=card.colour))

class GameScreen(Screen):
    num_players = NumericProperty(2)
    validate = BooleanProperty(False)

    tier_1_cards = ListProperty([])
    tier_2_cards = ListProperty([])
    tier_3_cards = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_game_state()

    def init_game_state(self):
        self.state = GameState(players=self.num_players,
                               init_game=True,
                               validate=self.validate)
        self.sync_with_game_state()

    def sync_with_game_state(self):
        self.tier_1_cards = self.state.cards_in_market(1)
        self.tier_2_cards = self.state.cards_in_market(2)
        self.tier_3_cards = self.state.cards_in_market(3)
    

class MenuScreen(Screen):
    pass

class GameGuiApp(App):
    def build(self):
        Window.clearcolor = (0.945, 0.945, 0.831, 1)
        return Root()


if __name__ == "__main__":
    GameGuiApp().run()
