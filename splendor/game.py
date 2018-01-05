import random
from itertools import permutations
import numpy as np

from data import colours

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

    def __str__(self):
        return '<Card T={} P={} {}>'.format(
            self.tier, self.points, ','.join(
                ['{}:{}'.format(colour, getattr(self, colour)) for colour in ('white', 'blue', 'green', 'red', 'black') if getattr(self, colour)]))

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

    def __str__(self):
        return '<Noble P={} {}>'.format(
            self.points, ','.join(
                ['{}:{}'.format(colour, getattr(self, colour)) for colour in ('white', 'blue', 'green', 'red', 'black') if getattr(self, colour)]))

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

    Card(3, 'red', 3, white=3, blue=5, green=3, black=5),
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

        self.gold = 0
        self.white = 0
        self.blue = 0
        self.green = 0
        self.red = 0
        self.black = 0

    @property
    def num_gems(self):
        return (self.gold + self.white + self.blue + self.green +
                self.red + self.black)

    @property
    def gems(self):
        return {'white': self.white,
                'blue': self.blue,
                'green': self.green,
                'red': self.red,
                'black': self.black,
                'gold': self.gold}

    def gems_list(self):
        return (['white' for _ in range(self.white)] + 
                ['blue' for _ in range(self.blue)] +
                ['green' for _ in range(self.green)] +
                ['red' for _ in range(self.red)] +
                ['black' for _ in range(self.black)] +
                ['gold' for _ in range(self.gold)])

    def add_gems(self, **kwargs):
        for kwarg in kwargs:
            assert hasattr(self, kwarg)
            setattr(self, kwarg, getattr(self, kwarg) + kwargs[kwarg])

    @property
    def num_reserved(self):
        return len(self.cards_in_hand)

    @property
    def score(self):
        score = 0
        for card in self.cards_played:
            score += card.points

        # TODO: Add and score nobles too
        return score

    def num_cards_of_colour(self, colour):
        number = 0
        for card in self.cards_played:
            if card.colour == colour:
                number += 1
        return number

    def can_afford(self, card):
        missing_colours = [max(getattr(card, colour) -
                               getattr(self, colour) -
                               self.num_cards_of_colour(colour), 0)
                           for colour in colours]

        if sum(missing_colours) > self.gold:
            return False, None

        cost = {colour: max(min(getattr(self, colour),
                                getattr(card, colour) -
                                self.num_cards_of_colour(colour)), 0) for colour in colours}
        cost['gold'] = sum(missing_colours)

        # TODO: Allow gold to be used instead of coloured gems, if available

        return True, cost

    def verify_state(self):
        assert 0 <= self.num_gems <= 10
        assert len(self.cards_in_hand) <= 3
        assert len(set(self.nobles)) == len(self.nobles)

        for colour in colours + ['gold']:
            assert getattr(self, colour) >= 0


