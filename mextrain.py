#!/usr/bin/env python3
import random
import TileSet
from Player import Player

# in_max_tile = int(input('What is the maximum tile: '))
# in_players_count = int(input('How many players are we awaiting: '))
# in_difficulty = input('What is the difficulty: ')
in_max_tile = 4
in_players_count = 3
in_difficulty = 'easy'

class Table:
    def __init__(self, players_count):
        self.players = dict() #players
        for pl in range(1, players_count + 1):
            in_player_name = input(f'№{pl} player name: ')
            print('Choose player difficulty:')
            print('\t[1] for easy')
            print('\t[2] for normal')
            print('\t[3] for hard')
            print('\t[0] for manual')
            in_player_dfctl = input('...')
            self.players[pl] = Player(in_player_name, in_player_dfctl)
        self.tile_set = TileSet.Set(in_max_tile)
        # self.dealing_set = self.tile_set.set.copy()
        self.max_tile = self.tile_set.max_tile
        # self.table_tile_cnt = len(self.tile_set.set)
        # Set hand tile_count. Not by the rules, but why not to make it?
        self.hand_tile_cnt = self.tile_set.max_tile  # in_max_tile#12
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
    # TODO make true flip
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


class GameRound:
    def __init__(self, table, round_num):
        self.table = table
        if round_num > self.table.max_tile:
            print(f'{round_num} is beyond possible.')
            round_num = input('Which round are we playing? ')
        self.num = int(round_num)
        self.table.layout['round'] = [self.num, 'Started']
        print(f'Round {self.num}. Go.')
        self.is_round_finished = False
        self.moves = 0
        print(self.table)
        self.table.deal(self.num)
        print(self.table)

    def play(self):
        for player in range(1, len(self.table.players) + 1):
            self.init_trail(player, in_difficulty)
            if len(self.table.layout['hands'][player]) == 0:
                print(f'Player {player} put all tiles to initial trail. Round {self.num} is over.')
                self.is_round_finished = True
            # input('')
        self.moves += 1
        while not self.is_round_finished:
            self.turn(in_difficulty)
            input('')
        if self.is_round_finished:
            self.aftermath()

    # Let the magic happen
    def init_trail(self, player_num):
        # get one hand
        hand = self.table.layout['hands'][player_num]
        player = self.table.players[player_num]
        trail = dict()
        init_number = self.num
        # print(f'\tPlayer {player.name} had hand: {hand.values()}')
        if player.difficulty == 'easy':
            # order based
            while len(hand) != 0 and init_number != -1:
                # print(f'Looking for {init_number}')
                # print(f'Hand tile count: {len(hand)}')
                i = 0
                for k, t in hand.items():
                    # print(f'--Key is {k} and value {repr(t)}')
                    i += 1
                    if t.is_suitable(init_number):
                        # print(f'{t} is ok')
                        # self.table.move_tile(t, ['hand', player_num], ['home'])
                        # TODO. I want to use move method
                        hand.pop(k)
                        trail.update({k: t})
                        init_number = t.numbers[1]
                        break
                    if i == len(hand):
                        # print('None found')
                        init_number = -1
                        break
        elif player.difficulty == 'normal':
            # TODO
            # max based without doubles
            i = 0
            while len(hand) != 0 and init_number != -1 and i < 100:
                print(f'Hand tile count: {len(hand)}')
                print(f'Looking for {init_number}')
                second_number = -1
                for t in hand:
                    print(f'{hand.index(t) + 1}. Current tile: {t}. Current max number: {second_number}. Looking for init {init_number}.')
                    if t.is_suitable(init_number):
                        print(f'{t} is ok')
                        # TODO something bad with this breaking loop
                        if t.is_double:
                            print('Double is always good. Take it.')
                            good_tile = t
                            break
                        elif second_number < t.numbers[1]:
                            print('More is better. Changed tile')
                            good_tile = t
                            second_number = t.numbers[1]
                        else:
                            print('Old one is good')
                            pass
                init_number = second_number
                # TODO I don't like the good_tile
                if second_number != -1:
                    hand.remove(good_tile)
                    trail.append(good_tile)
                    print(f'We take {repr(good_tile)} to trail.\n')
                else:
                    break
                i += 1
        self.table.layout['trails'][player_num][1] = trail
        if len(trail) == 0:
            print(f'\tPlayer {player.name} has no trail')
            self.table.layout['trails'][player_num][0] = 'Empty'
        elif len(trail) == self.table.hand_tile_cnt:
            print(f'\tPlayer {player.name} set all tiles to init trail: {list(trail.values())}')
            self.is_round_finished = True
        else:
            self.table.layout['trails'][player_num][0] = 'Closed'
            print(f'\tPlayer {player.name} has init trail {len(trail)} tiles long: {list(trail.values())}')
        if self.is_round_finished:
            self.table.layout['round'][1] = 'End'
        else:
            self.table.layout['round'][1] = 'Init trails'
        print('\n')

    def turn(self):
        # TODO ugly
        player_num = (self.moves - 1) % len(self.table.players) + 1
        player = self.table.players[player_num]
        print(f"Turn {self.moves}. Player {player.name}.")
        hand = self.table.layout['hands'][player_num]
        print(f'Current hand: {hand}')
        possible_moves = {'tiles': dict(), 'nums': dict(), 'possible_tiles': [], 'possible_cnt': 0}
        if self.moves != 0 and self.table.layout['trails'][player_num][0] != 'Empty':
            # TODO init move
            # technically open self trail for this turn if it is not initial turn
            self.table.layout['trails'][player_num][0] = 'Opened'

        # Look for opened trails
        for p, trail in self.table.layout['trails'].items():
            if trail[0] == 'Opened':
                possible_moves['tiles'][p] = list(trail[1].values())[-1]
                possible_moves['nums'][p] = possible_moves['tiles'][p].numbers[1]  # trail[1][-1][1]
            elif trail[0] in ('Empty', 'Closed'):
                pass
        # Look for possible tiles
        for p, n in possible_moves['nums'].items():
            # print(f'Add {n} to possible tiles set')
            for t in hand.values():
                # print(f'--Checkin out if tile {t} suits for {n}')
                if t.is_suitable(n):
                    # print(f'Found possible tile: {t}')
                    possible_moves['possible_tiles'].append(t)
                    possible_moves['possible_cnt'] += 1
        # print(f'Possible moves are {possible_moves}')
        # Draw if no possible tiles and check it
        if possible_moves['possible_cnt'] == 0 and len(self.table.layout['hands']['Table']) != 0:
            self.table.draw(player_num)
            new_tile = list(self.table.layout['hands'][player_num].values())[-1]
            print(f'\tPlayer {player.name} drew a tile from table.')
            # print(f"--Drew {repr(new_tile)}")
            is_new_tile_suitable = False
            for p, n in possible_moves['nums'].items():
                # print(f'--Checkin out if tile {repr(new_tile)} suits for {n}')
                if new_tile.is_suitable(n):
                    print(f'Put new tile to {p}')
                    self.table.move_tile(new_tile, ['hand', player_num], ['trail', p])
                    if p != 'Table':
                        print(f'\tClose trail {p}.')
                        if self.table.layout['trails'][p][0] != 'Empty':
                            self.table.layout['trails'][p][0] = 'Closed'
                    is_new_tile_suitable = True
                    break
            if not is_new_tile_suitable:
                print(f"\t\tNew tile is no good. Open {player.name}'s trail.")
                if self.table.layout['trails'][player_num][0] != 'Empty':
                    self.table.layout['trails'][player_num][0] = 'Opened'
        # Just open trail if no tiles left on table
        elif possible_moves['possible_cnt'] == 0 and len(self.table.layout['hands']['Table']) == 0:
            print(f"\tNo tiles left on self.table to draw. Open {player.name}'s trail.")
            if self.table.layout['trails'][player_num][0] != 'Empty':
                self.table.layout['trails'][player_num][0] = 'Opened'
        else:
            for t in possible_moves['possible_tiles']:
                if player.difficulty == 'easy':
                    # by order
                    end_turn = False
                    for p, n in possible_moves['nums'].items():
                        if t.is_suitable(n):
                            print(f'Put {repr(t)} in trail {p}')
                            self.table.move_tile(t, ['hand', player_num], ['trail', p])
                            if p != 'Table':
                                print(f'\tClose trail {p}.')
                                if self.table.layout['trails'][p][0] != 'Empty':
                                    self.table.layout['trails'][p][0] = 'Closed'
                            end_turn = True
                            break
                elif player.difficulty == 'normal':
                    # by weight
                    # TODO
                    pass
                if end_turn:
                    self.table.layout['trails'][player_num][0] = 'Closed'
                    break
        if len(self.table.layout['hands'][player_num]) == 0:
            print(f'{player.name} has no tile left in hand. Round {self.num} is over.')
            self.is_round_finished = True
        self.moves += 1
        print('\n')
        return self.is_round_finished

    def aftermath(self):
        hands = self.table.layout['hands']
        for p in hands:
            # print(f'--{p}: {self.hands[p]}')
            final_score = 0
            for t in hands[p].values():
                # print(f'--{t.numbers}')
                # print(f'--{t} {t.score} points gonna be added.')
                final_score += t.score
            self.table.scores[p] += final_score
            if p == 'Table':
                print(f'{len(hands[p])} tiles undealt for {final_score} points.\n')
            else:
                if final_score == 0:
                    print(f'Player {p} has no tiles left in hand and scores {final_score}.\n')
                else:
                    print(f'Player {p} has {len(hands[p])} tiles left in hand and scores {final_score}.')
                    print(f'\tHis tiles: {hands[p].values()}\n')


class Game:
    def __init__(self, players, rounds=None):
        self.players = players
        self.table = Table(len(self.players))
        self.first_player = random.randint(1, 4)
        if rounds:
            print(f'Game will last for {rounds} rounds. Final round is {self.table.max_tile - rounds}.\n')
        # print(f'--Max tile: {self.table.max_tile}')
        # print(f'--Final round: {self.table.max_tile - (rounds or 0) + 1}')
        for rnd in range(self.table.max_tile, self.table.max_tile - (rounds or 0), -1):
            gr = GameRound(self.table, rnd)
            for p in range(1, len(self.players) + 1):
                gr.init_trail(p, in_difficulty)
            gr.moves += 1

    def end(self):
        final_scores = dict(sorted(self.table.scores.items(), key=lambda item: item[1]))
        i = 1
        for k in final_scores:
            if k != 'Table':
                print(f'{i} place. Player {k} scores {final_scores[k]}.')
            i += 1
