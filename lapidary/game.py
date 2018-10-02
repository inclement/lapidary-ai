import random
from itertools import permutations
import numpy as np

from data import colours, colour_indices

# Splendor colour order:
# - White
# - Blue
# - Green
# - Red
# - Black

class Card(object):
    def __init__(
            self, tier, colour, points, white=0, blue=0,
            green=0, red=0, black=0):
        self.colour = colour
        self.points = points
        self.tier = tier

        
        self.white = white
        self.blue = blue
        self.green = green
        self.red = red
        self.black = black

    @property
    def requirements(self):
        return (self.white, self.blue, self.green, self.red, self.black)

    def num_required(self, colour):
        return getattr(self, colour)

    @property
    def total_num_required(self):
        return sum(self.requirements)

    @property
    def sort_info(self):
        return (self.points, self.white, self.blue, self.green, self.black)

    def __str__(self):
        return '<Card T={} P={} {}>'.format(
            self.tier, self.points, ','.join(
                ['{}:{}'.format(colour, self.num_required(colour)) for colour in ('white', 'blue', 'green', 'red', 'black') if self.num_required(colour)]))

    def __repr__(self):
        return str(self)
                 
class Noble(object):
    def __init__(self, points=3, white=0, blue=0, green=0, red=0, black=0):
        self.points = points

        self.white = white
        self.blue = blue
        self.green = green
        self.red = red
        self.black = black

    def num_required(self, colour):
        return getattr(self, colour)

    def __str__(self):
        return '<Noble P={} {}>'.format(
            self.points, ','.join(
                ['{}:{}'.format(colour, self.num_required(colour)) for colour in ('white', 'blue', 'green', 'red', 'black') if self.num_required(colour)]))

    def __repr__(self):
        return str(self)

tier_1 = [
    Card(1, 'blue', 0, black=3),
    Card(1, 'blue', 0, white=1, black=2),
    Card(1, 'blue', 0, green=2, black=2),
    Card(1, 'blue', 0, white=1, green=2, red=2),
    Card(1, 'blue', 0, blue=1, green=3, red=1),
    Card(1, 'blue', 0, white=1, green=1, red=1, black=1),
    Card(1, 'blue', 0, white=1, green=1, red=2, black=1),
    Card(1, 'blue', 1, red=4),

    Card(1, 'red', 0, white=3),
    Card(1, 'red', 0, blue=2, green=1),
    Card(1, 'red', 0, white=2, red=2),
    Card(1, 'red', 0, white=2, green=1, black=2),
    Card(1, 'red', 0, white=1, red=1, black=3),
    Card(1, 'red', 0, white=1, blue=1, green=1, black=1),
    Card(1, 'red', 0, white=2, blue=1, green=1, black=1),
    Card(1, 'red', 1, white=4),

    Card(1, 'black', 0, green=3),
    Card(1, 'black', 0, green=2, red=1),
    Card(1, 'black', 0, white=2, green=2),
    Card(1, 'black', 0, white=2, blue=2, red=1),
    Card(1, 'black', 0, green=1, red=3, black=1),
    Card(1, 'black', 0, white=1, blue=1, green=1, red=1),
    Card(1, 'black', 0, white=1, blue=2, green=1, red=1),
    Card(1, 'black', 1, blue=4),

    Card(1, 'white', 0, blue=3),
    Card(1, 'white', 0, red=2, black=1),
    Card(1, 'white', 0, blue=2, black=2),
    Card(1, 'white', 0, blue=2, green=2, black=1),
    Card(1, 'white', 0, white=3, blue=1, black=1),
    Card(1, 'white', 0, blue=1, green=1, red=1, black=1),
    Card(1, 'white', 0, blue=1, green=2, red=1, black=1),
    Card(1, 'white', 1, green=4),

    Card(1, 'green', 0, red=3),
    Card(1, 'green', 0, white=2, blue=1),
    Card(1, 'green', 0, blue=2, red=2),
    Card(1, 'green', 0, blue=1, red=2, black=2),
    Card(1, 'green', 0, white=1, blue=3, green=1),
    Card(1, 'green', 0, white=1, blue=1, red=1, black=1),
    Card(1, 'green', 0, white=1, blue=1, red=1, black=2),
    Card(1, 'green', 1, black=4)
    ]

tier_2 = [
    Card(2, 'blue', 1, blue=2, green=2, red=3),
    Card(2, 'blue', 1, blue=2, green=3, black=3),
    Card(2, 'blue', 2, blue=5),
    Card(2, 'blue', 2, white=5, blue=3),
    Card(2, 'blue', 2, white=2, red=1, black=4),
    Card(2, 'blue', 3, blue=6),

    Card(2, 'red', 1, white=2, red=2, black=3),
    Card(2, 'red', 1, blue=3, red=2, black=3),
    Card(2, 'red', 2, black=5),
    Card(2, 'red', 2, white=3, black=5),
    Card(2, 'red', 2, white=1, blue=4, green=2),
    Card(2, 'red', 3, red=6),

    Card(2, 'black', 1, white=3, blue=2, green=2),
    Card(2, 'black', 1, white=3, green=3, black=2),
    Card(2, 'black', 2, white=5),
    Card(2, 'black', 2, green=5, red=3),
    Card(2, 'black', 2, blue=1, green=4, red=2),
    Card(2, 'black', 3, black=6),

    Card(2, 'white', 1, green=3, red=2, black=2),
    Card(2, 'white', 1, white=2, blue=3, red=3),
    Card(2, 'white', 2, red=5),
    Card(2, 'white', 2, red=5, black=3),
    Card(2, 'white', 2, green=1, red=4, black=2),
    Card(2, 'white', 3, white=6),

    Card(2, 'green', 1, white=2, blue=3, black=2),
    Card(2, 'green', 1, white=3, green=2, red=3),
    Card(2, 'green', 2, green=5),
    Card(2, 'green', 2, blue=5, green=3),
    Card(2, 'green', 2, white=4, blue=2, black=1),
    Card(2, 'green', 3, green=6)
    ]

tier_3 = [
    Card(3, 'blue', 3, white=3, green=3, red=3, black=5),
    Card(3, 'blue', 4, white=7),
    Card(3, 'blue', 4, white=6, blue=3, black=3),
    Card(3, 'blue', 5, white=7, blue=3),

    Card(3, 'red', 3, white=3, blue=5, green=3, black=3),
    Card(3, 'red', 4, green=7),
    Card(3, 'red', 4, blue=3, green=6, red=3),
    Card(3, 'red', 5, green=7, red=3),

    Card(3, 'black', 3, white=3, blue=3, green=5, red=3),
    Card(3, 'black', 4, red=7),
    Card(3, 'black', 4, green=3, red=6, black=3),
    Card(3, 'black', 5, red=7, black=3),

    Card(3, 'white', 3, blue=3, green=3, red=5, black=3),
    Card(3, 'white', 4, black=7),
    Card(3, 'white', 4, white=3, red=3, black=6),
    Card(3, 'white', 5, white=3, black=7),

    Card(3, 'green', 3, white=5, blue=3, red=3, black=3),
    Card(3, 'green', 4, blue=7),
    Card(3, 'green', 4, white=3, blue=6, green=3),
    Card(3, 'green', 5, blue=7, green=3)
    ]

triples = {('black', 'blue', 'white'),
           ('black', 'green', 'blue'),
           ('black', 'green', 'white'),
           ('black', 'red', 'blue'),
           ('black', 'red', 'green'),
           ('black', 'red', 'white'),
           ('green', 'blue', 'white'),
           ('red', 'blue', 'white'),
           ('red', 'green', 'blue'),
           ('red', 'green', 'white')}
pairs = [('black', 'red'),
         ('black', 'blue'),
         ('black', 'white'),
         ('black', 'green'),
         ('red', 'blue'),
         ('red', 'white'),
         ('red', 'green'),
         ('blue', 'white'),
         ('blue', 'green'),
         ('green', 'white')]
# tier_1 = [Card(1, 'blue', 0, **{c: 1 for c in triple}) for triple in triples]
# tier_1 = [Card(1, 'blue', 0, **{c1: 2, c2: 1}) for c1, c2 in pairs]
# tier_1 = [Card(1, 'blue', 0, **{'black': 3, 'white': 1}) for _ in range(4)] + [Card(1, 'blue', 0, **{'green': 3, 'red': 1}) for _ in range(4)]
# tier_1 = [Card(1, 'blue', 0, **{'black': 3, 'white': 1}) for _ in range(5)] + [Card(1, 'blue', 0, **{'green': 3, 'red': 1}) for _ in range(5)] + [Card(1, 'red', 0, **{'white': 3, 'green': 1}) for _ in range(5)] + [Card(1, 'red', 0, **{'red': 3, 'black': 1}) for _ in range(5)]
# tier_2 = []
# tier_2 = [Card(2, 'blue', 1, **{'blue': 6}) for _ in range(5)] + [Card(2, 'red', 1, **{'red': 5}) for _ in range(5)]
# tier_1 = tier_1[:18]
# tier_2 = tier_2[:12]
# tier_3 = []
all_cards = tier_1 + tier_2 + tier_3
# tier_1 = set(tier_1)
# tier_2 = set(tier_2)
# tier_3 = set(tier_3)

cards_by_gem_colour = {'white': [],
                       'blue': [],
                       'green': [],
                       'red': [],
                       'black': []}
for card in all_cards:
    for colour in colours:
        if card.num_required(colour):
            cards_by_gem_colour[colour].append(card)


