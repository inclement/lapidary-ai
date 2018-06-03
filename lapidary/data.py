

colours = ['white', 'blue', 'green', 'red', 'black']
all_colours = colours + ['gold']

colour_indices = {colour: index for index, colour in enumerate(colours)}
colour_indices['none'] = len(colours)

colours_dict = {'white': (0.9, 0.9, 0.9, 1),
                'blue': (0.6, 0.6, 1.0, 1),
                'green': (0.3, 0.9, 0.3, 1),
                'red': (1.0, 0.4, 0.4, 1),
                'black': (0.6, 0.6, 0.6, 1),
                'gold': (0.941, 0.902, 0.529, 1)}

border_colours_dict = {'white': (1, 1, 1, 1),
                       'blue': (0, 0, 1, 1),
                       'green': (0, 1, 0, 1),
                       'red': (1, 0, 0, 1),
                       'black': (0, 0, 0, 1),
                       'gold': (1, 0.843, 0, 1)}
