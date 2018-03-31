

from nn import H50AI_TDlam
from game import GameState, tier_1, tier_2, tier_3, all_cards
from data import colours, colours_dict

from colorama import Style, Fore, Back
from itertools import cycle, islice, repeat
import sys
from collections import defaultdict

def line_round_robin(*iterables, padding=0):
    # Modified from recipe credited to George Sakkis
    num_active = len(iterables)

    real_iterables = []
    for iterable in iterables:
        real_iterables.append(iterable)
        real_iterables.append(iter_padding(padding))
    iterables = real_iterables[:-1]
    iterables.append(repeat('\n'))
        

    nexts = cycle(iter(it).__next__ for it in iterables)
    try:
        for next in nexts:
            yield next()
    except StopIteration:
        # Remove the iterator we just exhausted from the cycle.
        return
        # num_active -= 1
        # nexts = cycle(islice(nexts, num_active))

def iter_padding(spaces):
    return repeat(' ' * spaces)

def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    num_active = len(iterables)
    nexts = cycle(iter(it).__next__ for it in iterables)
    while num_active:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            # Remove the iterator we just exhausted from the cycle.
            num_active -= 1
            nexts = cycle(islice(nexts, num_active))
bg_cols = {'white': Back.LIGHTWHITE_EX,
           'blue': Back.LIGHTBLUE_EX,
           'green': Back.LIGHTGREEN_EX,
           'red': Back.LIGHTRED_EX,
           'black': Back.LIGHTBLACK_EX}
fg_cols = {'white': Fore.WHITE,
           'blue': Fore.BLUE,
           'green': Fore.GREEN,
           'red': Fore.RED,
           'black': Fore.LIGHTBLACK_EX,
           'gold': Fore.LIGHTYELLOW_EX}
text_bg_cols = {'white': Back.LIGHTWHITE_EX,
                'blue': Back.LIGHTBLUE_EX,
                'green': Back.LIGHTGREEN_EX,
                'red': Back.LIGHTRED_EX,
                'black': Back.LIGHTBLACK_EX,
                'gold': Back.LIGHTYELLOW_EX}
text_fg_cols = {'white': Fore.BLACK,
                'blue': Fore.BLACK,
                'green': Fore.BLACK,
                'red': Fore.BLACK,
                'black': Fore.WHITE,
                'gold': Fore.BLACK}
                
           
def coloured_row(length, colour):
    return '{}{}{}'.format(bg_cols[colour],
                           ' ' * length,
                           Back.RESET)

def coloured_row_pad(before, text, after, colour):
    before_text = '{}{}'.format(bg_cols[colour],
                                  ' ' * before,
                                  )

    after_text = '{}{}{}'.format(bg_cols[colour],
                                 ' ' * after,
                                 Back.RESET)
    
    return ''.join([before_text, text, after_text])

def spacer(length, height):
    for _ in range(height):
        yield ' ' * length

def card_to_strs(card, v_pad=1, h_pad=1):
    
    num_data_rows = 5
    num_data_columns = 6
    num_columns = num_data_columns + h_pad * 2

    for i in range(v_pad):
        yield coloured_row(num_columns, card.colour)

    colour_text = colour_values_to_card_text(
        **{colour: card.num_required(colour) for colour in colours})

    # points
    yield coloured_row_pad(4,
                           '{} {} '.format(Style.RESET_ALL,
                                           ''.join([Style.RESET_ALL,
                                                    Fore.LIGHTWHITE_EX,
                                                    Style.BRIGHT,
                                                    str(card.points)])),
                           1,
                           card.colour)

    for text in colour_text[1:]:
        yield coloured_row_pad(1, text, 4, card.colour)
        # yield coloured_row(num_columns, card.colour)

    for i in range(v_pad):
        yield coloured_row(num_columns, card.colour)

def label_to_strs(label, width, height):
    if height % 2 == 0:
        lines_before_label = height // 2 - 1
    else:
        lines_before_label = int(height / 2)
    
    for _ in range(lines_before_label):
        yield ' ' * width
    yield (' ' * (width - len(label)) +
           ''.join([Style.RESET_ALL,
                    Fore.WHITE,
                    Style.BRIGHT]) +
           label)

    for _ in range(height - 1 - lines_before_label):
        yield ' ' * width
    
        
