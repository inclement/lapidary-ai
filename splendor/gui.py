
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
    colour = StringProperty('white')
    bg_colour = ListProperty([0, 0, 0, 1])
    border_colour = ListProperty([0, 0, 0, 1])
    hide_zeros = BooleanProperty(False)
    hidden = BooleanProperty(False)

    padding = NumericProperty(0)

class CardsDisplay(AnchorLayout):
    cards = ListProperty([])
    label = StringProperty('')

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

class GemsDisplay(AnchorLayout):
    white = NumericProperty(0)
    blue = NumericProperty(0)
    green = NumericProperty(0)
    red = NumericProperty(0)
    black = NumericProperty(0)
    gold = NumericProperty(0)

class PlayerDisplay(AnchorLayout):
    white = NumericProperty(0)
    blue = NumericProperty(0)
    green = NumericProperty(0)
    red = NumericProperty(0)
    black = NumericProperty(0)
    gold = NumericProperty(0)

    white_played = NumericProperty(0)
    blue_played = NumericProperty(0)
    green_played = NumericProperty(0)
    red_played = NumericProperty(0)
    black_played = NumericProperty(0)
    gold_played = NumericProperty(0)

    player = ObjectProperty(None)
    name = StringProperty('player')

    def update_player_info(self):
        if self.player is None:
            return
        for colour in colours + ['gold']:
            setattr(self, colour, player.num_gems(colour))

class GameScreen(Screen):
    num_players = NumericProperty(2)
    validate = BooleanProperty(False)

    tier_1_cards = ListProperty([])
    tier_2_cards = ListProperty([])
    tier_3_cards = ListProperty([])

    supply_white = NumericProperty(0)
    supply_blue = NumericProperty(0)
    supply_green = NumericProperty(0)
    supply_red = NumericProperty(0)
    supply_black = NumericProperty(0)
    supply_gold = NumericProperty(0)

    p1_white = NumericProperty(0)
    p1_blue = NumericProperty(0)
    p1_green = NumericProperty(0)
    p1_red = NumericProperty(0)
    p1_black = NumericProperty(0)
    p1_gold = NumericProperty(0)

    p2_white = NumericProperty(0)
    p2_blue = NumericProperty(0)
    p2_green = NumericProperty(0)
    p2_red = NumericProperty(0)
    p2_black = NumericProperty(0)
    p2_gold = NumericProperty(0)

    player_types = ListProperty(['player:1', 'player:2']) #H50AI_TDlam(restore=True, prob_factor=20, num_players=2)])
    current_player_index = NumericProperty(0)

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

        for colour in colours + ['gold']:
            setattr(self, 'supply_' + colour, self.state.num_gems_available(colour))

        for i, player in enumerate(self.state.players):
            setattr(self, 'p{}_{}'.format(i + 1, colour), player.num_gems(colour))

class MenuScreen(Screen):
    pass

class GameGuiApp(App):
    def build(self):
        Window.clearcolor = (0.945, 0.945, 0.831, 1)
        return Root()


if __name__ == "__main__":
    GameGuiApp().run()
