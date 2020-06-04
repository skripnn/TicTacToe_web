import random


def make_wins(size=3):  # create list with win combinations

    wins_xy = []
    for x in range(size):
        wins_xy.append([])
        for y in range(size):
            wins_xy[x].append([x, y])

    wins_yx = []
    for y in range(size):
        wins_yx.append([])
        for x in range(size):
            wins_yx[y].append([x, y])

    wins_d = [[], []]
    for x, y in enumerate(reversed(range(size))):
        wins_d[0].append([x, x])
        wins_d[1].append([x, y])

    wins = wins_xy + wins_yx + wins_d
    return wins


class Easy:
    def __init__(self):
        self.wins = make_wins()
        self.size = len(self.wins[0])

    def find_steps(self, field):  # return the list with all available steps
        steps = []
        for x in range(self.size):
            for y in range(self.size):
                if field[x][y] == ' ':
                    steps.append([x, y])
        return steps

    def step(self, field, side):
        print('Making move level "easy"')
        x, y = self.easy_step(field)
        return x, y

    def easy_step(self, field):  # random step
        steps = self.find_steps(field)
        step = random.choice(steps)
        x, y = step[0], step[1]
        return x, y


class Medium(Easy):

    def step(self, field, side):
        print('Making move level "medium"')
        step = self.medium_step(field, side)
        if step is None:
            step = self.easy_step(field)
        return step

    def medium_step(self, field, side):  # find the win combination without one element
        for win in self.wins:
            win_string = ''
            for xy in win:
                win_string += field[xy[0]][xy[1]]
            win_letters = win_string.replace(' ', '')
            win_set = set(win_letters)
            if len(win_letters) == self.size - 1 and len(win_set) == 1:
                option = win_string.index(' ')
                x = win[option][0]
                y = win[option][1]
                if str(win_set) == side:
                    return x, y  # return self win
        try:  # if combination is exist
            return x, y  # return step for break rival's win
        except NameError:  # else
            return None  # return None


class Hard(Medium):
    count = 0
    counts = 0

    def counter(self, side, count=1, counts=1):
        self.count += count
        self.counts += counts
        print(f'side = {side}\ncount = {self.count}\ncounts = {self.counts}')

    def step(self, field, side):
        self.count = 0
        print('Making move level "hard"')
        steps = self.find_steps(field)

        if self.size % 2 != 0:  # if size is odd
            c = self.size % 2  # c = center of field
            if len(steps) == len(self.size ** 2):  # if all steps available
                x, y = c, c
                self.counter(side)
                return x, y  # return step on center of field

            if field[c][c] != ' ' and len(self.size ** 2) - len(steps) == 1:  # if only center of filed is busy
                x = random.choice([0, self.size - 1])
                y = random.choice([0, self.size - 1])
                self.counter(side)
                return x, y  # return step in a random angle

        if len(steps) == 1:  # if only one step available
            x, y = steps[0][0], steps[0][1]
            self.counter(side)
            return x, y  # return the step

        try:  # try to find medium_level step
            x, y = self.medium_step(field, side)
        except TypeError:  # if medium_level step doesn't exist
            pass  # pass this part
        else:
            self.counter(side)
            return x, y  # else return the step

        self.hard_step(field, side, steps)

    def hard_step(self, field, side, steps_list):       # minimax step
        steps = self.dict_steps(field)

        # score counting for each available step
        for xy, score in steps.items():
            result_score, level = self.minimax(field, int(xy[0]), int(xy[1]), side, score)
            steps[xy] = result_score

        maximum = max(steps.values())       # find maximum score
        # create the list with all maximum-score steps
        result_list = [xy for xy, score in steps.items() if score == maximum]
        # choose a random step from list
        xy = random.choice(result_list)
        x, y = int(xy[0]), int(xy[1])
        self.counter(side, 0, 0)
        return x, y     # return random maximum-score step

    def dict_steps(self, field):        # return the dict with all available steps {step: score}
        steps = {}
        for x in range(3):
            for y in range(3):
                if field[x][y] == ' ':
                    steps[str(x) + str(y)] = 0
        return steps

    def minimax(self, field, x, y, side, score, level=1):
        k = 1 if level % 2 == 1 else -1     # k = result change factor (+ or -)
        self.count += 1
        self.counts += 1

        # check win combinations
        result = self.check_wins(field, x, y, side)
        # if win combination exists
        if result == 10:
            return 10 * k, level

        # level = deep of maximum recursion
        if level == 3:  # level limiter
            field[x][y] = ' '
            return -10 * k, level

        # change side
        side = 'X' if side == 'O' else 'O'
        # find available steps for next step
        steps = self.dict_steps(field)

        # start of recursion
        level += 1
        for xy, score in steps.items():
            new_score = score + result * k
            result_score, level, max_level = self.minimax(field, int(xy[0]), int(xy[1]), side, new_score, level)
            steps[xy] += result_score
        level -= 1
        field[x][y] = ' '
        return sum(steps.values()) + result * k, level

    def check_wins(self, field, x, y, side):        # check win combination on field with new step
        field[x][y] = side      # make step
        for win in self.wins:
            win_string = ''
            for xy in win:
                win_string += field[xy[0]][xy[1]]
            win_letters = win_string.replace(' ', '')
            win_set = set(win_letters)
            if len(win_letters) == self.size and len(win_set) == 1:
                return 10       # return 10 if win combination detected
        return -10      # return -10 if win combination not detected


