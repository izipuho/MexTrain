#!/usr/bin/env python3
import random
import json

#in_max_tile = int(input('What is the maximum tile: '))
#in_players_count = int(input('How much players are we awaiting: '))
#in_difficulty = input('What is the difficulty: ')
in_max_tile = 12
in_players_count = 4
in_difficulty = 'normal'
# define tile
class tile:
    def __init__(self, numbers):
        self.numbers = numbers
        self.code = f'{numbers[0]}-{numbers[1]}}'
        self.text = f'[{self.numbers[0]:>2}|{self.numbers[1]:>2}]'
        self.text_flipped = f'[{self.numbers[1]:>2}|{self.numbers[0]:>2}]'
        self.score = sum(numbers)
        if self.score == 0:
            self.score = 25

    def is_double(self):
        if self.numbers[0] == self.numbers[1]:
            print(f'{self.numbers} is double.')
            return(True)
        else:
            print(f'{self.numbers} not a double.')
            return(False)

    def flip(self):
        print(f'Tile {self.text} will be fliped to {self.text_flipped}')
        self.numbers.reverse()

    def is_suitable(self, number):
        if number in self.numbers:
            if number == self.numbers[1]:
                self.flip()
            return(True)
        else:
            return(False)

    def __str__(self):
        return(f'[{self.numbers[0]:>2}|{self.numbers[1]:>2}]')

    def __repr__(self):
        return(f'Tile {self.numbers} scores {self.score} points.')

class tile_set:
    def __init__(self):
        self.max_tile = in_max_tile#[in_max_tile, in_max_tile]
        self.set = dict()
        self.set_repr = str()
        self.create()
        print(self)

    def create(self):
        for t in range(in_max_tile, -1, -1):
            for i in range(t, -1, -1):
                tl = tile((t,i))
                #print(tl)
                self.set[(t,i)] = tl
                self.set_repr += str(tl) + ' '
            self.set_repr += '\n'
        #random.shuffle(self.set)

    def __str__(self):
        return(f'Got set of {len(self.set)} tiles with {self.max_tile} highest.')

    def __repr__(self):
        return(self.set_repr)

#TODO messed up with tile set
class table:
    def __init__(self, players):
        self.players = players 
        self.tile_set = tile_set()
        self.max_tile = self.tile_set.max_tile
        #self.table_tile_cnt = len(self.tile_set.set)
        # Set hand tile_count. Not by the rules, but why not to make it?
        self.hand_tile_cnt = self.tile_set.max_tile#in_max_tile#12
        if self.players == 2:
            self.hand_tile_cnt += 3
        # Init scores
        self.scores = dict()
        for p in range(1, self.players+1):
            self.scores[p] = 0
        self.scores['Table'] = 0
        self.table = dict()

    def deal(self, round):
        tile_set = self.tile_set.set.copy()
        # remove start tile
        tile_set.remove(tile([round, round]))
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
                ##n = random.randint(0, len(tile_set)-1)
                #print("deal: {order}'th tile out of {total}".format(order = n, total = len(tile_set)))
                ##hands[p].append(tile_set[n])
                hands[p].append(random.choice(list(tile_set.values())))
                # delete it from set
                ##del tile_set[n]
        hands['Table'] = tile_set
        table_tile_cnt = len(hands['Table'])
        print(f'Dealt {self.hand_tile_cnt} tiles for {self.players} players. Got {table_tile_cnt} tiles left on table and {[round, round]} is strating tile.\n')
        self.table = {'hands': hands, 'trails': trails, 'moves': 0}

    def __str__(self):
        #return(f'Got set of {self.table_tile_cnt} tiles.')
        pass


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
        for rnd in range(self.tbl.max_tile, -1, -1):
            #print(self.tbl)
            r = game_round(self.tbl, rnd)
            for p in range(1, self.players+1):
                r.init_trail(p, in_difficulty)
            r.calc_hands()

    def end_game(self):
        final_scores = dict(sorted(self.tbl.scores.items(), key=lambda item: item[1]))
        i = 1
        for k in final_scores:
            if k != 'Table':
                print(f'{i} place. Player {k} scores {final_scores[k]}.')
            i += 1

a = tile((1,2))
print(a)
a.flip()
