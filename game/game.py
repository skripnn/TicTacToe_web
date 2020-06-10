from game import players


class TicTacToe:

    def __init__(self, player_x, player_o, size=3, first_step=None, next_step=None):
        self.size = size
        self.field = self.make_field()
        self.wins = players.make_wins(size)
        self.red_line = ''

        self.cells = None
        self.winners = []
        self.state = None
        self.count_steps = 0
        self.player = None
        self.change_player()

        self.player_x = self.player_choose(player_x, size)
        self.player_o = self.player_choose(player_o, size)

        self.next_step = next_step

        if first_step is not None:
            if len(first_step) == size ** 2:
                self.first_step(first_step)
            else:
                print("First step can't exist")
                self.add_to_cells()
                # self.print_cells()
                self.algorithm()

        else:
            self.add_to_cells()
            # self.print_cells()
            self.algorithm()

    def get_context(self):
        return {
            'size': self.size,
            'state': self.state,
            'field': self.field,
            'player_x': self.player_x,
            'player_o': self.player_o,
            'player': self.player,
            'counts': self.count_steps,
            'red_line': self.red_line
        }

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
        self.add_to_cells()
        # self.print_cells()
        self.algorithm()

    def algorithm(self):
        self.check_state()
        if self.state == 'game not finished':
            self.step()
        else:
            print(self.state)

    def step(self):
        # self.count_steps += 1
        if str(self.player_x) == str(self.player_o) == 'hard':
            self.count_steps = self.player_x.counts + self.player_o.counts
        self.change_player()
        # print(f'player {self.player} step:')
        if self.player == 'X':
            x, y = self.player_x.step(self.field, self.player, self.next_step)
            self.count_steps += self.player_x.counts
        else:  # if self.player == 'O':
            x, y = self.player_o.step(self.field, self.player, self.next_step)
            self.count_steps += self.player_o.counts
        self.field[x][y] = self.player
        self.add_to_cells()
        # self.print_cells()
        self.check_state()
        self.change_player()
        # self.algorithm()

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
                self.line_type(win)
                break

    def line_type(self, win):
        x_list = []
        y_list = []
        for xy in win:
            x_list.append(xy[0])
            y_list.append(xy[1])
        x_set = set(x_list)
        y_set = set(y_list)
        if len(x_set) == 1 and len(y_set) != 1:
            self.red_line += 'horizontal _'
            self.red_line += str(x_set.pop() + 1)
            self.red_line += str(self.size)
        elif len(y_set) == 1 and len(x_set) != 1:
            self.red_line += 'vertical _'
            self.red_line += str(y_set.pop() + 1)
            self.red_line += str(self.size)
        else:
            self.red_line += 'diagonal '
            if x_list[0] == y_list[0]:
                self.red_line += 'top'
            else:
                self.red_line += 'bottom'

    def check_draw(self):
        for win in self.wins:
            win_string = ''
            for xy in win:
                win_string += self.field[xy[0]][xy[1]]
            win_letters = win_string.replace(' ', '')
            win_set = set(win_letters)
            if len(win_set) == 2:
                continue
            else:
                return False
        return True

    def check_state(self):
        self.check_win_rows()
        all_cells = [m for n in self.field for m in n]
        all_x = [x for x in all_cells if x == 'X']
        all_o = [o for o in all_cells if o == 'O']
        if any((len(all_x) - len(all_o) > 1,
                len(all_o) - len(all_x) > 1)):
            self.state = 'Impossible'
        elif any((len(self.winners) == 0 and ' ' not in all_cells,
                  self.check_draw())):
            self.state = 'Draw'
        elif len(self.winners) == 0 and ' ' in all_cells:
            self.state = 'game not finished'
        else:
            if self.winners[0] == 'X':
                self.state = 'X wins'
            elif self.winners[0] == 'O':
                self.state = 'O wins'

        if any((self.state == 'Draw',
                self.state == 'X',
                self.state == 'O')):
            print(self.state)