nobles = [
    Noble(red=4, green=4),
    Noble(black=4, red=4),
    Noble(blue=4, green=4),
    Noble(black=4, white=4),
    Noble(blue=4, white=4),
    Noble(black=3, red=3, white=3),
    Noble(green=3, blue=3, white=3),
    Noble(black=3, red=3, green=3),
    Noble(green=3, blue=3, red=3),
    Noble(black=3, blue=3, white=3)
    ]

class Player(object):
    def __init__(self):
        self.cards_in_hand = []
        self.cards_played = []
        self.nobles = []

        self._gold = 0
        self._white = 0
        self._blue = 0
        self._green = 0
        self._red = 0
        self._black = 0

    def copy(self):
        copy = Player()
        for colour in colours + ['gold']:
            copy.set_gems(colour, self.num_gems(colour))
        copy.nobles = self.nobles[:]
        copy.cards_in_hand = self.cards_in_hand[:]
        copy.cards_played = self.cards_played[:]
        return copy

    def num_gems(self, colour):
        return getattr(self, '_' + colour)

    def set_gems(self, colour, number):
        setattr(self, '_' + colour, number)

    @property
    def total_num_gems(self):
        return (self._gold + self._white + self._blue + self._green +
                self._red + self._black)

    @property
    def gems(self):
        return {'white': self._white,
                'blue': self._blue,
                'green': self._green,
                'red': self._red,
                'black': self._black,
                'gold': self._gold}

    # def gems_list(self):
    #     return (['white' for _ in range(self.white)] + 
    #             ['blue' for _ in range(self.blue)] +
    #             ['green' for _ in range(self.green)] +
    #             ['red' for _ in range(self.red)] +
    #             ['black' for _ in range(self.black)] +
    #             ['gold' for _ in range(self.gold)])

    def add_gems(self, **kwargs):
        for colour, change in kwargs.items():
            assert colour in colours or colour == 'gold'
            self.set_gems(colour, self.num_gems(colour) + change)


    @property
    def num_reserved(self):
        return len(self.cards_in_hand)

    @property
    def score(self):
        score = 0
        num_zero = 0
        for card in self.cards_played:
            points = card.points
            if points > 0:
                score += card.points
            else:
                num_zero += 1

        # score -= num_zero# // 3

        for noble in self.nobles:
            score += noble.points

        return score

    def num_cards_of_colour(self, colour):
        number = 0
        for card in self.cards_played:
            if card.colour == colour:
                number += 1
        return number

    def can_afford(self, card):
        missing_colours = [max(card.num_required(colour) -
                               self.num_gems(colour) -
                               self.num_cards_of_colour(colour), 0)
                           for colour in colours]

        if sum(missing_colours) > self.num_gems('gold'):
            return False, sum(missing_colours) - self.num_gems('gold')

        cost = {colour: max(min(self.num_gems(colour),
                                card.num_required(colour) -
                                self.num_cards_of_colour(colour)),
                            0) for colour in colours}
        cost['gold'] = sum(missing_colours)

        # TODO: Allow gold to be used instead of coloured gems, if available

        return True, cost

    def verify_state(self):
        assert 0 <= self.total_num_gems <= 10
        assert len(self.cards_in_hand) <= 3
        assert len(set(self.nobles)) == len(self.nobles)

        for colour in colours + ['gold']:
            assert self.num_gems(colour) >= 0

    @property
    def num_cards_each_tier(self):
        results = np.zeros(3)
        for card in self.cards_played:
            results[card.tier - 1] += 1
        return results


