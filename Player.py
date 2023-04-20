#!/usr/bin/env python3

class Player:
    def __init__(self, name, difficulty = -1):
        self.name = name
        if difficulty in ('easy', 'e', '1', 3):
            self.difficulty = 'easy'
        elif difficulty in ('normal', 'n', '2', 2):
            self.difficulty = 'normal'
        elif difficulty in ('hard', 'h', '3', 3):
            self.difficulty = 'hard'
        else:
            self.difficulty = 'manual'
        pass

    def __str__(self):
        player_str = f'{self.name}'
        if self.difficulty != 'manual':
            player_str += f' ({self.difficulty})'
        return player_str

    def __repr__(self):
        player_str = f'{self.name}.'
        if self.difficulty != 'manual':
            player_str += f' Played by computer with {self.difficulty} difficulty.'
        return player_str
