#!/usr/bin/env python3
import random
import os


# Clear screen
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


class Round:
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

    # TODO
    def play(self):
        pass

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
            # max based without doubles
            i = 0
            while len(hand) != 0 and init_number != -1 and i < 100:
                # print(f'Hand tile count: {len(hand)}')
                # print(f'Looking for {init_number}')
                second_number = -1
                for t in hand.values():
                    # print(f'Current tile: {t}. Current max number: {second_number}. Looking for init {init_number}.')
                    if t.is_suitable(init_number):
                        # print(f'{repr(t)} is ok')
                        if t.is_double():
                            # print('Double is always good. Take it.')
                            good_tile = t
                            second_number = t.numbers[1]
                        elif second_number < t.numbers[1]:
                            # print('More is better. Changed tile')
                            good_tile = t
                            second_number = t.numbers[1]
                        else:
                            # print('Old one is good')
                            pass
                init_number = second_number
                # TODO I don't like the good_tile
                if second_number != -1:
                    hand.pop(good_tile.code)
                    trail[good_tile.code] = good_tile
                    # print(f'We take {repr(good_tile)} to trail.\n')
                else:
                    break
                i += 1
        self.table.layout['trails'][player_num][1] = trail
        if len(trail) == 0:
            print(f'\t{player.name} has no trail')
            self.table.layout['trails'][player_num][0] = 'Empty'
        elif len(trail) == self.table.hand_tile_cnt:
            print(f'\t{player.name} set all tiles to init trail: {list(trail.values())}')
            self.is_round_finished = True
        else:
            self.table.layout['trails'][player_num][0] = 'Closed'
            print(f'\t{player.name} has init trail {len(trail)} tiles long: {list(trail.values())}')
        if self.is_round_finished and len(self.table.layout['hands'][player_num]) == 0:
            self.table.layout['round'][1] = 'End'
            print(f'{player.name} has no tiles left. Do aftermath.')
        else:
            self.table.layout['round'][1] = 'Init trails'
        print('\n')

    def turn(self, player_num):
        # cls()
        # TODO ugly
        # player_num = (self.moves - 1) % len(self.table.players) + 1
        player = self.table.players[player_num]
        print(f"Turn {self.moves}. Player {player.name}.")
        hand = self.table.layout['hands'][player_num]
        print(f'Current hand: {list(hand.values())}')
        possible_moves = {'trails': dict(), 'nums': dict(), 'possible_tiles': dict(), 'possible_cnt': 0}
        if len(self.table.layout['trails']['Table'][1]) > 1 and self.table.layout['trails'][player_num][0] != 'Empty':
            # technically open self trail for this turn if it is not initial turn
            self.table.layout['trails'][player_num][0] = 'Opened'
        elif len(self.table.layout['trails']['Table'][1]) == 0:
            pass
        # Look for opened trails
        for p, trail in self.table.layout['trails'].items():
            if trail[0] == 'Opened':
                possible_moves['trails'][p] = list(trail[1].values())[-1]
                possible_moves['nums'][p] = possible_moves['trails'][p].numbers[1]  # trail[1][-1][1]
                possible_moves['possible_tiles'][p] = []
            elif trail[0] in ('Empty', 'Closed'):
                pass
        # Look for possible tiles
        for p, n in possible_moves['nums'].items():
            # print(f'Add {n} to possible tiles set')
            for t in hand.values():
                # print(f'--Checkin out if tile {t} suits for {n}')
                if t.is_suitable(n):
                    # print(f'Found possible tile: {t}')
                    possible_moves['possible_tiles'][p].append(t)
                    possible_moves['possible_cnt'] += 1
        # print(f'--Possible moves are {possible_moves}')
        # Draw if no possible tiles and check it
        if possible_moves['possible_cnt'] == 0 and len(self.table.layout['hands']['Table']) != 0:
            self.table.draw(player_num)
            new_tile = list(self.table.layout['hands'][player_num].values())[-1]
            print(f'\t{player.name} drew a tile from table.')
            # print(f"--Drew {repr(new_tile)}")
            is_new_tile_suitable = False
            for p, n in possible_moves['nums'].items():
                # print(f'--Checkin out if tile {repr(new_tile)} suits for {n}')
                if new_tile.is_suitable(n):
                    print(f'\t\tPut new tile ({repr(new_tile)}) to trail {p}.')
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
        # Put tile from hand to some trail
        else:
            end_turn = False
            if player.difficulty == 'easy':
                for p, tiles in possible_moves['possible_tiles'].items():
                    # by order
                    if len(tiles) != 0:
                        print(f'\tPut {repr(tiles[0])} to trail {p}')
                        self.table.move_tile(tiles[0], ['hand', player_num], ['trail', p])
                        if p != 'Table':
                            print(f'\tClose trail {p}.')
                            if self.table.layout['trails'][p][0] != 'Empty':
                                self.table.layout['trails'][p][0] = 'Closed'
                        end_turn = True
                        break

                    if end_turn:
                        self.table.layout['trails'][player][0] = 'Closed'
                        break
            elif player.difficulty == 'normal':
                # by weight
                second_number = -1
                for p, tiles in possible_moves['possible_tiles'].items():
                    for tile in tiles:
                        # print(f'Checking out {repr(tile)}.')
                        if tile.is_double():
                            # print('Double is always good. Take it.')
                            good_tile = [tile, p]
                            break
                        elif tile.numbers[1] > second_number:
                            # print('More is better.')
                            second_number = tile.numbers[1]
                            good_tile = [tile, p]
                        else:
                            pass
                print(f'Put {repr(good_tile[0])} in trail {good_tile[1]}')
                self.table.move_tile(good_tile[0], ['hand', player_num], ['trail', good_tile[1]])

        if len(self.table.layout['hands'][player_num]) == 0:
            print(f'Player {player.name} has no tile left in hand. Round {self.num} is over.')
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
                    print(f'{self.table.players[p].name} has no tiles left in hand and scores {final_score}.\n')
                else:
                    print(f'{self.table.players[p].name} has {len(hands[p])} tiles left in hand and scores {final_score}.')
                    print(f'\tHis tiles: {list(hands[p].values())}\n')


class Game:
    def __init__(self, table, first_round=None, rounds=None):
        self.table = table
        first_player = random.choice(list(self.table.players.keys()))
        if rounds:
            print(f'Game will last for {rounds} rounds. Final round is {self.table.max_tile - rounds}.\n')
        # print(f'--Max tile: {self.table.max_tile}')
        # print(f'--Final round: {self.table.max_tile - (rounds or 0) + 1}')
        for rnd in range(first_round, -1, -1):
            input(f'Press Enter to deal round {rnd}.')
            gr = Round(self.table, rnd)
            for player_num, player in self.table.players.items():
                input(f'Press Enter to set init trail for {player.name}.')
                gr.init_trail(player_num)
            gr.moves += 1
            while not gr.is_round_finished:
                input(f'Press Enter for next turn...')
                current_player = ((first_player - 1 + (self.table.max_tile - rnd) + gr.moves - 1) % len(self.table.players)) + 1
                gr.turn(current_player)
            input(f'\nPress Enter for aftermath.')
            gr.aftermath()

    def end(self):
        final_scores = dict(sorted(self.table.scores.items(), key=lambda item: item[1]))
        i = 1
        final_scores.pop('Table')
        for k in final_scores:
            if k != 'Table':
                print(f'{i} place. Player {k} scores {final_scores[k]}.')
            i += 1
