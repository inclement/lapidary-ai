import random
from itertools import permutations

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
    def num_reserved(self):
        return len(self.cards_in_hand)

    @property
    def score(self):
        score = 0
        for card in self.cards_played:
            score += card.points
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

        cost = {colour: min(getattr(self, colour),
                            getattr(card, colour) -
                            self.num_cards_of_colour(colour)) for colour in colours}
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

        self.num_gems = {2: 4, 3: 5, 4: 7}[players]
        self.num_dev_cards = 4
        self.num_nobles = {2:3, 3:4, 4:5}[players]

        self.tier_1 = tier_1[:]
        self.tier_2 = tier_2[:]
        self.tier_3 = tier_3[:]

        self.tier_1_visible = []
        self.tier_2_visible = []
        self.tier_3_visible = []

        self.num_gold_available = 5
        self.num_white_available = 10
        self.num_blue_available = 10
        self.num_green_available = 10
        self.num_red_available = 10
        self.num_black_available = 10

        self.nobles = []

        self.generator = random.Random()

        self.init_game()

    def get_winner(self):
        for index, player in enumerate(self.players):
            if player.score >= 15:
                return index

    @property
    def current_player(self):
        return self.players[self.current_player_index]

    def num_gems_available(self, colour):
        return getattr(self, 'num_{}_available'.format(colour))

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
        orig_nobles = nobles
        self.generator.shuffle(orig_nobles)
        self.nobles = orig_nobles[:self.num_nobles]

        # Update visible dev cards
        self.update_dev_cards()

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
        print('{} tier 1 remain'.format(len(self.tier_2)))
        print()

        print('Tier 3 visible:')
        for card in self.tier_3_visible:
            print(card)
        print('{} tier 1 remain'.format(len(self.tier_3)))
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

        moves = self.get_current_player_valid_moves()
        for move in moves:
            print(move)
        print('{} moves available'.format(len(moves)))

    def get_valid_moves(self, player_index):

        moves = []
        player = self.players[player_index]

        # Moves that take gems
        # 1) taking two of the same colour
        for colour in colours:
            if self.num_gems_available(colour) >= 4:
                moves.append(('gems', {colour: 2}))
        # 2) taking up to three different colours
        available_colours = [c for c in colours if self.num_gems_available(colour) > 0]
        for ps in permutations(available_colours, len(available_colours)):
            ps = ps[:3]  # take only up to 3 gems
            moves.append(('gems', {p: 1 for p in ps}))

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
                for i in range(4):
                    moves.append(('reserve', tier, i, {'gold': gold_gained}))
                moves.append(('reserve', tier, -1, {'gold': gold_gained}))
        

        # If taking gems leaves us with more than 10, discard any
        # possible gem combination
        for move in moves:
            if move[0] == 'gems':
                num_gems_gained = sum(move[1].values())
                if player.num_gems + num_gems_gained <= 10:
                    continue
                pass  # TODO: discard if necessary
            elif move[0] == 'reserve':
                num_gems_gained = sum(move[3].values())
                if player.num_gems + num_gems_gained <= 10:
                    continue
                pass  # TODO: discard if necessary

        return moves

    def get_current_player_valid_moves(self):
        return self.get_valid_moves(self.current_player_index)

def main():
    manager = GameState()
    manager.print_state()

if __name__ == "__main__":
    main()
