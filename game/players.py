import random
from copy import deepcopy
# TODO Научить Hard записывать в базу каждый счёт каждого просчитаного шага и читать их потом из базы, а не считать

def make_wins(size):  # create list with win combinations
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


class Mirrors:
    size = 3

    def horizontal(self, field):
        half = self.size // 2
        field1 = []
        field2 = []
        for i in range(half):
            field1.append(field[i])
            row = field[self.size - 1 - i]
            row.reverse()
            field2.append(row)

        if field1 == field2:
            field_new = deepcopy(field)
            for x in range(self.size):
                for y in range(self.size):
                    if x > half:
                        field_new[x][y] = '?'
            return field_new
        return field

    def vertical(self, field):
        half = self.size // 2
        field1 = []
        field2 = []
        for i in range(self.size):
            field1.append(field[i][:half])
            row = field[self.size - 1 - i][self.size - half:]
            row.reverse()
            field2.append(row)

        if field1 == field2:
            field_new = deepcopy(field)
            for x in range(self.size):
                for y in range(self.size):
                    if y > half:
                        field_new[x][y] = '?'
            return field_new
        return field

    def quarter(self, field):
        half = self.size // 2
        field1 = []
        field2 = []
        field3 = []
        field4 = []

        for i in range(half):
            field1.append(field[i][:half])
            row = field[i][self.size - half:]
            row.reverse()
            field2.append(row)
            field3.append(field[self.size - 1 - i][:half])
            row = field[self.size - 1 - i][self.size - half:]
            row.reverse()
            field4.append(row)

        if field1 == field2 == field3 == field4:
            if self.size % 2 == 1:
                field_new = deepcopy(field)
                for x in range(self.size):
                    for y in range(self.size):
                        if x > half or y > half:
                            field_new[x][y] = '?'
                return field_new
            return field1
        return field

    def main_diagonal(self, field):
        field1 = []
        field2 = []
        for i in range(self.size - 1):
            field1.append(field[i][:self.size - 1 - i])
            row = field[self.size - 1 - i][i + 1:]
            row.reverse()
            field2.append(row)

        if field1 == field2:
            field_new = deepcopy(field)
            for x in range(1, self.size):
                for y in reversed(range(1, self.size)):
                    field_new[x][y] = '?'
            return field_new
        return field

    def side_diagonal(self, field):
        field1 = []
        field2 = []
        for i in range(self.size - 1):
            field1.append(field[self.size - 1 - i][:self.size - 1 - i])
            row = field[i][i + 1:]
            row.reverse()
            field2.append(row)

        if field1 == field2:
            field_new = deepcopy(field)
            for x in range(1, self.size):
                for y in reversed(range(1, self.size)):
                    field_new[x][y] = '?'
            return field_new
        return field


class Easy:
    def __init__(self, size=3):
        self.wins = make_wins(size)
        self.size = len(self.wins[0])

    def __str__(self):
        return 'easy'

    def find_steps(self, field):  # return the list with all available steps
        steps = []
        for x in range(self.size):
            for y in range(self.size):
                if field[x][y] == ' ':
                    steps.append([x, y])
        return steps

    def step(self, field, side, none):
        print('Making move level "easy"')
        x, y = self.easy_step(field)
        return x, y

    def easy_step(self, field):  # random step
        steps = self.find_steps(field)
        step = random.choice(steps)
        x, y = step[0], step[1]
        return x, y


class Medium(Easy):

    def __str__(self):
        return 'medium'

    def step(self, field, side, none):
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


