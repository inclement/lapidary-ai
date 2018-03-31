

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
        
def colour_values_to_card_text(**kwargs):
    values = []
    for colour in colours:
        if colour not in kwargs or kwargs[colour] == 0:
            continue
        values.append('{} {} {}'.format(''.join([Style.RESET_ALL,
                                                 text_bg_cols[colour],
                                                 Fore.BLACK]),
                                        str(kwargs[colour]),
                                        Style.RESET_ALL))
                                                 
    values = ['   ' for _ in range(5 - len(values))] + values
    return values
            

def print_iterables(*iterables):
    for text in line_round_robin(*iterables, padding=3):
        if text is not None:
            sys.stdout.write(text)
            sys.stdout.flush()

# print_iterables(card_to_str(tier_1[0]))



