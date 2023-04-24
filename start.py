#!/usr/bin/env python3
from Table import Table
from Game import Game

in_max_tile = int(input('Choose game type: 4, 6, 12, 15: '))
in_players_count = int(input('How many players are we awaiting: '))
tbl = Table(in_max_tile, in_players_count)

try:
    in_start_round = int(input(f'Which round we start with (not greater then {in_max_tile}) or press Enter for full game: '))
except ValueError:
    in_start_round = in_max_tile

gm = Game(tbl, in_start_round)

gm.end()