def colour_values_to_card_text(**kwargs):
    values = []
    for colour in colours:
        if colour not in kwargs or kwargs[colour] == 0:
            continue
        values.append('{} {} {}'.format(''.join([Style.RESET_ALL,
                                                 text_bg_cols[colour],
                                                 text_fg_cols[colour]]),
                                        str(kwargs[colour]),
                                        Style.RESET_ALL))
                                                 
    values = ['   ' for _ in range(5 - len(values))] + values
    return values
            

def print_iterables(*iterables):
    for text in line_round_robin(*iterables, padding=3):
        if text is not None:
            sys.stdout.write(text)
            sys.stdout.flush()

def print_card_list(cards, name=''):
    print_iterables(*([label_to_strs(name, width=5, height=7)] +
                      [card_to_strs(card) for card in cards]))

def print_gems_list(name='', **gems):

    total = 0

    text = []
    text.append(Style.BRIGHT)
    text.append(Fore.WHITE)
    text.append(' ' * (7 - len(name)) + name)

    text.append(' ')

    for colour in colours + ['gold']:
        total += gems.get(colour, 0)
        num_gems = gems.get(colour, 0)
        num_cards = gems.get(colour + '_cards', 0)
        text.append('{} {}{} '.format(
            ''.join([Style.RESET_ALL,
                     text_bg_cols[colour],
                     text_fg_cols[colour]]),
            str(gems.get(colour, 0)),
            (' ({})'.format(num_cards)) if num_cards > 0 else '',
        ))
        text.append(Style.RESET_ALL)
        text.append(' ')

    text.append(Style.RESET_ALL)

    text.append(' ({} total)'.format(total))

    print(''.join(text))

def print_nobles(nobles, name=''):

    text = []

    text.append(Style.BRIGHT)
    text.append(Fore.WHITE)
    text.append(name + ' ')
    text.append(Style.RESET_ALL)

    for noble in nobles:
        text.append('< ')
        text.append('{} points '.format(noble.points))
        for colour in colours:
            if not noble.num_required(colour):
                continue
            text.append('{} {} {} '.format(
                ''.join([Style.RESET_ALL,
                         text_bg_cols[colour],
                         text_fg_cols[colour]]),
                str(noble.num_required(colour)),
                Style.RESET_ALL))
        text.append('> ')

    print(''.join(text))

def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--num-players', default=2, type=int)
    parser.add_argument('--player-index', default=0)
    parser.add_argument('--ai-autoplay', default=False, action='store_true')

    args = parser.parse_args(sys.argv[1:])

    ai_player_indices = list(range(args.num_players))
    ai_player_indices.remove(args.player_index)
    run_game(num_players=args.num_players,
             ai_player_indices=ai_player_indices)


def run_game(num_players=2, validate=True, ai_player_indices=[1]):
    state = GameState(players=num_players,
                      init_game=True,
                      validate=False)

    ai = H50AI_TDlam(restore=True, stepsize=0,
                     prob_factor=100, num_players=2)

    while True:
        print_game_state(state, player_index=0, ai=ai)

        if validate:
            state.verify_state()

        winner = check_winner(state)
        if winner is not None:
            print(Style.BRIGHT + Fore.WHITE)
            print('Player {} wins with {} points'.format(
                winner + 1,
                state.players[winner].score))
            exit(0)

        if state.current_player_index in ai_player_indices:
            move, move_info = ai.make_move(state)
            state.make_move(move)
        
        else:
            do_player_move(state, ai)

        # If the player has too many gems, discard some
        discard_to_ten_gems(state)


