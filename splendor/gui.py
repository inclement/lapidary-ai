
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

def format_nobles(nobles):

    output = []
    for noble in nobles:
        colour_outputs = []
        for colour in colours:
            required = noble.num_required(colour)
            if not required:
                continue
            colour_outputs.append(format_colour('{} {}'.format(required, colour), colour))
        output.append('< {} >'.format(', '.join(colour_outputs)))

    return ' '.join(output)
                    
colour_lookup = {'white': 'aaaaaa',
                 'blue': '0000cc',
                 'green': '00aa00',
                 'red': 'cc0000',
                 'black': '000000'}
def format_colour(string, colour):
    return '[b][color=#{}]{}[/color][/b]'.format(colour_lookup[colour],
                                                 string)

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

class NumberCircleWithCard(NumberCircle):
    card_number = NumericProperty(0)
    show_card_number = BooleanProperty(True)

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

    white_cards = NumericProperty(0)
    blue_cards = NumericProperty(0)
    green_cards = NumericProperty(0)
    red_cards = NumericProperty(0)
    black_cards = NumericProperty(0)

    show_card_number = BooleanProperty(True)

class PlayerDisplay(AnchorLayout):
    white = NumericProperty(0)
    blue = NumericProperty(0)
    green = NumericProperty(0)
    red = NumericProperty(0)
    black = NumericProperty(0)
    gold = NumericProperty(0)

    white_cards = NumericProperty(0)
    blue_cards = NumericProperty(0)
    green_cards = NumericProperty(0)
    red_cards = NumericProperty(0)
    black_cards = NumericProperty(0)

    player = ObjectProperty(None)
    name = StringProperty('player')
    show_card_number = BooleanProperty(True)

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

    p1_white_cards = NumericProperty(0)
    p1_blue_cards = NumericProperty(0)
    p1_green_cards = NumericProperty(0)
    p1_red_cards = NumericProperty(0)
    p1_black_cards = NumericProperty(0)
    p1_gold_cards = NumericProperty(0)

    p2_white_cards = NumericProperty(0)
    p2_blue_cards = NumericProperty(0)
    p2_green_cards = NumericProperty(0)
    p2_red_cards = NumericProperty(0)
    p2_black_cards = NumericProperty(0)
    p2_gold_cards = NumericProperty(0)

    scores = ListProperty([])

    player_hand_cards = ListProperty([])

    round_number = NumericProperty(0)

    last_move_info = StringProperty('')

    nobles_text = StringProperty('')

    current_value_text = StringProperty('')

    player_types = ListProperty(['player:1', 'player:2']) #H50AI_TDlam(restore=True, prob_factor=20, num_players=2)])
    current_player_index = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ai = H50AI_TDlam(restore=True, stepsize=0, prob_factor=100, num_players=2)
        self.init_game_state()


    def init_game_state(self):
        self.state = GameState(players=self.num_players,
                               init_game=True,
                               validate=self.validate)
        self.sync_with_game_state()

    def sync_with_game_state(self):

        self.current_player_index = self.state.current_player_index

        self.tier_1_cards = self.state.cards_in_market(1)
        self.tier_2_cards = self.state.cards_in_market(2)
        self.tier_3_cards = self.state.cards_in_market(3)

        self.player_hand_cards = self.state.players[0].cards_in_hand

        for colour in colours + ['gold']:
            setattr(self, 'supply_' + colour, self.state.num_gems_available(colour))

            for i, player in enumerate(self.state.players):
                setattr(self, 'p{}_{}'.format(i + 1, colour), player.num_gems(colour))
                setattr(self, 'p{}_{}_cards'.format(i+1, colour), player.num_cards_of_colour(colour))

        self.round_number = self.state.round_number

        self.scores = [player.score for player in self.state.players]

        if self.state.moves:
            last_move = self.state.moves[-1]
            if last_move[0] == 'gems':
                self.last_move_info = 'gained gems ' + str(last_move[1])
            elif last_move[0].startswith('buy_'):
                previous_player_index = (self.current_player_index - 1) % len(self.state.players)
                card = self.state.players[previous_player_index].cards_played[-1]
                self.last_move_info = 'bought {}'.format(card)
            elif last_move[0] == 'reserve':
                self.last_move_info = 'reserved from tier {}'.format(last_move[1])
            else:
                import ipdb
                ipdb.set_trace()
                raise ValueError('Unrecognised move')

        else:
            self.last_move_info = '---'

        self.nobles_text = 'nobles: {}\nP1 nobles: {}   P2 nobles: {}'.format(
            format_nobles(self.state.nobles),
            format_nobles(self.state.players[0].nobles),
            format_nobles(self.state.players[1].nobles))

        values = self.ai.evaluate(self.state)
        text = 'P1: {:.03f} {:.03f}\nP2: {:.03f} {:.03f}'.format(
            values[0, 0], values[1, 1], values[0, 1], values[1, 0])
        self.current_value_text = text


    def do_ai_move(self):
        move, move_info = self.ai.make_move(self.state)
        self.state.make_move(move)
        self.sync_with_game_state()

    def reset_game(self):
        self.init_game_state()

class MenuScreen(Screen):
    pass

class GameGuiApp(App):
    def build(self):
        Window.clearcolor = (0.945, 0.945, 0.831, 1)
        return Root()


if __name__ == "__main__":
    GameGuiApp().run()
