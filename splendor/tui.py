

from nn import H50AI_TDlam
from game import GameState, tier_1, tier_2, tier_3, all_cards
from data import colours, colours_dict

from colorama import Style, Fore, Back
from itertools import cycle, islice, repeat
import sys

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
        text.append('{} {} '.format(
            ''.join([Style.RESET_ALL,
                     text_bg_cols[colour],
                     text_fg_cols[colour]]),
            str(gems.get(colour, 0))))
        text.append(Style.RESET_ALL)
        text.append(' ')

    text.append(Style.RESET_ALL)

    text.append(' ({} total)'.format(total))

    print(''.join(text))

def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--num-players', default=2, type=int)

    args = parser.parse_args(sys.argv[1:])

    run_game(num_players=args.num_players)


def run_game(num_players=2, validate=True):
    state = GameState(players=num_players,
                      init_game=True,
                      validate=validate)

    ai = H50AI_TDlam(restore=True, stepsize=0,
                     prob_factor=100, num_players=2)

    print_game_state(state, player_index=0, ai=ai)

def print_game_state(state, player_index=0, ai=None):
    print()
    print('=====================================')
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

if __name__ == "__main__":
    main()