def discard_to_ten_gems(state):
    player_index = (state.current_player_index - 1) % len(state.players)
    player = state.players[player_index]

    if player.total_num_gems <= 10:
        return

    num_to_discard = player.total_num_gems - 10
    while True:
        # print gems in supply
        print()
        print_gems_list(**{colour: state.num_gems_available(colour)
                        for colour in colours + ['gold']},
                        name='supply:')

        print()
        print()

        # print player gems
        for i, player_obj in enumerate(state.players):
            if i == player_index:
                name = 'you:'
            else:
                name = 'P{}:'.format(i + 1)
            print_gems_list(**{colour: player_obj.num_gems(colour)
                            for colour in colours + ['gold']},
                            **{colour + '_cards': player_obj.num_cards_of_colour(colour)
                            for colour in colours},
                            name=name)
            print()

        print('Need to discard {} gems'.format(num_to_discard))

        discards = input('>>> ')
        discards = discards.split(' ')
        if len(discards) != num_to_discard:
            print('Must discard exactly {}'.format(num_to_discard))
            continue

        gems_dict = defaultdict(lambda: 0)
        for discard in discards:
            if discard.startswith('w'):
                gems_dict['white'] += 1
            elif discard.startswith('blu'):
                gems_dict['blue'] += 1
            elif discard.startswith('gr'):
                gems_dict['green'] += 1
            elif discard.startswith('r'):
                gems_dict['red'] += 1
            elif discard.startswith('bla'):
                gems_dict['black'] += 1
            elif discard.startswith('go'):
                gems_dict['gold'] += 1
            else:
                print('Did not understand colour {}'.format(discard))
                continue

        for colour, value in gems_dict.items():
            if value > player.num_gems(colour):
                print('Tried to return {} {}, but only have {}'.format(
                      value, colour, player.num_gems(colour)))

                break
        else:
            break

    player.add_gems(**{key: -1 * value for key, value in gems_dict.items()})
    for colour, value in gems_dict.items():
        state.add_supply_gems(colour, value)
        state.state_vector.set_supply_gems(colour, state.num_gems_available(colour))
        state.state_vector.set_player_gems(player_index, colour, player.num_gems(colour))



def do_player_move(state, ai):
    while True:
        print('Enter a move:')
        move = input('>>> ')

        items = move.strip().split(' ')
        if items[0] == 'q':
            print('Exiting')
            exit(0)
        if items[0].startswith('res'):
            state_move = interpret_reserve(items, state)
        elif items[0] == 'buy':
            state_move = interpret_buy(items, state)
        elif items[0].startswith('gem'):
            state_move = interpret_gems(items, state)
        elif items[0] == 'ai':
            state_move, move_info = ai.make_move(state)
        else:
            state_move = None
        print()

        if state_move is None:
            print('Could not apply move `{}`'.format(move))
            continue

        break

        
        print('Move `{}` not understood'.format(move))
    state.make_move(state_move)

def interpret_gems(items, state):
    gems = items[1:]

    gems_dict = defaultdict(lambda: 0)
    for gem in gems:
        if gem.startswith('w'):
            gems_dict['white'] += 1
        elif gem.startswith('blu'):
            gems_dict['blue'] += 1
        elif gem.startswith('g'):
            gems_dict['green'] += 1
        elif gem.startswith('r'):
            gems_dict['red'] += 1
        elif gem.startswith('bla'):
            gems_dict['black'] += 1
        else:
            print('Could not interpret gem `{}`'.format(gem))
            return

    if len(gems_dict) > 1:
        for key, value in gems_dict.items():
            if value > 1:
                print('{} is not a valid gem selection'.format(gems_dict))
                return

    for key, value in gems_dict.items():
        if value > 2:
            print('{} is not a valid gem selection'.format(gems_dict))
            return

        if value == 2 and state.num_gems_available(key) < 4:
            print('Cannot take {} {} gems, {} available'.format(
                value, key, state.num_gems_available(key)))

        if value > state.num_gems_available(key):
            print('Cannot take {} {} gems, {} available'.format(
                value, key, state.num_gems_available(key)))
            return

    state_move = ('gems', gems_dict)
    return state_move
    
        
def interpret_buy(items, state):
    if len(items) != 3:
        print('Did not understand what card to buy from {}'.format(items))
        return

    move, tier, index = items

    if tier != 'hand':
        if (len(tier) > 1 and tier[0] not in ['T', 't']) or len(tier) > 2:
            print('Did not understand card location `{}`'.format(items[1]))
            return


    if not tier[0] == 'h':
        try:
            tier = int(tier[-1])
        except ValueError:
            print('Error turning iter {} into int'.format(tier))
            return
    else:
        tier = 'hand'

    try:
        index = int(index)
    except ValueError:
        print('Error turning index {} into int'.format(index))

    if tier != 'hand':
        cards = state.cards_in_market(tier)
    else:
        cards = state.current_player.cards_in_hand
    if index >= len(cards):
        print('Index {} too high for cards list {}'.format(index, cards))
        return

    card = cards[index]

    can_afford, cost = state.current_player.can_afford(card)
    if not can_afford:
        print('You cannot afford the card {}'.format(card))
        return

    cost = {key: -1 * value for key, value in cost.items()}
    if tier == 'hand':
        state_move = ('buy_reserved', index, cost)
    else:
        state_move = ('buy_available', tier, index, cost)

    return state_move
        