class GameState(object):

    def __init__(self, players=3):
        self.num_players = players
        self.players = [Player() for _ in range(players)]
        self.current_player_index = 0

        self.num_gems_in_play = {2: 4, 3: 5, 4: 7}[players]
        self.num_dev_cards = 4
        self.num_nobles = {2:3, 3:4, 4:5}[players]

        self.tier_1 = tier_1[:]
        self.tier_2 = tier_2[:]
        self.tier_3 = tier_3[:]

        self.tier_1_visible = []
        self.tier_2_visible = []
        self.tier_3_visible = []

        self.num_gold_available = 5
        self.num_white_available = self.num_gems_in_play
        self.num_blue_available = self.num_gems_in_play
        self.num_green_available = self.num_gems_in_play
        self.num_red_available = self.num_gems_in_play
        self.num_black_available = self.num_gems_in_play

        self.nobles = []

        self.generator = random.Random()

        self.init_game()

    def get_scores(self):
        scores = [player.score for player in self.players]
        return scores

    @property
    def current_player(self):
        return self.players[self.current_player_index]

    def num_gems_available(self, colour):
        return getattr(self, 'num_{}_available'.format(colour))

    def total_num_gems_available(self):
        return sum([self.num_gems_available(colour) for colour in colours])

    def update_gems(self, colour, change):
        attr_name = 'num_{}_available'.format(colour)
        setattr(self, attr_name, getattr(self, attr_name) + change)

    def cards_available_in(self, tier):
        return getattr(self, 'tier_{}_visible'.format(tier))

    def seed(self):
        self.generator.seed(seed)

    def init_game(self):
        # Shuffle the cards
        self.generator.shuffle(self.tier_1)
        self.generator.shuffle(self.tier_2)
        self.generator.shuffle(self.tier_3)

        # Select nobles
        orig_nobles = nobles[:]
        print('before', orig_nobles)
        self.generator.shuffle(orig_nobles)
        print('after', orig_nobles)
        self.nobles = orig_nobles[:self.num_nobles]
        self.initial_nobles = self.nobles[:]

        # Update visible dev cards
        self.update_dev_cards()

    def make_move(self, move):
        player = self.players[self.current_player_index]
        if move[0] == 'gems':
            for colour, change in move[1].items():
                self.update_gems(colour, -1 * change)
            player.add_gems(**move[1])

        elif move[0] == 'buy_available':
            action, tier, index, gems = move
            card = self.cards_available_in(tier).pop(index)
            player.cards_played.append(card)
            player.add_gems(**gems)
            for colour, change in gems.items():
                self.update_gems(colour, -1 * change)

        elif move[0] == 'buy_reserved':
            action, index, gems = move
            card = player.cards_in_hand.pop(index)
            player.cards_played.append(card)
            player.add_gems(**gems)
            for colour, change in gems.items():
                self.update_gems(colour, -1 * change)

        elif move[0] == 'reserve':
            action, tier, index, gems = move
            if index == -1:
                card = getattr(self, 'tier_{}'.format(tier)).pop()
            else:
                card = self.cards_available_in(tier).pop(index)
            player.cards_in_hand.append(card)
            player.add_gems(**gems)
            for colour, change in gems.items():
                self.update_gems(colour, -1 * change)

        else:
            raise ValueError('Received invalid move {}'.format(move))

        # Clean up the state
        self.update_dev_cards()

        # Check that everything is within expected parameters
        try:
            player.verify_state()
            self.verify_state()
        except AssertionError:
            # TODO: Fix known bug with invalid moves being generated and triggering this
            print('Failure verifying state after making move')
            import ipdb; ipdb.set_trace()

        self.current_player_index += 1
        self.current_player_index %= len(self.players)

        # TODO: Add noble selection/assignment

    def verify_state(self):
        for colour in colours:
            assert 0 <= self.num_gems_available(colour) <= self.num_gems_in_play
        assert 0 <= self.num_gems_available('gold') <= 5

        for colour in colours:
            assert self.num_gems_available(colour) + sum([getattr(player, colour) for player in self.players]) == self.num_gems_in_play

    def update_dev_cards(self):
        while len(self.tier_1_visible) < 4 and self.tier_1:
            self.tier_1_visible.append(self.tier_1.pop())

        while len(self.tier_2_visible) < 4 and self.tier_2:
            self.tier_2_visible.append(self.tier_2.pop())

        while len(self.tier_3_visible) < 4 and self.tier_3:
            self.tier_3_visible.append(self.tier_3.pop())

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
            print('  {}: {}'.format(colour, getattr(self, 'num_{}_available'.format(colour))))
        print()

        for i, player in enumerate(self.players):
            i += 1
            print('Player {}:'.format(i))
            for colour in colours:
                print('  {}: {}'.format(colour, getattr(player, colour)))
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
                moves.append(('gems', {colour: 2}))
        # 2) taking up to three different colours
        available_colours = [colour for colour in colours if self.num_gems_available(colour) > 0]
        for ps in permutations(available_colours, len(available_colours)):
            ps = ps[:3]  # take only up to 3 gems
            provisional_moves.append(('gems', {p: 1 for p in ps}))

        # Moves that buy available cards
        for tier in range(1, 4):
            for index, card in enumerate(self.cards_available_in(tier)):
                can_afford, cost = player.can_afford(card)
                if not can_afford:
                    continue
                moves.append(('buy_available', tier, index, {c: -1 * v for c, v in cost.items()}))

        # Moves that buy reserved cards
        for index, card in enumerate(player.cards_in_hand):
            can_afford, cost = player.can_afford(card)
            if not can_afford:
                continue
            moves.append(('buy_reserved', index, {c: -1 * v for c, v in cost.items()}))

        # Moves that reserve cards
        if player.num_reserved < 3:
            gold_gained = 1 if self.num_gold_available > 0 else 0
            for tier in range(1, 4):
                for i in range(len(self.cards_available_in(tier))):
                    provisional_moves.append(('reserve', tier, i, {'gold': gold_gained}))
                if getattr(self, 'tier_{}'.format(tier)):
                    provisional_moves.append(('reserve', tier, -1, {'gold': gold_gained}))
        

        # If taking gems leaves us with more than 10, discard any
        # possible gem combination
        player_gems = player.gems
        for move in provisional_moves:
            if move[0] == 'gems':
                num_gems_gained = sum(move[1].values())
                if player.num_gems + num_gems_gained <= 10:
                    moves.append(move)
                    continue
                num_gems_to_lose = player.num_gems + num_gems_gained - 10

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
                if player.num_gems + num_gems_gained <= 10:
                    moves.append(move)
                    continue
                gems_list = set(player.gems_list() + gems_dict_to_list(move[3]))
                for gem in gems_list:
                    new_gems_dict = {key: value for key, value in move[3].items()}
                    if gem not in new_gems_dict:
                        new_gems_dict[gem] = 0
                    new_gems_dict[gem] -= 1
                    moves.append(('reserve', move[1], move[2], new_gems_dict))

        return moves

    def get_current_player_valid_moves(self):
        return self.get_valid_moves(self.current_player_index)

    def get_state_vector(self):
        '''Get the current game state as a vector of 1s and 0s, for the neural net.
        '''

        all_cards = tier_1 + tier_2 + tier_3
        num_cards = len(all_cards)

        ordered_players = self.players[self.current_player_index:] + self.players[:self.current_player_index]

        # store card locations
        card_locations = [0 for _ in range(num_cards * (2 + len(self.players)))]
        for i, card in enumerate(all_cards):
            if card in self.tier_1 or card in self.tier_2 or card in self.tier_3:
                card_locations[i] = 1
            elif card in self.tier_1_visible or card in self.tier_2_visible or card in self.tier_3_visible:
                card_locations[i + num_cards] = 1
            else:
                for pi, player in enumerate(ordered_players):
                    if card in player.cards_in_hand:
                        card_locations[i + 2 + pi] = 1
                
        # store numbers of gems in the supply
        num_colour_gems_in_play = self.num_gems_in_play
        gem_nums_in_supply = [0 for _ in range(5 * (num_colour_gems_in_play + 1))]
        for i, colour in enumerate(colours):
            available = self.num_gems_available(colour)
            gem_nums_in_supply[(num_colour_gems_in_play + 1)*i + available] = 1

        gold_nums_in_supply = [0 for _ in range(6)]
        gold_nums_in_supply[self.num_gems_available('gold')] = 1

        # store numbers of gems held by each player
        all_player_gems = []
        for player in ordered_players:
            player_gems = [0 for _ in range(5 * (num_colour_gems_in_play + 1))]
            for i, colour in enumerate(colours):
                num_gems = getattr(player, colour)
                player_gems[(num_colour_gems_in_play + 1)*i + num_gems] = 1
            all_player_gems.extend(player_gems)
            player_gold_gems = [0 for _ in range(5)]
            player_gold_gems[getattr(player, 'gold')] = 1
            all_player_gems.extend(player_gold_gems)
                

        # store numbers of coloured cards played by each player
        # only count up to 7 - more than this makes no difference
        all_player_cards = []
        for player in ordered_players:
            player_cards = [0 for _ in range(5 * 8)]
            for i, colour in enumerate(colours):
                num_cards = player.num_cards_of_colour(colour)
                player_cards[8 * i + min(num_cards, 7)] = 1
            all_player_cards.extend(player_cards)

        # store number of points of each player
        # only count up to 20, higher scores are very unlikely
        player_scores = [0 for _ in range(21 * len(ordered_players))]
        for i, player in enumerate(ordered_players):
            player_scores[i * 21 + min(player.score, 20)] = 1

        # store number of nobles in the game, and available
        nobles_in_game = [0 for _ in nobles]
        nobles_available = [0 for _ in nobles]
        nobles_claimed = [0 for _ in nobles for player in ordered_players]
        for i, noble in enumerate(nobles):
            if noble in self.initial_nobles:
                print('noble', i, 'in game')
                nobles_in_game[i] = 1
                if noble in self.nobles:
                    nobles_available[i] = 1
                    continue
                for pi, player in enumerate(ordered_players):
                    if noble in player.nobles:
                        nobles_claimed[len(self.initial_nobles)*pi + i] = 1
                

        return np.array(card_locations + gem_nums_in_supply + gold_nums_in_supply +
                        all_player_gems + all_player_cards + player_scores +
                        nobles_in_game + nobles_available + nobles_claimed)
        


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
