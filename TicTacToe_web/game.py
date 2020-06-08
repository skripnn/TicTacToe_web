from copy import deepcopy

from TicTacToe_web import players


class TicTacToe:

    def __init__(self, player_x, player_o, size=3, first_step=None):
        self.size = size
        self.field = self.make_field()
        self.wins = players.make_wins(size)

        self.cells = None
        self.winners = []
        self.state = None
        self.count_steps = 0
        self.player = 'X'

        self.player_x = player_x
        self.player_o = player_o

        if first_step is not None:
            if len(first_step) == size ** 2:
                self.first_step(first_step)
            else:
                print("First step can't exist")
                self.algorithm()
        else:
            self.algorithm()

    def make_field(self):
        field = []
        for x in range(self.size):
            field.append([' ' for y in range(self.size)])
        return field

    def first_step(self, steps):
        for x in range(self.size):
            for y in range(self.size):
                step = steps[y + x * self.size]
                if step == 'X' or step == 'O':
                    self.field[x][y] = step
        self.algorithm()

    def algorithm(self):
        self.add_to_cells()
        self.print_cells()
        self.check_state()
        if self.state == 'game not finished':
            self.change_player()
            self.count_steps += 1
            self.step()
        else:
            print(self.state)
            try:
                all_counts = self.player_x.counts + self.player_o.counts
                print(f'all counts = {all_counts}')
            except AttributeError:
                print('Counts available only for HARD/HARD game')
            print('')


    def step(self):
        print(f'player {self.player} step:')
        if self.player == 'X':
            x, y = self.player_x.step(self.field, self.player)
        else:  # if self.player == 'O':
            x, y = self.player_o.step(self.field, self.player)
        self.field[x][y] = self.player
        self.algorithm()

    def change_player(self):
        all_cells = [m for n in self.field for m in n]
        all_x = [x for x in all_cells if x == 'X']
        all_o = [o for o in all_cells if o == 'O']
        if len(all_x) > len(all_o):
            self.player = 'O'
        elif len(all_o) >= len(all_x):
            self.player = 'X'

    def print_cells(self):
        print(self.cells)

    def add_to_cells(self):
        cells = []
        n_top_bottom = '--' + ('--' * self.size) + '-'
        cells.append(n_top_bottom)
        for x in range(self.size):
            n = '| '
            for y in range(self.size):
                n += f'{self.field[x][y]} '
            n += '|'
            cells.append(n)
        cells.append(n_top_bottom)

        self.cells = '\n'.join(cells)

    def check_win_rows(self):
        for win in self.wins:
            win_string = ''
            for xy in win:
                win_string += self.field[xy[0]][xy[1]]
            win_letters = win_string.replace(' ', '')
            win_set = set(win_letters)
            if len(win_letters) == self.size and len(win_set) == 1:
                winner = ''.join(win_set)
                self.winners.append(winner)

    def check_state(self):
        self.check_win_rows()
        all_cells = [m for n in self.field for m in n]
        all_x = [x for x in all_cells if x == 'X']
        all_o = [o for o in all_cells if o == 'O']
        if len(all_x) - len(all_o) > 1:
            self.state = 'Impossible'
        elif len(all_o) - len(all_x) > 1:
            self.state = 'Impossible'
        elif len(self.winners) == 0 and ' ' in all_cells:
            self.state = 'game not finished'
        elif len(self.winners) == 0 and ' ' not in all_cells:
            self.state = 'Draw'
        else:
            if self.winners[0] == 'X':
                self.state = 'X wins'
            elif self.winners[0] == 'O':
                self.state = 'O wins'


class Menu:

    # def __init__(self):
    # while True:
    #     line = input('Input command: ').split()
    #     command = line.pop(0)
    #     self.input(command, line)

    def input(self, command, args, size=3):
        if command == 'start':
            if len(args) != 2:
                return self.bad_parameters()
            players = []
            for arg in args:
                players.append(self.player_choose(arg, size))
                if players[-1] is None:
                    return self.bad_parameters()
            game = TicTacToe(*players, size)
            # new_field = []
            # for n, row in enumerate(game.field):
            #     new_field.append([])
            #     for column in row:
            #         if column == 'X':
            #             column = 'images/x.png'
            #         elif column == 'O':
            #             column = 'images/o.png'
            #         else:
            #             column = 'images/none.png'
            #         new_field[n].append(column)
            # print(new_field)
            return {
                'state': game.state,
                'cells': game.field
            }

        if command == 'exit':
            exit()
        else:
            print('Wrong command!')

    def player_choose(self, player, size):
        if player == 'user':
            return players.Human()
        if player == 'easy':
            return players.Easy(size)
        if player == 'medium':
            return players.Medium(size)
        if player == 'hard':
            return players.Hard(size)
        return None

    def bad_parameters(self):
        print('Bad parameters!')
        return None


# Menu().input('start', ['medium', 'easy'], 3)