def interpret_reserve(items, state):

    if len(state.current_player.cards_in_hand) >= 3:
        print('Cannot reserve, already have 3 cards in hand')
        return

    if len(items) != 3:
        print('Did not understand what card to reserve from {}'.format(items))
        return
    
    move, tier, index = items
    if len(tier) > 2 or (len(tier) == 2 and tier[0] not in ('t', 'T')):
        print('Did not understand tier', tier)
        return
    
    try:
        tier = int(tier[-1])
    except ValueError:
        print('Error turning tier {} into int'.format(tier))
        return
    
    try:
        index = int(index)
    except ValueError:
        print('Error turning index {} into int'.format(index))
        return
        
    if index > len(state.cards_in_market(tier)):
        print('index {} is too high for tier {}'.format(index, tier))
        return

    gems_dict = {}
    if state.num_gems_available('gold') > 0:
        gems_dict['gold'] = 1
    state_move = ('reserve', tier, index, gems_dict)

    return state_move


                                                         
def check_winner(state):
    for i, player in enumerate(state.players):
        if player.score >= 15:
            return i
    return None

def print_game_state(state, player_index=0, ai=None):
    print(Style.RESET_ALL)
    print(Style.BRIGHT)
    print('=====================================')
    print('    Round {} player {}'.format(state.round_number,
                                          state.current_player_index + 1))
    print('=====================================')
    print(Style.RESET_ALL)

    # print score
    for i, player in enumerate(state.players):
        print('    {}{}P{}: {} points'.format(
            Fore.WHITE, Style.BRIGHT, i + 1, player.score))
    print()

    # print nobles
    print_nobles(state.nobles, name='Nobles:')
    for i, player in enumerate(state.players):
        print_nobles(player.nobles, name='P{}:'.format(i + 1))
    print()

    # print cards available
    for tier in range(3, 0, -1):
        cards = state.cards_in_market(tier)
        print_card_list(cards, name='T{}:'.format(tier))
        print()

    print()

    # print gems in supply
    print_gems_list(**{colour: state.num_gems_available(colour)
                       for colour in colours + ['gold']},
                    name='supply:')

    print()
    print()

    # print player gems
    for i, player in enumerate(state.players):
        if i == player_index:
            name = 'you:'
        else:
            name = 'P{}:'.format(i + 1)
        print_gems_list(**{colour: player.num_gems(colour)
                           for colour in colours + ['gold']},
                        **{colour + '_cards': player.num_cards_of_colour(colour)
                           for colour in colours},
                        name=name)
        print()

    # print player hands
    for i, player in enumerate(state.players):
        if i == player_index:
            print_card_list(player.cards_in_hand,
                            name='hand:')
        else:
            print('{}    (Player {} holds {} cards)'.format(
                Style.RESET_ALL,
                i + 1,
                len(player.cards_in_hand)))
        print()

    # print ai evaluations
    if ai is not None:
        assert len(state.players) == 2
        values = ai.evaluate(state)
        print('    AI P1 evaluations: {:.03f} {:.03f}'.format(values[0, 0],
                                                              values[1, 1]))
        print('    AI P2 evaluations: {:.03f} {:.03f}'.format(values[0, 1],
                                                              values[1, 0]))
    print()
    
    # print last move
    if state.moves:
        last_move = state.moves[-1]
        last_player_index = (state.current_player_index - 1) % len(state.players)
        if last_move[0] == 'gems':
            last_move_info = 'gained gems ' + str(last_move[1])
        elif last_move[0].startswith('buy_'):
            previous_player_index = (state.current_player_index - 1) % len(state.players)
            card = state.players[previous_player_index].cards_played[-1]
            last_move_info = 'bought {}'.format(card)
        elif last_move[0] == 'reserve':
            last_move_info = 'reserved from tier {}'.format(last_move[1])
        print('P{} {}'.format(last_player_index + 1, last_move_info))

    print()

if __name__ == "__main__":
    main()

