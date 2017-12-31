

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
        
        self.white = white
        self.blue = blue
        self.green = green
        self.red = red
        self.black = black

    @property
    def requirements(self):
        return (self.white, self.blue, self.green, self.red, self.black)
                 
class Noble(object):
    def __init__(self, points=3, white=0, blue=0, green=0, red=0, black=0):
        self.points = points

        self.white = white
        self.blue = blue
        self.green = green
        self.red = red
        self.black = black

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


class GameManager(object):
    pass
