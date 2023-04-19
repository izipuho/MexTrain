#!/usr/bin/env python3

# TODO ugly printing with dict_values
class Tile:
    def __init__(self, numbers):
        self.numbers = numbers
        self.code = f'{numbers[0]}-{numbers[1]}'
        self.text = f'[{self.numbers[0]:>2}|{self.numbers[1]:>2}]'
        self.text_flipped = f'[{self.numbers[1]:>2}|{self.numbers[0]:>2}]'
        self.highlighted = False
        self.score = sum(numbers)
        if self.score == 0:
            self.score = 25

    def is_double(self):
        if self.numbers[0] == self.numbers[1]:
            print(f'{self.numbers} is double.')
            return True
        else:
            print(f'{self.numbers} not a double.')
            return False

    def flip(self):
        # print(f'Tile {self.text} will be flipped to {self.text_flipped}')
        self.numbers.reverse()
        self.text = f'[{self.numbers[0]:>2}|{self.numbers[1]:>2}]'
        self.text_flipped = f'[{self.numbers[1]:>2}|{self.numbers[0]:>2}]'

    def is_suitable(self, number):
        if number in self.numbers:
            # print(f'{self.numbers} vs {number}: ok!')
            if number == self.numbers[1]:
                self.flip()
            return True
        else:
            # print(f'{self.numbers} vs {number}: No!')
            return False

    def highlight(self):
        self.highlighted = True
        self.text.replace('[', '{').replace(']', '}')
        self.text_flipped.replace('[', '{').replace(']', '}')

    def dehighlight(self):
        self.highlighted = False
        self.text.replace('{', '[').replace('}', ']')
        self.text_flipped.replace('{', '[').replace('}', ']')

    def __repr__(self):
        return self.text

    def __str__(self):
        return f'Tile {self.numbers} scores {self.score} points.'


class Set:
    # tl = tile(in_max_tile)
    def __init__(self, max_tile):
        self.max_tile = max_tile  # [in_max_tile, in_max_tile]
        self.set = dict()
        self.set_repr = str()
        self.create()
        # print(self)

    def create(self):
        for t in range(self.max_tile, -1, -1):
            for i in range(t, -1, -1):
                tl = Tile([t, i])
                # print(tl)
                self.set[tl.code] = tl
                self.set_repr += str(tl) + ' '
            self.set_repr += '\n'

    def __str__(self):
        return f'Got set of {len(self.set)} tiles with {self.max_tile} highest.\n'

    def __repr__(self):
        return self.set_repr
