#!/usr/bin/env python3
import random
import json

#max_tile = int(input('What is the maximum tile: '))
#pl = int(input('How much players are we awaiting: '))
#dfct = input('What is the difficulty: ')
max_tile = 12
pl = 4
dfct = 'normal'
# define tile
class tile:
    #TODO set dynamic tiles
    def __init__(self, max_count):
        self.max_count = max_count
        return

class tile_set:
    tl = tile(max_tile)
    def __init__(self):
        self.max_tile = [self.tl.max_count, self.tl.max_count]
        #self.tile_set = self.create()
        self.ts = self.create()

    def create(self):
        tile_set = []
        for t in range(self.tl.max_count, -1, -1):
            for i in range(t, -1, -1):
               tile = [t, i]
               tile_set.append(tile)
        random.shuffle(tile_set)
        return(tile_set)

    def __str__(self):
        return(f'Got {len(self.ts)} tiles in set with {self.max_tile} highest.')

class table:
    def __init__(self, players):
        self.players = players 
        self.ts = tile_set()
        self.table_tile_cnt = len(self.ts.ts)
        # set hand tile_count
        self.hand_tile_cnt = max_tile#12
        if self.players == 2:
            self.hand_tile_cnt += 3
        print(self.ts)
        # init scores
        self.scores = dict()
        for p in range(1, self.players+1):
            self.scores[p] = 0
        self.scores['Table'] = 0
        self.table = dict()

    def deal(self, round):
        ts = self.ts.ts.copy()
        # remove start tile
        #print(ts)
        ts.remove([round, round])
        # init hands
        hands = dict()
        trails = dict() 
        for p in range(1, self.players+1):
            hands[p] = []
            trails[p] = ['Closed', dict()]
        trails['Table'] = ['Opened', [[round, round]]]
        # deal
        for t in range(0, self.hand_tile_cnt):
            for p in range(1, self.players+1):
                # get random tile
                n = random.randint(0, len(ts)-1)
                #print("deal: {order}'th tile out of {total}".format(order = n, total = len(tile_set)))
                hands[p].append(ts[n])
                # delete it from set
                del ts[n]
        hands['Table'] = ts
        table_tile_cnt = len(hands['Table'])
        print(f'Dealt {self.hand_tile_cnt} tiles for {self.players} players. Got {table_tile_cnt} tiles left on table and {[round, round]} is strating tile.\n')
        self.table = {'hands': hands, 'trails': trails, 'moves': 0}

    def __str__(self):
        return(f'Got set of {self.table_tile_cnt} tiles.')


class game_round:
    def __init__(self, table, round_num):
        self.num = round_num
        self.table = table
        self.table.deal(self.num)
        #print(self.table)
        print(f'Round {self.num}:')
        self.hands = self.table.table['hands']

    # Let the magic happen
    def init_trail(self, player, difficulty):
        # get one hand
        hand = self.hands[player]
        trail = []
        init_number = self.num
        print(f'\tPlayer {player} had hand: {hand}')
        if difficulty == 'easy':
            # order based
            while len(hand) != 0 and init_number != -1:
                #print(f'Looking for {init_number}')
                #print(f'Hand tile count: {len(hand)}')
                for t in hand:
                    #print(f'{hand.index(t) + 1}. Current tile: {t}')
                    if hand.index(t)+1 == len(hand):
                        #print('None found')
                        init_number = -1
                        break
                    if init_number in t:
                        #print(f'{t} is ok')
                        t_aligned = t
                        hand.remove(t)
                        if init_number == t[0]:
                            init_number = t[1]
                        else:
                            init_number = t[0]
                            t_aligned = [t[1], t[0]]
                        trail.append(t_aligned)
                        break
        elif difficulty == 'normal':
            # max based without doubles
            i = 0
            while len(hand) != 0 and init_number != -1 and i < 100:
                #print(f'Hand tile count: {len(hand)}')
                #print(f'Looking for {init_number}')
                second_number = -1
                for t in hand:
                    #print(f'{hand.index(t) + 1}. Current tile: {t}. Current max number: {second_number}. Looking for init {init_number}.')
                    if init_number in t:
                    #if init_number == t[0] or init_number == t[1]:
                        #print(f'{t} is ok')
                        t_aligned = t
                        if init_number != t[0]:
                            #print('Tile reversed')
                            t_aligned = [t[1], t[0]]
                        if second_number < t_aligned[1]:
                            #print('Changed tile')
                            second_number = t_aligned[1]
                        elif second_number == t_aligned[1]:
                            print('Double is always good. Take it.')
                            second_number = t_aligned[1]
                            break
                        else:
                            #print('Old one is good')
                            pass
                        t_aligned = [init_number, second_number]
                init_number = second_number
                if second_number != -1:
                    if t_aligned not in hand:
                        hand.remove([t_aligned[1], t_aligned[0]])
                    else:
                        hand.remove(t_aligned)
                    trail.append(t_aligned)
                    #print(f'We take {t_aligned} to trail.\n')
                else:
                    break
                i += 1
        self.table.table['trails'][player][1] = trail
        if len(trail) == 0:
            self.table.table['trails'][player][0] = 'Empty'
            print(f'\t\tPlayer {player} has no trail')
        else:
            print(f'\t\tPlayer {player} has init trail {len(trail)} tiles long: {trail}')
        print('\n')

    def draw(self, player):
        # get random tile
        n = random.randint(0, len(self.table.table['hands']['Table'])-1)
        #print("deal: {order}'th tile out of {total}".format(order = n, total = len(tile_set)))
        self.table.table['hands'][player].append(self.table.table['hands']['Table'][n])
        print(f"Draw a tile from table: {self.table.table['hands']['Table'][n]}")
        return(self.table.table['hands']['Table'][n])
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
            #TODO
        if self.table.table['trails'][player][0] != 'Empty':
            self.table.table['trails'][player][0] = 'Closed'
        self.table.table['moves'] += 1
        print('\n')

    def calc_hands(self):
        for k in self.hands:
            score = 0
            for t in self.hands[k]:
                #print([t][0])
                score += [t][0][0] + [t][0][1]
                if t == [0, 0]:
                    score += 25
            self.table.scores[k] += score
            if k == 'Table':
                print(f'\t{len(self.hands[k])} tiles undealed for {score} points.')
            else:
                if score == 0:
                    print(f'\tPlayer {k} has no tiles left in hand and scores {score}.')
                else:
                    print(f'\tPlayer {k} has {len(self.hands[k])} tiles left in hand and scores {score}.')
                    print(f'\tHis tiles: {self.hands[k]}')

class game:
    def __init__(self, players):
        self.players = players
        self.tbl = table(self.players)
        self.first_player = randint(1, 4)
        for rnd in range(max_tile, -1, -1):
            #print(self.tbl)
            r = game_round(self.tbl, rnd)
            for p in range(1, self.players+1):
                r.init_trail(p, dfct)
            r.calc_hands()

    def end_game(self):
        final_scores = dict(sorted(self.tbl.scores.items(), key=lambda item: item[1]))
        i = 1
        for k in final_scores:
            if k != 'Table':
                print(f'{i} place. Player {k} scores {final_scores[k]}.')
            i += 1


#gm = game(pl)
#gm.end_game()

tbl = table(pl)
#tbl.deal(12)
r = game_round(tbl, max_tile)
for p in range(1, pl+1):
    trl = r.init_trail(p, dfct)
r.move(1)
r.move(2)
r.move(3)
r.move(4)
print(tbl.table)
#r.calc_hands()

