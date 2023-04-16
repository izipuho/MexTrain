#!/usr/bin/env python3.9
import random
import pprint

# in_max_tile = int(input('What is the maximum tile: '))
# in_players_count = int(input('How much players are we awaiting: '))
# in_difficulty = input('What is the difficulty: ')
in_max_tile = 12
in_players_count = 4
in_difficulty = 'easy'


# define tile
class tile:
    def __init__(self, numbers):
        self.numbers = numbers
        self.code = f'{numbers[0]}-{numbers[1]}'
        self.text = f'[{self.numbers[0]:>2}|{self.numbers[1]:>2}]'
        self.text_flipped = f'[{self.numbers[1]:>2}|{self.numbers[0]:>2}]'
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
        # print(f'Tile {self.text} will be fliped to {self.text_flipped}')
        self.numbers.reverse()

    def is_suitable(self, number):
        if number in self.numbers:
            # print(f'{self.numbers} vs {number}: ok!')
            if number == self.numbers[1]:
                self.flip()
            return True
        else:
            # print(f'{self.numbers} vs {number}: No!')
            return False

    def __repr__(self):
        return f'[{self.numbers[0]:>2}|{self.numbers[1]:>2}]'

    def __str__(self):
        return f'Tile {self.numbers} scores {self.score} points.'


class tile_set:
    #tl = tile(in_max_tile)
    def __init__(self):
        self.max_tile = in_max_tile  # [in_max_tile, in_max_tile]
        self.set = dict()
        self.set_repr = str()
        self.create()
        print(self)

    def create(self):
        tile_set = []
        for t in range(self.tl.max_tile, -1, -1):
            for i in range(t, -1, -1):
                tl = tile([t, i])
                # print(tl)
                self.set[tl.code] = tl
                self.set_repr += str(tl) + ' '
            self.set_repr += '\n'

    def __str__(self):
        return f'Got set of {len(self.set)} tiles with {self.max_tile} highest.'

    def __repr__(self):
        return self.set_repr


class table:
    def __init__(self, players):
        self.players = players
        self.tile_set = tile_set()
        self.max_tile = self.tile_set.max_tile
        # self.table_tile_cnt = len(self.tile_set.set)
        # Set hand tile_count. Not by the rules, but why not to make it?
        self.hand_tile_cnt = self.tile_set.max_tile  # in_max_tile#12

        if self.players == 2:
            self.hand_tile_cnt += 3
        print(self.ts)
        # init scores
        self.scores = dict()
        for p in range(1, self.players + 1):
            self.scores[p] = 0
        self.scores['Table'] = 0
        self.layout = dict()

    def deal(self, round):
        print('Dealing...')
        tile_set = self.tile_set.set.copy()
        # Remove start tile. Ugly: not by tile class. MayBe TODO
        #TODO fix to normal tile-class
        del tile_set[f'{round}-{round}']
        # Init hands
        hands = dict()
        trails = dict()
        for p in range(1, self.players + 1):
            hands[p] = dict()
            trails[p] = ['Closed', dict()]
        trails['Table'] = ['Opened', [[round, round]]]
        # deal
        for t in range(0, self.hand_tile_cnt):
            for p in range(1, self.players + 1):
                # get random tile
                ##n = random.randint(0, len(tile_set)-1)
                # print("deal: {order}'th tile out of {total}".format(order = n, total = len(tile_set)))
                ##hands[p].append(tile_set[n])
                k, tl = random.choice(list(tile_set.items()))
                #print(f'--Player {p} draws tile with key {k} and value {repr(tl)}')
                hands[p][k] = tl
                # delete it from set
                del tile_set[tl.code]
        hands['Table'] = tile_set
        table_tile_cnt = len(hands['Table'])
        #print(f'Dealt {self.hand_tile_cnt} tiles for {self.players} players. Got {table_tile_cnt} tiles left on table and {[round, round]} is strating tile.\n')
        self.layout = {'hands': hands, 'trails': trails, 'moves': 0, 'round': [round, 'Dealt']}

    def __str__(self):
        table_str = f'We have {self.players} players at the table'
        if len(self.layout) == 0:
            table_str += '. No tiles are dealt. Game not started.'
        else:
            table_str += f"... still. All tiles are dealt. {len(self.layout['hands']['Table'])} tiles left. Current round is {self.layout['round'][0]}."
        return table_str

    def __repr__(self):
        #print(f"What do we have on table?\n{self.layout['round']}")
        layout_repr = str()
        if self.layout['round'][1] != 'Dealt':
            #print('Table is set. We have trails.')
            layout_repr = 'Trails are:\n'
            for p in range(1, self.players + 1):
                layout_repr += f"\tPlayer {p} has trail:\n"
                layout_repr += f"\t\t{self.layout['trails'][p][1]} and it is {self.layout['trails'][p][0].lower()}.\n"
        else:
            pass
        return layout_repr

