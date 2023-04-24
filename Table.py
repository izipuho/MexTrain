#!/usr/bin/env python3
import TileSet
import random


class Player:
    def __init__(self, name, difficulty=-1):
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


class Table:
    def __init__(self, max_tile, players_count):
        self.players = dict()
        for pl in range(1, players_count + 1):
            in_player_name = input(f'№{pl} player name: ')
            print('Choose player difficulty:')
            print('\t[1] for easy')
            print('\t[2] for normal')
            print('\t[3] for hard')
            print('\t[0] for manual')
            in_player_difficulty = input('...')
            if in_player_difficulty in ('3', '0'):
                print(f'Difficulty {in_player_difficulty} under construction. Will be 2 (normal).')
                in_player_difficulty = 2
            elif in_player_difficulty not in ('1', '2'):
                in_player_difficulty = input('Choose difficulty from listed above...')
            self.players[pl] = Player(in_player_name, in_player_difficulty)
        self.tile_set = TileSet.Set(max_tile)
        # self.dealing_set = self.tile_set.set.copy()
        self.max_tile = self.tile_set.max_tile
        # self.table_tile_cnt = len(self.tile_set.set)
        # Set hand tile_count. Not by the rules, but why not to make it?
        self.hand_tile_cnt = self.tile_set.max_tile
        if len(self.players) == 2:
            self.hand_tile_cnt += 3

        print(self.tile_set)
        # init scores
        self.scores = dict()
        for p in range(1, len(self.players) + 1):
            self.scores[p] = 0
        self.scores['Table'] = 0
        self.layout = {
            'hands': dict(),
            'trails': dict(),
            'round': [-1, 'Init']
        }

    def move_tile(self, tile, src=[], dst=[]):
        # TODO make some restrictions
        # inputs must be:
        # src: ['hand'/'Table', player or None]
        # dst: ['hand'/'trail'/'Table', player]
        if src[0] == 'Table':
            if dst[0] == 'trail':
                raise Exception("You can't move tile from table straight to trail.")
            elif dst[0] == 'hand':
                self.layout['hands']['Table'].pop(tile.code)
                if dst[1]:
                    self.layout['hands'][dst[1]].update({tile.code: tile})
                else:
                    raise Exception('Determine player')
        elif src[0] == 'hand':
            if src[1]:
                self.layout['hands'][src[1]].pop(tile.code)
            else:
                raise Exception('Determine source player')
            if dst[0] == 'trail':
                if tile.is_suitable(list(self.layout['trails'][dst[1]][1].values())[-1].numbers[1]):
                    self.layout['trails'][dst[1]][1].update({tile.code: tile})
            elif dst[0] == 'Table':
                if tile.is_suitable(list(self.layout['trails']['Table'][1].values())[-1].numbers[1]):
                    self.layout['trails']['Table'][1].update({tile.code: tile})
            elif dst[0] == 'home':
                if tile.is_suitable(list(self.layout['trails'][src[1]][1].values())[-1].numbers[1]):
                    self.layout['trails'][src[1]][1].update({tile.code: tile})

    def draw(self, player):
        k, tl = random.choice(list(self.layout['hands']['Table'].items()))
        # print(f'--Player {p} draws tile with key {k} and value {repr(tl)}')
        self.move_tile(tl, ['Table'], ['hand', player])

    def deal(self, round_num):
        self.layout['hands']['Table'] = self.tile_set.set.copy()
        print('Dealing...')
        hands = self.layout['hands']
        trails = self.layout['trails']
        init_tile = hands['Table'][f'{round_num}-{round_num}']
        del hands['Table'][init_tile.code]
        for p in range(1, len(self.players) + 1):
            hands[p] = dict()
            trails[p] = ['Empty', dict()]
        trails['Table'] = ['Opened', {init_tile.code: init_tile}]
        # deal
        for t in range(0, self.hand_tile_cnt):
            for p in range(1, len(self.players) + 1):
                self.draw(p)
        # table_tile_cnt = len(hands['Table'])
        # print(f'Dealt {self.hand_tile_cnt} tiles for {len(self.players)} players.')
        # print(f'Got {table_tile_cnt} tiles left on table and {[round, round]} is starting tile.\n')
        # self.layout = {'hands': hands, 'trails': trails, 'moves': 0, 'round': [round_num, 'Dealt']}
        self.layout['round'] = [round_num, 'Dealt']

    def __str__(self):
        table_str = f'We have {len(self.players)} players at the table'
        if self.layout['round'][1] == 'Started':
            pass  # table_str += '. No tiles are dealt.'
        else:
            table_str = f"All tiles are dealt. {len(self.layout['hands']['Table'])} tiles left."
        return table_str

    def __repr__(self):
        # print(f"What do we have on table?\n{self.layout['round']}")
        layout_repr = str()
        if self.layout['round'][1] != 'Dealt':
            # print('Table is set. We have trails.')
            layout_repr = 'Trails are:\n'
            for p in range(1, len(self.players) + 1):
                layout_repr += f"\tPlayer {p} has trail:\n"
                layout_repr += f"\t\t{self.layout['trails'][p][1]} and it is {self.layout['trails'][p][0].lower()}.\n"
        else:
            pass
        return layout_repr
