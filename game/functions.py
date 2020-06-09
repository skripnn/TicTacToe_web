def field_list_to_str(list_field, size):
    str_field = ''
    for x in range(size):
        for y in range(size):
            str_field += list_field[x][y]
    return str_field


def field_str_to_list(str_field, size):
    list_field = []
    for x in range(size):
        list_field.append([])
        for y in range(size):
            list_field[x].append(str_field[x * size + y])
    return list_field


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