class Hard(Mirrors, Medium):
    count = 0
    counts = 0

    def counter(self, side, count=1, counts=1):
        self.count += count
        self.counts += counts
        print(f'side = {side}\ncount = {self.count}\ncounts = {self.counts}')

    def __str__(self):
        return 'hard'

    def step(self, field, side, none):
        self.count = 0
        print('Making move level "hard"')
        steps = self.find_steps(field)

        if self.size % 2 != 0:  # if size is odd
            c = self.size // 2  # c = center of field
            if len(steps) == self.size ** 2:  # if all steps available
                x, y = c, c
                self.counter(side)
                return x, y  # return step on center of field

            if field[c][c] != ' ' and self.size ** 2 - len(steps) == 1:  # if only center of filed is busy
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

        x, y = self.hard_step(field, side)
        return x, y

    def check_mirrors(self, field):
        if self.size % 2 != 0:
            steps = self.dict_steps(field)
            return steps, 'full'
        new_field = field
        part = 'full'
        if new_field == field:
            new_field = self.quarter(field)
            part = 'quarter'
        if new_field == field:
            new_field = self.main_diagonal(field)
            part = 'main_diagonal'
        if new_field == field:
            new_field = self.side_diagonal(field)
            part = 'side_diagonal'
        if new_field == field:
            new_field = self.horizontal(field)
            part = 'horizontal'
        if new_field == field:
            new_field = self.vertical(field)
            part = 'vertical'
        if new_field == field:
            part = 'full'
        steps = self.dict_steps(new_field)
        return steps, part

    def mirror_back(self, steps, part):
        if part == 'full':
            return steps

        half = self.size // 2
        full_steps = []
        s = self.size - 1
        for step in steps:
            full_steps.append(step)
            x, y = int(step[0]), int(step[1])
            if part == 'quarter':
                if x != half or y != half:
                    full_steps.append([x, s - y])
                    full_steps.append([s - x, y])
                    full_steps.append([s - x, s - y])
            elif part == 'main_diagonal':
                if x != s - y:
                    full_steps.append([s - x, s - y])
            elif part == 'side_diagonal':
                if x != y:
                    full_steps.append([y, x])
            elif part == 'horizontal':
                if x != half:
                    full_steps.append([s - x, s - y])
            elif part == 'vertical':
                if y != half:
                    full_steps.append([s - x, s - y])

        return full_steps

    def hard_step(self, field, side):  # minimax step
        # delete mirror steps
        # # steps, part = self.check_mirrors(field)
        steps = self.dict_steps(field)

        # score counting for each available step
        for xy, score in steps.items():
            result_score, level = self.minimax(field, int(xy[0]), int(xy[1]), side)
            steps[xy] = result_score

        maximum = max(steps.values())  # find maximum score
        # create the list with all maximum-score steps
        result_list = [xy for xy, score in steps.items() if score == maximum]
        # return mirror steps
        # # result_list = self.mirror_back(result_list, part)
        # choose a random step from list
        xy = random.choice(result_list)
        x, y = int(xy[0]), int(xy[1])
        self.counter(side, 0, 0)
        return x, y  # return random maximum-score step

    def dict_steps(self, field):  # return the dict with all available steps {step: score}
        steps = {}
        field_size = len(field)
        for x in range(field_size):
            for y in range(field_size):
                if field[x][y] == ' ':
                    steps[str(x) + str(y)] = 0
        return steps

    def minimax(self, field, x, y, side, level=1):
        k = 1 if level % 2 == 1 else -1  # k = result change factor (+ or -)
        self.count += 1
        self.counts += 1

        # check win combinations
        result = self.check_wins(field, x, y, side)
        # if win combination exists
        if result == 10:
            field[x][y] = ' '
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
            result_score, level = self.minimax(field, int(xy[0]), int(xy[1]), side, level)
            steps[xy] += result_score
        level -= 1
        field[x][y] = ' '
        return sum(steps.values()) + result * k, level

    def check_wins(self, field, x, y, side):  # check win combination on field with new step
        field[x][y] = side  # make step
        for win in self.wins:
            win_string = ''
            for xy in win:
                win_string += field[xy[0]][xy[1]]
            win_letters = win_string.replace(' ', '')
            win_set = set(win_letters)
            if len(win_letters) == self.size and len(win_set) == 1:
                return 10  # return 10 if win combination detected
        return -10  # return -10 if win combination not detected


class Human:

    def __str__(self):
        return 'user'

    def step(self, field, side, step):
        # coordinates = input('Enter the coordinates: ')
        # size = len(field[0])
        # x, y = self.make_xy_from_step(coordinates, size)
        x = int(step[0])
        y = int(step[1])
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