class StateVector(object):
    def __init__(self, num_players, vector=None):
        super(StateVector, self).__init__()

        self.num_players = num_players

        self.num_gems_in_play = {2: 4, 3: 5, 4: 7}[num_players]
        self.num_dev_cards = 4
        self.num_nobles = {2:3, 3:4, 4:5}[num_players]

        self.num_cards = len(all_cards)

        if vector is None:
            self.init_vector()
        else:
            self.vector = vector

    def copy(self):
        vector = StateVector(num_players=self.num_players,
                             vector=self.vector.copy())
        vector.supply_gem_indices = self.supply_gem_indices
        vector.player_gem_indices = self.player_gem_indices
        vector.player_played_colours_indices = self.player_played_colours_indices
        vector.player_score_indices = self.player_score_indices
        vector.current_player_indices = self.current_player_indices
        vector.card_cost_indices = self.card_cost_indices
        vector.player_card_cost_indices = self.player_card_cost_indices
        vector.card_points_indices = self.card_points_indices
        vector.player_card_points_indices = self.player_card_points_indices
        vector.tier_max_gems = self.tier_max_gems
        vector.tier_max_points = self.tier_max_points
        vector.tier_min_points = self.tier_min_points
        vector.points_indices = self.points_indices
        vector.no_points_indices = self.no_points_indices
        vector.noble_cost_indices = self.noble_cost_indices
        vector.nobles_present_index = self.nobles_present_index
        vector.card_remaining_cost_indices = self.card_remaining_cost_indices
        vector.player_card_remaining_cost_indices = self.player_card_remaining_cost_indices

        vector.card_colour_indices = self.card_colour_indices
        vector.player_card_colour_indices = self.player_card_colour_indices

        return vector

    def from_perspective_of(self, index, debug=False):
        if index == 0:
            return self.vector

        
        vector = self.vector
        new_vector = self.vector.copy()
        num_cards = self.num_cards
        num_players = self.num_players

        first_colour = colours[0]

        # # Rotate the cards in hand values
        # start_index = 0
        # end_index = self.supply_gem_indices[colours[0]]
        # player_cards_in_hand = [vector[start_index + 2 + i:end_index:(2 + num_players + num_players)]
        #                         for i in range(num_players)]
        # for i in range(num_players):
        #     cards_in_hand = player_cards_in_hand[(i + index) % num_players]
        #     assert len(cards_in_hand) == num_cards
        #     new_vector[(start_index + 2 + i):end_index:(2 + num_players + num_players)] = cards_in_hand

        # if debug:
        #     import ipdb
        #     ipdb.set_trace()

        # # Rotate the cards played values
        # start_index = 0
        # end_index = self.supply_gem_indices[colours[0]]
        # player_cards_played = [vector[start_index + 2 + num_players + i:end_index:(2 + num_players * 2)]
        #                        for i in range(num_players)]
        # for i in range(num_players):
        #     cards_played = player_cards_played[(i + index) % num_players]
        #     assert len(cards_played) == num_cards
        #     new_vector[(start_index + 2 + num_players + i):end_index:(2 + num_players * 2)] = cards_played

        # Rotate number of gems held by each player
        arr_size = self.player_gem_indices[1, colours[0]] - self.player_gem_indices[0, colours[0]]
        player_gems = [vector[self.player_gem_indices[(i, first_colour)]:self.player_gem_indices[(i, first_colour)] + arr_size] for i in range(num_players)]
        for i in range(num_players):
            cur_player_gems = player_gems[(i + index) % num_players]
            cur_player_index = self.player_gem_indices[(i, first_colour)]
            new_vector[cur_player_index:cur_player_index + arr_size] = cur_player_gems

        # Rotate number of cards played by each player
        arr_size = 8 * 5
        player_cards = [vector[self.player_played_colours_indices[(i, first_colour)]:self.player_played_colours_indices[(i, first_colour)] + arr_size] for i in range(num_players)]
        for i in range(num_players):
            cur_player_num_cards = player_cards[(i + index) % num_players]
            cur_player_index = self.player_played_colours_indices[(i, first_colour)]
            new_vector[cur_player_index:cur_player_index + arr_size] = cur_player_num_cards

        # Rotate current score of each player
        arr_size = 21
        player_scores = [vector[self.player_score_indices[i]:self.player_score_indices[i] + arr_size] for i in range(num_players)]
        for i in range(num_players):
            cur_player_score = player_scores[(i + index) % num_players]
            cur_player_index = self.player_score_indices[i]
            new_vector[cur_player_index:cur_player_index + arr_size] = cur_player_score

        # Rotate current player
        p1_index = self.current_player_indices[0]
        current_players = vector[p1_index:p1_index + self.num_players]
        new_vector[p1_index:p1_index + self.num_players] = np.roll(current_players, -1 * index)

        # Rotate noble remaining costs
        p1_index = self.noble_cost_indices[(0, 0, colours[0])]
        current_costs = vector[
            p1_index:p1_index + self.num_players * len(colours) * 5 * self.num_nobles]
        new_vector[p1_index:p1_index + len(current_costs)] = np.roll(
            current_costs, len(colours) * 5 * self.num_nobles * index)

        # Rotate cost of cards in hand
        p1_index = self.player_card_cost_indices[(0, 0, colours[0])]
        p2_index = self.player_card_cost_indices[(1, 0, colours[0])]
        length = p2_index - p1_index
        new_vector[p1_index:p1_index + self.num_players * length] = np.roll(
            vector[p1_index:p1_index + self.num_players * length], -1 * length * index)

        # Rotate points of cards in hand
        p1_index = self.player_card_points_indices[(0, 0)]
        p2_index = self.player_card_points_indices[(1, 0)]
        length = p2_index - p1_index
        new_vector[p1_index:p1_index + self.num_players * length] = np.roll(
            vector[p1_index:p1_index + self.num_players * length], -1 * length * index)

        # Rotate remaining cost of cards in market
        p1_index = self.card_remaining_cost_indices[(0, 1, 0, 'white')]
        p2_index = self.card_remaining_cost_indices[(1, 1, 0, 'white')]
        length = p2_index - p1_index
        new_vector[p1_index:p1_index + self.num_players * length] = np.roll(
            vector[p1_index:p1_index + self.num_players * length], -1 * length * index)

        # Rotate remaining cost of cards in hands
        p1_index = self.player_card_remaining_cost_indices[(0, 0, 'white')]
        p2_index = self.player_card_remaining_cost_indices[(1, 0, 'white')]
        length = p2_index - p1_index
        new_vector[p1_index:p1_index + self.num_players * length] = np.roll(
            vector[p1_index:p1_index + self.num_players * length], -1 * length * index)

        # Rotate colours of hand cards
        p1_index = self.player_card_colour_indices[(0, 0)]
        p2_index = self.player_card_colour_indices[(1, 0)]
        length = p2_index - p1_index
        new_vector[p1_index:p1_index + self.num_players * length] = np.roll(
            vector[p1_index:p1_index + self.num_players * length], -1 * length * index)
        

        # Rotate number of points-less buys
        p1_index = self.no_points_indices[0]
        p2_index = self.no_points_indices[1]
        length = p2_index - p1_index
        new_vector[p1_index:p1_index + self.num_players * length] = np.roll(
            vector[p1_index:p1_index + self.num_players * length], -1 * length * index)

        # Rotate number of pointsful buys
        p1_index = self.points_indices[0]
        p2_index = self.points_indices[1]
        length = p2_index - p1_index
        new_vector[p1_index:p1_index + self.num_players * length] = np.roll(
            vector[p1_index:p1_index + self.num_players * length], -1 * length * index)
        

        return new_vector

    def init_vector(self):
        
        num_players = self.num_players
        num_cards = len(all_cards)

        cur_index = 0

        # # store card locations
        # card_locations = [0 for _ in range(num_cards * (2 + num_players + num_players))]
        # self.card_indices = {card: i * (2 + num_players + num_players)
        #                      for i, card in enumerate(all_cards)}

        # cur_index += len(card_locations)

        # store numbers of gems in the supply
        num_colour_gems_in_play = self.num_gems_in_play
        gem_nums_in_supply = [0 for _ in range(5 * (num_colour_gems_in_play + 1))]
        self.supply_gem_indices = {colour: cur_index + i * (num_colour_gems_in_play + 1)
                                   for i, colour in enumerate(colours)}

        cur_index += len(gem_nums_in_supply)

        # ...plus gold
        gold_nums_in_supply = [0 for _ in range(6)]
        self.supply_gem_indices['gold'] = cur_index

        cur_index += len(gold_nums_in_supply)

        # store numbers of gems held by each player
        all_player_gems = []
        player_gem_indices = {}
        for player_index in range(num_players):
            player_gems = [0 for _ in range(5 * (num_colour_gems_in_play + 1))]
            all_player_gems.extend(player_gems)
            player_gem_indices.update({(player_index, colour): cur_index + i * (num_colour_gems_in_play + 1)
                                       for i, colour in enumerate(colours)})
            cur_index += len(player_gems)

            all_player_gems.extend([0 for _ in range(6)])
            player_gem_indices[(player_index, 'gold')] = cur_index
            cur_index += 6
        
            all_player_gems.extend([0 for _ in range(11)])
            player_gem_indices[(player_index, 'all')] = cur_index
            cur_index += 11
        
        self.player_gem_indices = player_gem_indices

        # store numbers of coloured cards played by each player
        # only count up to 7 - more than this makes no difference
        all_player_cards = []
        player_played_colours_indices = {}
        for player_index in range(num_players):
            player_cards = [0 for _ in range(5 * 8)]
            all_player_cards.extend(player_cards)

            player_played_colours_indices.update({(player_index, colour): cur_index + i * 8
                                                  for i, colour in enumerate(colours)})
            cur_index += len(player_cards)
        self.player_played_colours_indices = player_played_colours_indices
            
        # store number of points of each player
        # only count up to 20, higher scores are very unlikely
        player_scores = [0 for _ in range(21 * num_players)]
        self.player_score_indices = {player_index: cur_index + player_index * 21
                                     for player_index in range(num_players)}

        cur_index  += len(player_scores)

        # store current player
        current_player = [0 for _ in range(num_players)]
        current_player[0] = 1
        self.current_player_indices = {player_index: cur_index + player_index
                                       for player_index in range(num_players)}

        cur_index += len(current_player)

        # # store current round
        # current_round = [0 for _ in range(51)]
        # current_round[0] = 1
        # self.current_round_index = cur_index

        # cur_index += 51

        # store remaining cost of each available noble
        noble_cost_indices = {}
        noble_costs = [0 for _ in range(self.num_nobles * 5 * 5 * num_players)]
        for player_index in range(num_players):
            for noble_index in range(self.num_nobles):
                for colour_index, colour in enumerate(colours):
                    noble_cost_indices[(player_index, noble_index, colour)] = (
                        cur_index + noble_index * 5 * 5 + colour_index * 5 + player_index * self.num_nobles * 5 * 5)
        self.noble_cost_indices = noble_cost_indices
        cur_index += len(noble_costs)

        # store whether each noble is present
        nobles_present = [0 for _ in range(self.num_nobles)]
        self.nobles_present_index = cur_index
        cur_index += len(nobles_present)

        # store cost of each available card
        card_cost_indices = {}
        t1_max_gems = 5
        for card_index in range(4):  # tier 1
            for colour_index, colour in enumerate(colours):
                card_cost_indices[(1, card_index, colour)] = (
                    cur_index + card_index * 5 * t1_max_gems + colour_index * t1_max_gems)
        cur_index += 4 * 5 * t1_max_gems
        t2_max_gems = 7
        for card_index in range(4):  # tier 2
            for colour_index, colour in enumerate(colours):
                card_cost_indices[(2, card_index, colour)] = (
                    cur_index + card_index * 5 * t2_max_gems + colour_index * t2_max_gems)
        cur_index += 4 * 5 * t2_max_gems
        t3_max_gems = 8
        for card_index in range(4):  # tier 3
            for colour_index, colour in enumerate(colours):
                card_cost_indices[(3, card_index, colour)] = (
                    cur_index + card_index * 5 * t3_max_gems + colour_index * t3_max_gems)
        cur_index += 4 * 5 * t3_max_gems
        self.card_cost_indices = card_cost_indices
        self.tier_max_gems = {1: 5, 2: 7, 3: 8}
        card_costs = [0 for _ in range(4 * 5 * (t1_max_gems + t2_max_gems + t3_max_gems))]

        # store cost of each card in player hands
        player_card_cost_indices = {}
        hand_max_gems = 8
        for player_index in range(num_players):
            for card_index in range(3):  # player hands
                for colour_index, colour in enumerate(colours):
                    player_card_cost_indices[(player_index, card_index, colour)] = (
                        cur_index + card_index * 5 * hand_max_gems + colour_index * t3_max_gems)
            cur_index += 3 * 5 * hand_max_gems
        self.player_card_cost_indices = player_card_cost_indices
        player_card_costs = [0 for _ in range(3 * 5 * hand_max_gems * num_players)]

        # store remaining cost of each available card
        card_remaining_cost_indices = {}
        for player_index in range(num_players):
            for tier_index in range(1, 4):
                tier_max_gems = {1: 5, 2: 7, 3: 8}[tier_index]
                for card_index in range(4):
                    for colour_index, colour in enumerate(colours):
                        card_remaining_cost_indices[
                            (player_index, tier_index, card_index, colour)] = cur_index
                        cur_index += tier_max_gems
        self.card_remaining_cost_indices = card_remaining_cost_indices
        remaining_card_costs = [0 for _ in range(num_players * (5 + 7 + 8) * 4 * 5)]

        # store remaining cost of each card in player hands
        player_card_remaining_cost_indices = {}
        hand_max_gems = 8
        for player_index in range(num_players):
            for card_index in range(3):
                for colour in colours:
                    player_card_remaining_cost_indices[(player_index, card_index, colour)] = cur_index
                    cur_index += hand_max_gems
        self.player_card_remaining_cost_indices = player_card_remaining_cost_indices
        player_remaining_card_costs = [0 for _ in range(num_players * 8 * 3 * 5)]

        # store points value of each available card
        card_points_indices = {}
        self.tier_max_points = {1: 1, 2: 3, 3: 5}
        self.tier_min_points = {1: 0, 2: 1, 3: 3}
        t1_num_diff_points = 2
        t2_num_diff_points = 3
        t3_num_diff_points = 3
        for card_index in range(4):  # tier 1
            card_points_indices[(1, card_index)] = cur_index + card_index * t1_num_diff_points
        cur_index += 4 * t1_num_diff_points
        for card_index in range(4):  # tier 2
            card_points_indices[(2, card_index)] = cur_index + card_index * t2_num_diff_points
        cur_index += 4 * t2_num_diff_points
        for card_index in range(4):  # tier 3
            card_points_indices[(3, card_index)] = cur_index + card_index * t3_num_diff_points
        cur_index += 4 * t3_num_diff_points
        card_points = [0 for _ in range(4 * (t1_num_diff_points + t2_num_diff_points + t3_num_diff_points))]
        self.card_points_indices = card_points_indices

        # store points value of each card in player hands
        hand_max_points = 6
        player_card_points_indices = {}
        for player_index in range(num_players):
            for card_index in range(3):  # player hands
                player_card_points_indices[(player_index, card_index)] = cur_index + card_index * hand_max_points
            cur_index += 3 * hand_max_points
        player_card_points = [0 for _ in range(num_players * 3 * hand_max_points)]
        self.player_card_points_indices = player_card_points_indices

        # store colour of each available card
        card_colour_indices = {}
        for tier_index in range(1, 4):
            for card_index in range(4):
                card_colour_indices[(tier_index, card_index)] = (
                    cur_index +
                    (tier_index - 1) * 4 * len(colour_indices) +
                    card_index * len(colour_indices))
        card_colours = [0 for _ in range(3 * 4 * len(colour_indices))]
        cur_index += len(card_colours)
        self.card_colour_indices = card_colour_indices

        # store colour of each card in player hands
        player_card_colour_indices = {}
        for player_index in range(num_players):
            for card_index in range(3):
                player_card_colour_indices[(player_index, card_index)] = (
                    cur_index +
                    player_index * 3 * len(colour_indices) +
                    card_index * len(colour_indices))
        player_card_colours = [0 for _ in range(num_players * 3 * len(colour_indices))]
        self.player_card_colour_indices = player_card_colour_indices
        cur_index += len(player_card_colours)


        # store number of times a points-less card has been bought
        no_points_buys = [0 for _ in range(16 * num_players)]
        self.no_points_indices = {player_index: cur_index + 16 * player_index for player_index in range(num_players)}
        cur_index += len(no_points_buys)

        # store number of times a pointful card has been bought
        points_buys = [0 for _ in range(10 * num_players)]
        self.points_indices = {player_index: cur_index + 10 * player_index for player_index in range(num_players)}
        cur_index += len(points_buys)

        # missing_state = [0]
        # self.missing_state_index = cur_index
        # cur_index += 1
                
        self.vector = np.array(#card_locations +
            gem_nums_in_supply + gold_nums_in_supply +
            all_player_gems + all_player_cards + player_scores +
            # nobles_available +
            current_player +
            noble_costs +
            nobles_present +
            # current_round +
            card_costs + player_card_costs +
            remaining_card_costs + player_remaining_card_costs +
            card_points + player_card_points +
            card_colours + player_card_colours +
            no_points_buys + points_buys
            # missing_state
        )
            # card_progress)

    def verify_state(self):

        # for i, card in enumerate(all_cards):
        #     index = self.card_indices[card]
        #     assert np.sum(self.vector[index:index + 2 + self.num_players + self.num_players]) == 1

        for colour in colours:
            index = self.supply_gem_indices[colour]
            assert np.sum(self.vector[index:index + self.num_gems_in_play + 1] == 1)
        gold_index = self.supply_gem_indices['gold']
        assert np.sum(self.vector[gold_index:gold_index + 5 + 1]) == 1

        for player_index in range(self.num_players):
            for colour in colours:
                index = self.player_gem_indices[(player_index, colour)]
                assert np.sum(self.vector[index:index + self.num_gems_in_play + 1] == 1)
            gold_index = self.player_gem_indices[(player_index, 'gold')]
            assert np.sum(self.vector[gold_index:gold_index + 5 + 1]) == 1

            # score_index = self.player_score_indices[player_index]
            # assert np.sum(self.vector[score_index:score_index + 21]) == 1

        current_player_index = self.current_player_indices[0]
        players = self.vector[current_player_index:current_player_index + self.num_players]
        assert np.sum(players) == 1

        vs = [self.from_perspective_of(i) for i in range(self.num_players)]
        sums = [np.sum(v) for v in vs]
        assert np.all(sums == sums[0])
            
    def num_supply_gems(self, colour):
        index = self.supply_gem_indices[colour]
        arr = self.vector[index:index + self.num_gems_in_play + 1]
        return np.argmax(arr)
        # return np.sum(arr) - 1

    # def set_missing_state(self, missing_state):
    #     index = self.missing_state_index
    #     self.vector[index] = 1

    def set_current_round(self, round_number):
        return
        index = self.current_round_index
        self.vector[index:index + 51] = 0
        # self.vector[index:index + round_number + 1] = 1
        self.vector[index + round_number] = 1

    def set_card_location(self, card, location):
        return  # not currently included
        card_index = self.card_indices[card]
        for i in range(2 + self.num_players):
            self.vector[card_index + i] = 0
        if location is not None:
            self.vector[card_index + location] = 1

    def set_supply_gems(self, colour, number):
        index = self.supply_gem_indices[colour]
        num_gems_in_play = self.num_gems_in_play if colour != 'gold' else 5
        self.vector[index:index + num_gems_in_play + 1] = 0
        # self.vector[index:index + number + 1] = 1
        self.vector[index + number] = 1

    def set_player_gems(self, player_index, colour, number):
        index = self.player_gem_indices[(player_index, colour)]
        if colour == 'gold':
            num_gems_in_play = 5
        elif colour == 'all':
            num_gems_in_play = 10
        else:
            num_gems_in_play = self.num_gems_in_play
        for i in range(num_gems_in_play + 1):
            self.vector[index + i] = 0
        # self.vector[index:index + number + 1] = 1
        self.vector[index + min(number, num_gems_in_play)] = 1

    def set_player_played_colour(self, player_index, colour, number):
        number = min(7, number)
        index = self.player_played_colours_indices[(player_index, colour)]
        for i in range(8):
            self.vector[index + i] = 0
        # self.vector[index + number] = 1
        self.vector[index:index + number + 1] = 1

    def set_player_score(self, player_index, score):
        score = min(score, 20)  # measured scores are clamped to 20
        index = self.player_score_indices[player_index]
        for i in range(21):
            self.vector[index + i] = 0
        # self.vector[index + score] = 1
        self.vector[index:index + score + 1] = 1

    def set_noble_available(self, noble, available):
        raise ValueError('set_noble_available no longer valid')
        noble_index = self.noble_indices[noble]
        if available:
            self.vector[noble_index] = 1
        else:
            self.vector[noble_index] = 0

    def set_current_player(self, player_index):
        start_index = self.current_player_indices[0]
        for i in range(self.num_players):
            self.vector[start_index + i] = 0
        self.vector[start_index + player_index] = 1

    # def set_can_afford(self, player_index, card, required):
    #     index = self.card_progress_indices[(player_index, card)]
    #     self.vector[index:index + 5] = 0
    #     self.vector[index + min(required, 4)] = 1

    # def set_progress(self, player_index, tier, row_index, required):
    #     index = self.card_progress_indices[(player_index, tier, row_index)]
    #     self.vector[index:index + self.max_progress_possible[tier]] = 0
    #     self.vector[index + required] = 1

    # def set_available_score(self, player_index, tier, row_index, points):
    #     index = self.available_score_indices[(player_index, tier, row_index)]
    #     self.vector[index:index + 6] = 0
    #     self.vector[index + points - 1] = 1

    def set_noble_cost(self, *args):
        raise AttributeError('set_noble_cost is not currently available')

    def set_noble_remaining_cost(self, player_index, noble_index, colour, number):

        assert number in range(5) or number is None
        index = self.noble_cost_indices[(player_index, noble_index, colour)]
        self.vector[index:index + 5] = 0

        if number is not None:
            self.vector[index + number] = 1

    def set_noble_present(self, index, value):
        self.vector[self.nobles_present_index + index] = value

    def set_card_cost(self, tier, index, colour, cost):
        index = self.card_cost_indices[(tier, index, colour)]
        self.vector[index:index + self.tier_max_gems[tier]] = 0.
        self.vector[index + cost] = 1.
        # self.vector[index:index + cost + 1] = 1.

    def set_card_points(self, tier, index, points):
        index = self.card_points_indices[(tier, index)]
        self.vector[index:index + self.tier_max_points[tier] - self.tier_min_points[tier] + 1] = 0.
        self.vector[index + points] = 1.
        # self.vector[index:index + points + 1] = 1.

    def set_player_card_cost(self, player_index, card_index, colour, cost):
        index = self.player_card_cost_indices[(player_index, card_index, colour)]
        self.vector[index:index + 8] = 0.
        if cost is not None:
            self.vector[index + cost] = 1.
            # self.vector[index:index + cost + 1] = 1.

    def set_player_card_points(self, player_index, card_index, points):
        index = self.player_card_points_indices[(player_index, card_index)]
        self.vector[index:index + 6] = 0.
        if points is not None:
            self.vector[index + points] = 1.
            # self.vector[index:index + points + 1] = 1.

    def set_card_remaining_cost(self, player_index, tier_index, card_index, colour, number):
        index = self.card_remaining_cost_indices[(player_index, tier_index, card_index, colour)]
        num_zeros = {1: 5, 2: 7, 3: 8}[tier_index]
        self.vector[index:index + num_zeros] = 0
        if number is not None:
            # self.vector[index + number] = 1
            self.vector[index:index + number + 1] = 1

    def set_player_card_remaining_cost(self, player_index, card_index, colour, number):
        index = self.player_card_remaining_cost_indices[(player_index, card_index, colour)]
        num_zeros = 8
        self.vector[index:index + num_zeros] = 0
        if number is not None:
            # self.vector[index + number] = 1
            self.vector[index:index + number + 1] = 1

    def set_card_colour(self, tier_index, card_index, colour):
        index = self.card_colour_indices[(tier_index, card_index)]
        self.vector[index:index + len(colour_indices)] = 0
        if colour is not None:
            self.vector[index + colour_indices[colour]] = 1

    def set_player_card_colour(self, player_index, card_index, colour):
        index = self.player_card_colour_indices[(player_index, card_index)]
        self.vector[index:index + len(colour_indices)] = 0
        if colour is not None:
            self.vector[index + colour_indices[colour]] = 1

    def set_no_points_buys(self, player_index, number):
        number = min(number, 15)
        index = self.no_points_indices[player_index]
        self.vector[index:index + 16] = 0
        self.vector[index:index + number + 1] = 1

    def set_points_buys(self, player_index, number):
        number = min(number, 9)
        index = self.points_indices[player_index]
        self.vector[index:index + 10] = 0
        self.vector[index:index + number + 1] = 1
        
    