class Human:
    def step(self, field, side):
        coordinates = input('Enter the coordinates: ')
        size = len(field[0])
        x, y = self.make_xy_from_step(coordinates, size)
        return x, y

    def make_xy_from_step(self, step, size):
        step = step.replace(' ', '')
        x = int(step[1]) - 1
        y = int(step[0]) - 1
        if x == size - 1:
            x = 0
        elif x == 0:
            x = size - 1
        return x, y


# TODO переделать шаги на координаты, посмотреть весь класс и причесать
class TicTacToe:

    def __init__(self, player_x, player_o, size=3):
        self.size = size
        self.field = self.make_field()
        self.wins = make_wins()

        self.cells = None
        self.winners = []
        self.state = None
        self.count_steps = 0
        self.player = 'X'

        self.player_x = player_x
        self.player_o = player_o

        # self.first_step('O_XX_X_OO')
        self.algorithm()

    def make_field(self):
        field = []
        for x in range(self.size):
            field.append([' ' for y in range(self.size)])
        return field

    def first_step(self, steps):
        for x in range(3):
            for y in range(3):
                step = steps[y + x * 3]
                if step == 'X' or step == 'O':
                    self.field[x][y] = step
        self.algorithm()

    def algorithm(self):
        # all_counts = self.player_x.counts + self.player_o.counts
        # print(f'all counts = {all_counts}')
        self.add_to_cells()
        self.print_cells()
        self.check_state()
        if self.state == 'Game not finished':
            self.change_player()
            self.count_steps += 1
            self.step()
        else:
            print(self.state)
            print('')

    def step(self):
        step = None
        print(f'player {self.player} step:')
        if self.player == 'X':
            step = self.player_x.step(self.field, self.player)
        elif self.player == 'O':
            step = self.player_o.step(self.field, self.player)

        if self.count_steps == 0:
            self.first_step(step)
        else:
            if not self.check_step(step):
                self.step()
            else:
                x, y = self.make_coordinates(step)
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

    def make_coordinates(self, step):
        step = step.replace(' ', '')
        x = int(step[1]) - 1
        y = int(step[0]) - 1
        if x == 2:
            x = 0
        elif x == 0:
            x = 2
        return x, y

    def check_step(self, step):
        step = step.replace(' ', '')
        if not step.isdigit():
            print('You should enter numbers!')
            return False
        elif len(step) != 2:
            print('You should enter two numbers!')
            return False
        for _ in step:
            if int(_) > 3 or int(_) < 1:
                print('Coordinates should be from 1 to 3!')
                return False
        x, y = self.make_coordinates(step)
        if self.field[x][y] != ' ':
            print('This cell is occupied! Choose another one!')
            return False
        return True

    def enter_the_coordinates(self):
        print('Enter the coordinates: ', end='')

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
            _ = ''
            for coordinate in win:
                x = coordinate[0]
                y = coordinate[1]
                _ += self.field[x][y]
            if _[0] == _[1] == _[2] == 'X' or _[0] == _[1] == _[2] == 'O':
                self.winners.append(_[0])

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
            self.state = 'Game not finished'
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

    def input(self, command, args):
        if command == 'start':
            if len(args) != 2:
                return self.bad_parameters()
            players = []
            for arg in args:
                players.append(self.player_choose(arg))
                if players[-1] is None:
                    return self.bad_parameters()
            return TicTacToe(*players)
        if command == 'exit':
            exit()
        else:
            print('Wrong command!')

    def player_choose(self, player):
        if player == 'user':
            return Human()
        if player == 'easy':
            return Easy()
        if player == 'medium':
            return Medium()
        if player == 'hard':
            return Hard()
        return None

    def bad_parameters(self):
        print('Bad parameters!')
        return None