class game_round:
    def __init__(self, table, round_num):
        self.num = round_num
        self.table = table
        self.table.deal(self.num)
        self.hands = self.table.layout['hands']

    # Let the magic happen
    def init_trail(self, player, difficulty):
        # get one hand
        hand = self.hands[player]
        trail = dict()
        init_number = self.num
        print(f'\tPlayer {player} had hand: {hand}')
        if difficulty in ('easy', 'e', '0'):
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
                        del hand[k]
                        trail[k] = t
                        init_number = t.numbers[1]
                        break
                    if i + 1 == len(hand):
                        # print('None found')
                        init_number = -1
                        break
        # TODO messed up with tile_set and tile classes
        elif difficulty in ('normal', 'n', '1'):
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
                        #TODO something bad with this breaking loop
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
                #TODO I don't like the good_tile
                if second_number != -1:
                    hand.remove(good_tile)
                    trail.append(good_tile)
                    print(f'We take {repr(good_tile)} to trail.\n')
                else:
                    break
                i += 1
        self.table.layout['trails'][player][1] = trail
        if len(trail) == 0:
            self.table.layout['trails'][player][0] = 'Empty'
            print(f'\t\tPlayer {player} has no trail')
        else:
            print(f'\t\tPlayer {player} has init trail {len(trail)} tiles long: {trail}')
        self.table.layout['round'][1] = 'Init trails'
        print('\n')

    def draw(self, player):
        # get random tile
        n = random.randint(0, len(self.table.table['hands']['Table']) - 1)
        # print("deal: {order}'th tile out of {total}".format(order = n, total = len(tile_set)))
        self.table.table['hands'][player].append(self.table.table['hands']['Table'][n])
        print(f"Draw a tile from table: {self.table.table['hands']['Table'][n]}")
        return self.table.table['hands']['Table'][n]
        # delete it from set
        del self.table.table['hands']['Table'][n]

    def move(self, player):
        print(f"Move {self.table.table['moves']}. Player {player}.")
        hand = self.table.table['hands'][player]
        print(f'Current hand: {hand}')
        possible_moves = {'tiles': dict(), 'nums': dict(), 'arr': [], 'possible_tiles': dict(), 'possible_cnt': 0}
        if self.table.table['moves'] != 0 and self.table.table['trails'][player][0] != 'Empty':
            self.table.table['trails'][player][0] = 'Opened'
        for p, t in self.table.table['trails'].items():
            print(p, t)
            if t[0] == 'Opened':
                possible_moves['tiles'][p] = t[1][-1]
                possible_moves['nums'][p] = t[1][-1][1]
                possible_moves['arr'].append(t[1][-1][1])
            elif t[0] == 'Empty':
                pass
            elif t[0] == 'Closed':
                pass
        print(f'Possible moves: {possible_moves}')
        for a in possible_moves['arr']:
            print(f'Add {a} to possible tiles set')
            possible_moves['possible_tiles'][a] = []
            for t in hand:
                if a in t:
                    possible_moves['possible_tiles'][a].append(t)
                    possible_moves['possible_cnt'] += 1
        print(f'Possible moves: {possible_moves}')
        if possible_moves['possible_cnt'] == 0:
            new_tile = self.draw(player)
            # TODO
        if self.table.table['trails'][player][0] != 'Empty':
            self.table.table['trails'][player][0] = 'Closed'
        self.table.table['moves'] += 1
        print('\n')

    def calc_hands(self):
        for p in self.hands:
            # print(f'--{p}: {self.hands[p]}')
            final_score = 0
            #TODO some t is not tile class but str. Fix
            for t in self.hands[p].values():
                # print(f'--{t.numbers}')
                # print(f'--{t} {t.score} points gonna be added.')
                final_score += t.score
            self.table.scores[p] += final_score
            if p == 'Table':
                print(f'\t{len(self.hands[p])} tiles undealed for {final_score} points.\n')
            else:
                if final_score == 0:
                    print(f'\tPlayer {p} has no tiles left in hand and scores {final_score}.')
                else:
                    print(f'\tPlayer {p} has {len(self.hands[p])} tiles left in hand and scores {final_score}.')
                    #TODO ugly printing with dict_values
                    print(f'\tHis tiles: {self.hands[p].values()}\n')


class game:
    def __init__(self, players):
        self.players = players
        self.tbl = table(self.players)
        self.first_player = random.randint(1, 4)
        for rnd in range(self.tbl.max_tile, -1, -1):
            # print(self.tbl)
            r = game_round(self.tbl, rnd)
            for p in range(1, self.players + 1):
                r.init_trail(p, in_difficulty)
            r.calc_hands()

    def end_game(self):
        final_scores = dict(sorted(self.tbl.scores.items(), key=lambda item: item[1]))
        i = 1
        for k in final_scores:
            if k != 'Table':
                print(f'{i} place. Player {k} scores {final_scores[k]}.')
            i += 1


gm = game(4)
gm.end_game()