class GameState(object):

    def __init__(self, players=3, init_game=False, validate=True, generator=None,
                 state_vector=None):
        self.num_players = players
        self.players = []
        self.validate = validate

        if state_vector is None:
            state_vector = StateVector(self.num_players)
        self.state_vector = state_vector

        self.current_player_index = 0

        self.num_gems_in_play = {2: 4, 3: 5, 4: 7}[players]
        self.num_dev_cards = 4
        self.num_nobles = {2:3, 3:4, 4:5}[players]

        self._tier_1 = tier_1
        self._tier_1_copied = False
        self._tier_2 = tier_2
        self._tier_2_copied = False
        self._tier_3 = tier_3
        self._tier_3_copied = False

        self._tier_1_visible = []
        self._tier_1_visible_copied = False
        self._tier_2_visible = []
        self._tier_2_visible_copied = False
        self._tier_3_visible = []
        self._tier_3_visible_copied = False

        self._num_gold_available = 5
        self._num_white_available = self.num_gems_in_play
        self._num_blue_available = self.num_gems_in_play
        self._num_green_available = self.num_gems_in_play
        self._num_red_available = self.num_gems_in_play
        self._num_black_available = self.num_gems_in_play

        self.initial_nobles = []
        self.nobles = []
        self.noble_indices = {}

        self.round_number = 1

        self.moves = []

        if generator is None:
            generator = np.random.RandomState()
        self.generator = generator

        if init_game:
            self.init_game()

    @property
    def tier_1(self):
        raise ValueError('tier_1')
    @property
    def tier_2(self):
        raise ValueError('tier_2')
    @property
    def tier_3(self):
        raise ValueError('tier_3')

    @property
    def tier_1_available(self):
        raise ValueError('tier_1_available')
    @property
    def tier_2_available(self):
        raise ValueError('tier_2_available')
    @property
    def tier_3_available(self):
        raise ValueError('tier_3_available')

    @property
    def num_gold_available(self):
        raise ValueError('gold')
    @property
    def num_white_available(self):
        raise ValueError('white')
    @property
    def num_blue_available(self):
        raise ValueError('blue')
    @property
    def num_green_available(self):
        raise ValueError('green')
    @property
    def num_red_available(self):
        raise ValueError('red')
    @property
    def num_black_available(self):
        raise ValueError('black')

    def copy(self):
        copy = GameState(self.num_players, validate=self.validate, generator=self.generator,
                         state_vector=self.state_vector.copy())
        for colour in colours + ['gold']:
            setattr(copy, '_num_{}_available'.format(colour), self.num_gems_available(colour))

        copy.initial_nobles = self.initial_nobles
        copy.nobles = self.nobles[:]

        copy._tier_1 = self.cards_in_deck(1, ensure_copied=False)
        copy._tier_2 = self.cards_in_deck(2, ensure_copied=False)
        copy._tier_3 = self.cards_in_deck(3, ensure_copied=False)

        copy._tier_1_visible = self.cards_in_market(1, ensure_copied=False)
        copy._tier_2_visible = self.cards_in_market(2, ensure_copied=False)
        copy._tier_3_visible = self.cards_in_market(3, ensure_copied=False)

        copy.players = [p.copy() for p in self.players]
        copy.current_player_index = self.current_player_index

        copy.generator = self.generator

        return copy

    def get_scores(self):
        scores = [player.score for player in self.players]
        return scores

    @property
    def current_player(self):
        return self.players[self.current_player_index]

    def num_gems_available(self, colour):
        return getattr(self, '_num_{}_available'.format(colour))

    def total_num_gems_available(self):
        return sum([self.num_gems_available(colour) for colour in colours])

    def cards_in_deck(self, tier, ensure_copied=True):
        tier_attr = '_tier_{}'.format(tier)
        if ensure_copied:
            copied_attr = '_tier_{}_copied'.format(tier)
            if not getattr(self, copied_attr):
                setattr(self, tier_attr, getattr(self, tier_attr)[:])
                setattr(self, copied_attr, True)
        return getattr(self, tier_attr)

    def cards_in_market(self, tier, ensure_copied=True):
        tier_attr = '_tier_{}_visible'.format(tier)
        if ensure_copied:
            copied_attr = '_tier_{}_visible_copied'.format(tier)
            if not getattr(self, copied_attr):
                setattr(self, tier_attr, getattr(self, tier_attr)[:])
                setattr(self, copied_attr, True)
        return getattr(self, '_tier_{}_visible'.format(tier))

    def add_supply_gems(self, colour, change):
        attr_name = '_num_{}_available'.format(colour)
        setattr(self, attr_name, getattr(self, attr_name) + change)
        self.state_vector.set_supply_gems(colour, self.num_gems_available(colour))

    def seed(self):
        self.generator.seed(seed)

    def init_game(self):
        # Shuffle the cards
        self.generator.shuffle(self.cards_in_deck(1))
        self.generator.shuffle(self.cards_in_deck(2))
        self.generator.shuffle(self.cards_in_deck(3))

        # Select nobles
        orig_nobles = nobles[:]
        self.generator.shuffle(orig_nobles)
        self.nobles = orig_nobles[:self.num_nobles]
        self.initial_nobles = tuple(self.nobles[:])
        self.noble_indices = {noble: index for index, noble in enumerate(self.nobles)}

        # Make player objects
        self.players = [Player() for _ in range(self.num_players)]

        # Update visible dev cards
        self.update_dev_cards()
        self.update_card_costs_and_points()

        # Sync with state vector
        for card in self.cards_in_deck(1) + self.cards_in_deck(2) + self.cards_in_deck(3):
            self.state_vector.set_card_location(card, 0)
        for card in self.cards_in_market(1) + self.cards_in_market(2) + self.cards_in_market(3):
            self.state_vector.set_card_location(card, 1)
        
        for colour in colours:
            self.state_vector.set_supply_gems(colour, self.num_gems_in_play)
        self.state_vector.set_supply_gems('gold', 5)

        # for noble_index, noble in enumerate(self.initial_nobles):
        #     for colour in colours:
        #         self.state_vector.set_noble_cost(noble_index, colour, noble.num_required(colour))
            # self.state_vector.set_noble_available(noble, 1)
        self.update_noble_availability()

        for player_index in range(self.num_players):
            self.state_vector.set_player_score(player_index, 0)
            for colour in colours:
                self.state_vector.set_player_gems(player_index, colour, 0)
                self.state_vector.set_player_played_colour(player_index, colour, 0)
                # self.state_vector.set_player_cards(player_index, colour, 0)
            self.state_vector.set_player_gems(player_index, 'all', 0)
            self.state_vector.set_player_gems(player_index, 'gold', 0)

        # for i in range(self.num_players):
        #     self.update_card_affording(i)
        
    # def update_card_affording(self, player_index, update_colours=colours):
    #     player = self.players[player_index]
    #     v = self.state_vector

    #     cards_to_update = set()
    #     for colour in update_colours:
    #         for card in cards_by_gem_colour[colour]:
    #             cards_to_update.add(card)

    #     for card in cards_to_update:
    #         can_afford, cost = player.can_afford(card)
    #         if can_afford:
    #             v.set_can_afford(player_index, card, 0)
    #         else:
    #             v.set_can_afford(player_index, card, cost)
                

    def make_move(self, move, refill_market=True):
        self.moves.append(move)

        player = self.players[self.current_player_index]
        if move[0] == 'gems':
            player.add_gems(**move[1])
            for colour, change in move[1].items():
                self.add_supply_gems(colour, -1 * change)
                self.state_vector.set_supply_gems(colour, self.num_gems_available(colour))
                self.state_vector.set_player_gems(self.current_player_index, colour, player.num_gems(colour))

            # update remaining costs for this player
            player_index = self.current_player_index
            for tier in range(1, 4):
                for card_index, card in enumerate(self.cards_in_market(tier)):
                    for colour in move[1]:
                        value = max(0, card.num_required(colour) - player.num_gems(colour) - player.num_cards_of_colour(colour))
                        self.state_vector.set_card_remaining_cost(
                            player_index, tier, card_index, colour, value)
                for card_index, card in enumerate(player.cards_in_hand):
                    for colour in move[1]:
                        value = max(0, card.num_required(colour) - player.num_gems(colour) - player.num_cards_of_colour(colour))
                        self.state_vector.set_player_card_remaining_cost(
                            player_index, card_index, colour, value)
                

        elif move[0] == 'buy_available':
            action, tier, index, gems = move
            card = self.cards_in_market(tier).pop(index)
            player.cards_played.append(card)
            self.state_vector.set_card_location(card, 2 + self.num_players + self.current_player_index)
            player.add_gems(**gems)
            for colour, change in gems.items():
                self.add_supply_gems(colour, -1 * change)
                self.state_vector.set_player_gems(self.current_player_index, colour, player.num_gems(colour))
            card_colour = card.colour
            cur_num_card_colour = len([c for c in player.cards_played if c.colour == card_colour])
            self.state_vector.set_player_played_colour(self.current_player_index, card_colour,
                                                       cur_num_card_colour)

            self.state_vector.set_player_score(self.current_player_index, player.score)

            for noble, noble_index in self.noble_indices.items():
                if noble in self.nobles:
                    self.state_vector.set_noble_remaining_cost(
                        self.current_player_index, noble_index, card_colour,
                        max(0, noble.num_required(card_colour) - player.num_cards_of_colour(card_colour)))

        elif move[0] == 'buy_reserved':
            action, index, gems = move
            card = player.cards_in_hand.pop(index)
            player.cards_played.append(card)
            self.state_vector.set_card_location(card, 2 + self.num_players + self.current_player_index)
            player.add_gems(**gems)
            for colour, change in gems.items():
                self.add_supply_gems(colour, -1 * change)
                self.state_vector.set_player_gems(self.current_player_index, colour, player.num_gems(colour))
            card_colour = card.colour
            cur_num_card_colour = len([c for c in player.cards_played if c.colour == card_colour])
            self.state_vector.set_player_played_colour(self.current_player_index, card_colour,
                                                 cur_num_card_colour)

            self.state_vector.set_player_score(self.current_player_index, player.score)

            for noble, noble_index in self.noble_indices.items():
                if noble in self.nobles:
                    self.state_vector.set_noble_remaining_cost(
                        self.current_player_index, noble_index, card_colour,
                        max(0, noble.num_required(card_colour) - player.num_cards_of_colour(card_colour)))

        elif move[0] == 'reserve':
            action, tier, index, gems = move
            if index == -1:
                card = self.cards_in_deck(tier).pop()
            else:
                card = self.cards_in_market(tier).pop(index)
            player.cards_in_hand.append(card)
            player.add_gems(**gems)
            for colour, change in gems.items():
                self.add_supply_gems(colour, -1 * change)
                self.state_vector.set_player_gems(self.current_player_index, colour, player.num_gems(colour))
            self.state_vector.set_card_location(card, 2 + self.current_player_index)
            # self.update_card_affording(self.current_player_index, update_colours=colours)

        else:
            raise ValueError('Received invalid move {}'.format(move))

        # Assign nobles if necessary
        assignable = []
        for i, noble in enumerate(self.nobles):
            for colour in colours:
                if player.num_cards_of_colour(colour) < noble.num_required(colour):
                    break
            else:
                assignable.append(i)
        if assignable:
            noble = self.nobles.pop(assignable[0])
            player.nobles.append(noble)
            self.state_vector.set_player_score(self.current_player_index, player.score)
            self.update_noble_availability()
            # self.state_vector.set_noble_available(noble, 0)

        # Clean up the state
        self.update_dev_cards(fake_refill=not refill_market)
        if move[0] != 'gems':
            self.update_card_costs_and_points()
        if move[0].startswith('buy'):
            num_cards_played = len(player.cards_played)
            points_cards_played = len([c for c in player.cards_played if c.points > 0])
            no_points_cards_played = num_cards_played - points_cards_played
            self.state_vector.set_points_buys(self.current_player_index, points_cards_played)
            self.state_vector.set_no_points_buys(self.current_player_index, no_points_cards_played)
        self.state_vector.set_player_gems(self.current_player_index, 'all', player.total_num_gems)
            
        # Check that everything is within expected parameters
        if self.validate:
            try:
                player.verify_state()
                self.verify_state()
            except AssertionError:
                print('Failure verifying state after making move')
                print('move was', move)
                import traceback
                traceback.print_exc()
                import ipdb; ipdb.set_trace()

        self.current_player_index += 1
        self.current_player_index %= len(self.players)
        if self.current_player_index == 0:
            self.round_number += 1
            self.state_vector.set_current_round(self.round_number)
        self.state_vector.set_current_player(self.current_player_index)

        return self

    def verify_state(self):
        sv = self.state_vector

        for player in self.players:
            player.verify_state()

        for colour in colours:
            assert 0 <= self.num_gems_available(colour) <= self.num_gems_in_play
        assert 0 <= self.num_gems_available('gold') <= 5

        for colour in colours:
            assert self.num_gems_available(colour) + sum([player.num_gems(colour) for player in self.players]) == self.num_gems_in_play
            assert self.num_gems_available(colour) == self.state_vector.num_supply_gems(colour)

            index = sv.supply_gem_indices[colour]
            num_available = self.num_gems_available(colour)
            assert np.sum(sv.vector[index:index + self.num_gems_in_play + 1]) == 1 #num_available + 1
            assert np.sum(sv.vector[index + num_available]) == 1

        gold_index = sv.supply_gem_indices['gold']
        assert np.sum(sv.vector[gold_index:gold_index + 6]) == 1 #self.num_gems_available('gold') + 1
        assert sv.vector[gold_index + self.num_gems_available('gold')] == 1

        for noble, noble_index in self.noble_indices.items():
            if noble in self.nobles:
                assert sv.vector[sv.nobles_present_index + noble_index] == 1
            else:
                assert sv.vector[sv.nobles_present_index + noble_index] == 0

            if noble in self.nobles:
                for player_index, player in enumerate(self.players):
                    for colour in colours:
                        index = sv.noble_cost_indices[(player_index, noble_index, colour)]
                        assert np.sum(sv.vector[index:index + 5]) == 1
                        assert sv.vector[index + max(0, noble.num_required(colour) - player.num_cards_of_colour(colour))] == 1
            else:
                for player_index, player in enumerate(self.players):
                    if noble not in player.nobles:
                        num_required = 0
                    else:
                        num_required = max(0, noble.num_required(colour) - player.num_cards_of_colour(colour))
                    assert num_required == 0
                    for colour in colours:
                        index = sv.noble_cost_indices[(player_index, noble_index, colour)]
                        assert np.sum(sv.vector[index:index + 5]) == 0
                    
                
        for tier in range(1, 4):
            for card_index, card in enumerate(self.cards_in_market(tier)):
                for colour in colours:
                    index = sv.card_cost_indices[(tier, card_index, colour)]
                    try:
                        assert np.sum(sv.vector[index:index + sv.tier_max_gems[tier]]) == 1 #card.num_required(colour) + 1
                        assert sv.vector[index + card.num_required(colour)] == 1
                    except AssertionError:
                        import traceback
                        traceback.print_exc()
                        import ipdb
                        ipdb.set_trace()

                index = sv.card_colour_indices[(tier, card_index)]
                try:
                    assert np.sum(sv.vector[index:index + len(colour_indices)]) == 1
                    assert sv.vector[index + colour_indices[card.colour]] == 1
                except AssertionError:
                    import traceback
                    traceback.print_exc()
                    import ipdb
                    ipdb.set_trace()
                    

                index = sv.card_points_indices[(tier, card_index)]
                offset = (sv.tier_max_points[tier] - sv.tier_min_points[tier] + 1)
                try:
                    assert np.sum(sv.vector[index:index + offset]) == 1 #card.points - sv.tier_min_points[tier] + 1
                except AssertionError:
                    import traceback
                    traceback.print_exc()
                    import ipdb
                    ipdb.set_trace()

                assert sv.vector[index + card.points - sv.tier_min_points[tier]] == 1

        for player_index, player in enumerate(self.players):
            for card_index, card in enumerate(player.cards_in_hand):
                for colour in colours:
                    index = sv.player_card_cost_indices[(player_index, card_index, colour)]
                    try:
                        assert np.sum(sv.vector[index:index + 8]) == 1 #card.num_required(colour) + 1
                        assert sv.vector[index + card.num_required(colour)] == 1
                    except AssertionError:
                        import traceback
                        traceback.print_exc()
                        import ipdb
                        ipdb.set_trace()

                index = sv.player_card_points_indices[(player_index, card_index)]
                assert np.sum(sv.vector[index:index + 6]) == 1 #card.points + 1
                assert sv.vector[index + card.points] == 1

                index = sv.player_card_colour_indices[(player_index, card_index)]
                assert np.sum(sv.vector[index:index + len(colour_indices)]) == 1
                assert sv.vector[index + colour_indices[card.colour]] == 1
            for card_index in range(len(player.cards_in_hand), 3):
                for colour in colours:
                    index = sv.player_card_cost_indices[(player_index, card_index, colour)]
                    assert np.sum(sv.vector[index:index + 8]) == 0
                index = sv.player_card_points_indices[(player_index, card_index)]
                assert np.sum(sv.vector[index:index + 6]) == 0

        # remaining costs
        for player_index, player in enumerate(self.players):
            for tier in range(1, 4):
                num_zeros = {1: 5, 2: 7, 3: 8}[tier]
                for card_index, card in enumerate(self.cards_in_market(tier)):
                    for colour in colours:
                        index = sv.card_remaining_cost_indices[(player_index, tier, card_index, colour)]
                        try:
                            assert np.sum(sv.vector[index:index + num_zeros]) == max(0, card.num_required(colour) - player.num_gems(colour) - player.num_cards_of_colour(colour)) + 1

                        except AssertionError:
                            import traceback
                            traceback.print_exc()
                            import ipdb
                            ipdb.set_trace()
                        assert sv.vector[index + max(
                            0, (card.num_required(colour) -
                                player.num_gems(colour) -
                                player.num_cards_of_colour(colour)))] == 1

                for card_index in range(len(self.cards_in_market(tier)), 4):
                    for colour in colours:
                        index = sv.card_remaining_cost_indices[(player_index, tier, card_index, colour)]
                        assert np.sum(sv.vector[index:index + num_zeros]) == 0

            for card_index, card in enumerate(player.cards_in_hand):
                for colour in colours:
                    index = sv.player_card_remaining_cost_indices[(player_index, card_index, colour)]
                    assert np.sum(sv.vector[index:index + 8]) == max(0, card.num_required(colour) - player.num_gems(colour) - player.num_cards_of_colour(colour)) + 1
                    assert sv.vector[index + max(
                        0, (card.num_required(colour) -
                            player.num_gems(colour) -
                            player.num_cards_of_colour(colour)))] == 1
            for card_index in range(len(player.cards_in_hand), 3):
                for colour in colours:
                    index = sv.player_card_remaining_cost_indices[(player_index, card_index, colour)]
                    assert np.sum(sv.vector[index:index + 8]) == 0
                


        for player_index, player in enumerate(self.players):
            pv = sv.from_perspective_of(player_index)
            # for card in player.cards_in_hand:
            #     index = sv.card_indices[card]
            #     assert np.sum(sv.vector[index:index + 2 + len(self.players)]) == 1
            #     assert sv.vector[index + 2 + player_index] == 1

            #     assert pv[index + 2] == 1

            # for card in player.cards_played:
            #     index = sv.card_indices[card]
            #     assert np.sum(sv.vector[index:index + 2 + len(self.players)]) == 0
            #     assert sv.vector[index + 2 + self.num_players + player_index] == 1

            #     assert pv[index + 2 + self.num_players] == 1

            for colour in colours:
                index = sv.player_gem_indices[(player_index, colour)]
                number = player.num_gems(colour)
                try:
                    assert np.sum(sv.vector[index:index + self.num_gems_in_play + 1]) == 1 #number + 1
                except:
                    import ipdb
                    ipdb.set_trace()
                assert sv.vector[index + player.num_gems(colour)] == 1
                p0_index = sv.player_gem_indices[(0, colour)]
                assert pv[p0_index + player.num_gems(colour)] == 1

                num_played = len([c for c in player.cards_played if c.colour == colour])
                index = sv.player_played_colours_indices[(player_index, colour)]
                assert np.sum(sv.vector[index:index + 8]) == min(7, num_played) + 1
                assert sv.vector[index + min(num_played, 7)] == 1
                p0_index = sv.player_played_colours_indices[(0, colour)]
                try:
                    assert pv[p0_index + min(num_played, 7)] == 1
                except AssertionError:
                    print('ERROR with num played of colour')
                    import traceback
                    traceback.print_exc()
                    import ipdb
                    ipdb.set_trace()
            index = sv.player_gem_indices[(player_index, 'all')]
            number = player.total_num_gems
            assert np.sum(sv.vector[index:index + 11]) == 1
            assert sv.vector[index + number] == 1
            

            score = player.score
            index = sv.player_score_indices[player_index]
            assert np.sum(sv.vector[index:index + 21]) == min(score, 20) + 1
            assert sv.vector[index + min(score, 20)] == 1
            p0_index = sv.player_score_indices[0]
            assert pv[p0_index + min(score, 20)] == 1

            gold_index = sv.player_gem_indices[(player_index, 'gold')]
            assert np.sum(sv.vector[gold_index:gold_index + 6]) == 1 #player.num_gems('gold') + 1
            assert sv.vector[gold_index + player.num_gems('gold')] == 1
            p0_index = sv.player_gem_indices[(0, 'gold')]
            try:
                assert pv[p0_index + player.num_gems('gold')] == 1
            except AssertionError:
                print('ERROR with num gold')
                import traceback
                traceback.print_exc()
                import ipdb
                ipdb.set_trace()

            for card_index, card in enumerate(player.cards_in_hand):
                for colour in colours:
                    index = sv.player_card_cost_indices[(0, card_index, colour)]
                    assert np.sum(pv[index:index + 8]) == 1 #card.num_required(colour) + 1
                    assert pv[index + card.num_required(colour)] == 1

                index = sv.player_card_points_indices[(0, card_index)]
                assert np.sum(pv[index:index + 6]) == 1 #card.points + 1
                assert pv[index + card.points] == 1
                
            for noble, noble_index in self.noble_indices.items():
                if noble in self.nobles:
                    for cur_player_index, player in enumerate(self.players):
                        cur_player_index -= player_index
                        cur_player_index %= self.num_players
                        for colour in colours:
                            index = sv.noble_cost_indices[(cur_player_index, noble_index, colour)]
                            assert np.sum(sv.vector[index:index + 5]) == 1
                            assert pv[index + max(0, noble.num_required(colour) - player.num_cards_of_colour(colour))] == 1
                else:
                    for cur_player_index, player in enumerate(self.players):
                        cur_player_index -= player_index
                        cur_player_index %= self.num_players
                        if noble not in player.nobles:
                            continue
                        for colour in colours:
                            index = sv.noble_cost_indices[(cur_player_index, noble_index, colour)]
                            assert np.sum(sv.vector[index:index + 5]) == 0
                            num_required = max(0, noble.num_required(colour) - player.num_cards_of_colour(colour))
                            assert num_required == 0
                            # assert pv[index + num_required] == 1

        # import ipdb
        # ipdb.set_trace()
        assert sv.vector[sv.current_player_indices[self.current_player_index]] == 1

        self.state_vector.verify_state()

    def update_dev_cards(self, fake_refill=False):

        while len(self.cards_in_market(1)) < 4 and self.cards_in_deck(1):
            if fake_refill:
                card = Card(1, 'none', 0, white=2, blue=2, green=2, red=2, black=2)
            else:
                card = self.cards_in_deck(1).pop()
            self.state_vector.set_card_location(card, 1)
            self.cards_in_market(1).append(card)
            self.cards_in_market(1).sort(key=lambda j: j.sort_info )

        while len(self.cards_in_market(2)) < 4 and self.cards_in_deck(2):
            if fake_refill:
                card = Card(2, 'none', 1, white=3, blue=3, green=3, red=3, black=3)
            else:
                card = self.cards_in_deck(2).pop()
            self.state_vector.set_card_location(card, 1)
            self.cards_in_market(2).append(card)
            self.cards_in_market(2).sort(key=lambda j: j.points)

        while len(self.cards_in_market(3)) < 4 and self.cards_in_deck(3):
            if fake_refill:
                card = Card(3, 'none', 3, white=4, blue=4, green=4, red=4, black=4)
            else:
                card = self.cards_in_deck(3).pop()
            self.state_vector.set_card_location(card, 1)
            self.cards_in_market(3).append(card)
            self.cards_in_market(3).sort(key=lambda j: j.points)

    def update_noble_availability(self):
        for noble, noble_index in self.noble_indices.items():
            if noble in self.nobles:
                self.state_vector.set_noble_present(noble_index, 1)
            else:
                self.state_vector.set_noble_present(noble_index, 0)

        for player_index, player in enumerate(self.players):
            for noble, noble_index in self.noble_indices.items():
                if noble not in self.nobles:
                    for colour in colours:
                        self.state_vector.set_noble_remaining_cost(
                            player_index, noble_index, colour, None)
                else:
                    for colour in colours:
                        self.state_vector.set_noble_remaining_cost(
                            player_index, noble_index, colour,
                            max(0, noble.num_required(colour) - player.num_cards_of_colour(colour)))

    def update_card_costs_and_points(self):
        for tier in range(1, 4):
            min_points = self.state_vector.tier_min_points[tier]
            for i, card in enumerate(self.cards_in_market(tier)):
                for colour in colours:
                    self.state_vector.set_card_cost(tier, i, colour, card.num_required(colour))
                self.state_vector.set_card_points(tier, i, card.points - min_points)
                self.state_vector.set_card_colour(tier, i, card.colour)
            # note: we don't clear the vector state if cards aren't present?

        for player_index, player in enumerate(self.players):
            num_cards_in_hand = len(player.cards_in_hand)
            for card_index in range(3):
                if card_index < num_cards_in_hand:
                    card = player.cards_in_hand[card_index]
                    for colour in colours:
                        self.state_vector.set_player_card_cost(player_index, card_index, colour,
                                                            card.num_required(colour))
                    self.state_vector.set_player_card_points(player_index, card_index, card.points)
                    self.state_vector.set_player_card_colour(player_index, card_index, card.colour)
                else:
                    for colour in colours:
                        self.state_vector.set_player_card_cost(player_index, card_index, colour, None)
                    self.state_vector.set_player_card_points(player_index, card_index, None)
                    self.state_vector.set_player_card_colour(player_index, card_index, None)

        # update remaining costs
        for player_index, player in enumerate(self.players):
            for tier in range(1, 4):
                for card_index, card in enumerate(self.cards_in_market(tier)):
                    for colour in colours:
                        value = max(0, card.num_required(colour) - player.num_gems(colour) - player.num_cards_of_colour(colour))
                        self.state_vector.set_card_remaining_cost(
                            player_index, tier, card_index, colour, value)
                for card_index in range(len(self.cards_in_market(tier)), 4):
                    for colour in colours:
                        self.state_vector.set_card_remaining_cost(
                            player_index, tier, card_index, colour, None)
            for card_index, card in enumerate(player.cards_in_hand):
                for colour in colours:
                    value = max(0, card.num_required(colour) - player.num_gems(colour) - player.num_cards_of_colour(colour))
                    self.state_vector.set_player_card_remaining_cost(
                        player_index, card_index, colour, value)
            for card_index in range(len(player.cards_in_hand), 3):
                for colour in colours:
                    self.state_vector.set_player_card_remaining_cost(
                        player_index, card_index, colour, None)

    def print_state(self):
        print('{} players'.format(self.num_players))
        print()

        print('Nobles:')
        for noble in self.nobles:
            print(noble)
        print()

        print('Tier 1 visible:')
        for card in self.tier_1_visible:
            print(card)
        print('{} tier 1 remain'.format(len(self.tier_1)))
        print()

        print('Tier 2 visible:')
        for card in self.tier_2_visible:
            print(card)
        print('{} tier 2 remain'.format(len(self.tier_2)))
        print()

        print('Tier 3 visible:')
        for card in self.tier_3_visible:
            print(card)
        print('{} tier 3 remain'.format(len(self.tier_3)))
        print()

        print('Available colours:')
        for colour in colours:
            print('  {}: {}'.format(colour, self.num_gemsavailable(colour)))
        print()

        for i, player in enumerate(self.players):
            i += 1
            print('Player {}:'.format(i))
            for colour in colours + ['gold']:
                print('  {}: {}'.format(colour, player.num_gems(colour)))
            if player.cards_in_hand:
                print(' reserves:'.format(i))
                for card in player.cards_in_hand:
                    print('  ', card)
            if player.cards_played:
                print(' played:'.format(i))
                for card in player.cards_played:
                    print('  ', card)

        # moves = self.get_current_player_valid_moves()
        # for move in moves:
        #     print(move)
        # print('{} moves available'.format(len(moves)))

    def get_valid_moves(self, player_index):

        moves = []
        provisional_moves = []  # moves that take gems, will need checking later
        player = self.players[player_index]

        # Moves that take gems
        # 1) taking two of the same colour
        for colour in colours:
            if self.num_gems_available(colour) >= 4:
                provisional_moves.append(('gems', {colour: 2}))
        # 2) taking up to three different colours
        available_colours = [colour for colour in colours if self.num_gems_available(colour) > 0]
        # for ps in list(set(permutations(available_colours, min(3, len(available_colours))))):
        #     provisional_moves.append(('gems', {p: 1 for p in ps}))
        for selection in choose_3(available_colours):
            provisional_moves.append(('gems', {c: 1 for c in selection}))

        num_gem_moves = len(provisional_moves)

        # Moves that reserve cards
        if player.num_reserved < 3:
            gold_gained = 1 if self.num_gems_available('gold') > 0 else 0
            for tier in range(1, 4):
                for i in range(len(self.cards_in_market(tier))):
                    provisional_moves.append(('reserve', tier, i, {'gold': gold_gained}))
                if self.cards_in_deck(tier, ensure_copied=False):
                    provisional_moves.append(('reserve', tier, -1, {'gold': gold_gained}))

        num_reserve_moves = len([m for m in provisional_moves if m[0] == 'reserve'])

        # Moves that buy available cards
        buy_moves = []
        for tier in range(1, 4):
            for index, card in enumerate(self.cards_in_market(tier)):
                can_afford, cost = player.can_afford(card)
                if not can_afford:
                    continue
                buy_moves.append(('buy_available', tier, index, {c: -1 * v for c, v in cost.items()}))

        # Moves that buy reserved cards
        for index, card in enumerate(player.cards_in_hand):
            can_afford, cost = player.can_afford(card)
            if not can_afford:
                continue
            buy_moves.append(('buy_reserved', index, {c: -1 * v for c, v in cost.items()}))

        if buy_moves:
            buy_multiplier = max(1, (num_gem_moves + num_reserve_moves) / len(buy_moves))
            buy_multiplier = int(np.round(buy_multiplier))
            for move in buy_moves:
                for _ in range(buy_multiplier):
                    moves.append(move)
        # for move in buy_moves:
        #     moves.append(move)

        # If taking gems leaves us with more than 10, discard any
        # possible gem combination
        player_gems = player.gems
        for move in provisional_moves:
            if move[0] == 'gems':
                num_gems_gained = sum(move[1].values())
                if player.total_num_gems + num_gems_gained <= 10:
                    moves.append(move)
                    continue
                num_gems_to_lose = player.total_num_gems + num_gems_gained - 10

                gems_gained = move[1]
                new_gems = {c: (player_gems[c] + gems_gained.get(c, 0)) for c in (colours + ['gold'])}
                possible_discards = discard_to_n_gems(new_gems, 10)
                for discard in possible_discards:
                    new_gems_gained = {key: value for key, value in gems_gained.items()}
                    for key, value in discard.items():
                        if key not in new_gems_gained:
                            new_gems_gained[key] = 0
                        new_gems_gained[key] += value
                    moves.append(('gems', new_gems_gained))

                    # print(num_gems_to_lose, -1 * sum(discard.values()))
                    if num_gems_to_lose != -1 * sum(discard.values()):
                        import ipdb
                        ipdb.set_trace()
                    assert -1 * sum(discard.values()) == num_gems_to_lose

            elif move[0] == 'reserve':
                num_gems_gained = sum(move[3].values())
                if player.total_num_gems + num_gems_gained <= 10:
                    moves.append(move)
                    continue
                for colour in colours + ['gold']:
                    new_gems_dict = {key: value for key, value in move[3].items()}
                    if player.num_gems(colour) > 0:
                        if colour not in new_gems_dict:
                            new_gems_dict[colour] = 0
                        new_gems_dict[colour] -= 1
                        moves.append(('reserve', move[1], move[2], new_gems_dict))
                        
                # gems_list = set(player.gems_list() + gems_dict_to_list(move[3]))
                # for gem in gems_list:
                #     new_gems_dict = {key: value for key, value in move[3].items()}
                #     if gem not in new_gems_dict:
                #         new_gems_dict[gem] = 0
                #     new_gems_dict[gem] -= 1
                #     moves.append(('reserve', move[1], move[2], new_gems_dict))

        # if player.total_num_gems > 7:
        #     gems_moves = []
        #     other_moves = []
        #     gems_move_index = {}
        #     gems_move_keys = set()
        #     for move in moves:
        #         if move[0] == 'gems':
        #             gems_moves.append(move)
        #         else:
        #             other_moves.append(move)
        #     initial_num_gems_moves = len(gems_moves)
        #     for move in gems_moves:
        #         key = (move[1]['white'] if 'white' in move[1] else 0,
        #                move[1]['blue'] if 'blue' in move[1] else 0,
        #                move[1]['green'] if 'green' in move[1] else 0,
        #                move[1]['red'] if 'red' in move[1] else 0,
        #                move[1]['black'] if 'black' in move[1] else 0,
        #                move[1]['gold'] if 'gold' in move[1] else 0)
        #         gems_move_index[key] = move
        #         gems_move_keys.add(key)
        #     gems_moves = [gems_move_index[key] for key in gems_move_keys]
        #     final_num_gems_moves = len(gems_moves)
        #     # print('went from {} to {} gems moves'.format(initial_num_gems_moves,
        #     #                                              final_num_gems_moves))
        #     moves = gems_moves + other_moves

        if len(moves) == 0:
            print('passing')
            moves = [('gems', {})]

        return moves

    def get_current_player_valid_moves(self):
        return self.get_valid_moves(self.current_player_index)

    def get_state_vector(self, player_perspective_index=None):
        
        if player_perspective_index is None:
            raise ValueError('player_perspective_index is None')
            player_perspective_index = self.current_player_index

        return self.state_vector.from_perspective_of(player_perspective_index).copy()
        # return self.state_vector.vector.copy()



def discard_to_n_gems(gems, target, current_possibility={}, possibilities=None, colours=['white', 'blue', 'green', 'red', 'black']):
    if possibilities is None:
        return discard_to_n_gems(gems, target, current_possibility, colours=colours, possibilities=[])
    num_gems = sum(gems.values())

    if num_gems == target:
        possibilities.append(current_possibility)
        return possibilities
    if not colours:
        return possibilities
    assert num_gems >= target

    orig_current_possibility = {c: n for c, n in current_possibility.items()}

    colours = colours[:]
    colour = colours.pop()

    num_gems_of_colour = gems.get(colour, 0)
    for i in range(0, min(num_gems_of_colour, num_gems - target) + 1):
        current_gems = {c: n for c, n in gems.items()}
        current_gems[colour] -= i
        current_possibility = {c: n for c, n in orig_current_possibility.items()}
        current_possibility[colour] = -1 * i
        discard_to_n_gems(current_gems, target,
                          current_possibility=current_possibility,
                          possibilities=possibilities,
                          colours=colours)
        
    return possibilities


def choose_3(colours):
    choices = []
    for i, colour_1 in enumerate(colours):
        for j, colour_2 in enumerate(colours[i+1:]):
            j += i + 1
            for k, colour_3 in enumerate(colours[j+1:]):
                choices.append((colour_1, colour_2, colour_3))
            if len(colours) == 2:
                choices.append((colour_1, colour_2))
        if len(colours) == 1:
            choices.append((colour_1, ))

    return choices


def gems_dict_to_list(d):
    return (['white' for _ in range(d.get('white', 0))] +
            ['blue' for _ in range(d.get('blue', 0))] +
            ['green' for _ in range(d.get('green', 0))] +
            ['red' for _ in range(d.get('red', 0))] +
            ['black' for _ in range(d.get('black', 0))] +
            ['gold' for _ in range(d.get('gold', 0))])

def main():
    manager = GameState()
    manager.print_state()

if __name__ == "__main__":
    main()
