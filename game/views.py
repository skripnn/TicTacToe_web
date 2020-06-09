from django.shortcuts import render, redirect
from django.views import View
from game import game
from . import models


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


class Game(View):
    def get(self, request):
        return render(request, 'game/start_form.html')

    def post(self, request):
        size = int(request.POST['size'])
        if request.POST['field'] != '':
            field = request.POST['field']
        else:
            field = None
        player_x = request.POST['player_x']
        player_o = request.POST['player_o']
        print(f'size = {size}')
        print(f'field = {field}')
        print(f'player X = {player_x}')
        print(f'player O = {player_o}')

        # my_game = game.Menu().input('start', [player_x, player_o], size, field)
        # print(my_game)
        # str_field = field_list_to_str(my_game['field'], my_game['size'])
        # db_game = models.Game.objects.create(
        #     size=my_game['size'],
        #     field=str_field,
        #     state=my_game['state'],
        #     player_x=my_game['player_x'],
        #     player_o=my_game['player_o'],
        # )
        if request.POST['field'] != '':
            field = request.POST['field']
        else:
            field = ' ' * size ** 2
        db_game = models.Game.objects.create(
            size=size,
            field=field,
            state='game not finished',
            player_x=player_x,
            player_o=player_o,
        )
        return redirect(f'{db_game.id}/')


class GameContinue(View):
    def get(self, request, game_id):
        my_game = models.Game.objects.get(
            id=game_id
        )
        cells = field_str_to_list(my_game.field, my_game.size)
        print(cells)
        context = {
            'size': my_game.size,
            'state': my_game.state,
            'cells': cells
        }
        return render(request, 'game/result.html', context=context)

    def post(self, request, game_id):
        db_game = models.Game.objects.get(
            id=game_id
        )
        step = request.POST['step']
        size = int(db_game.size)
        field = db_game.field
        player_x = db_game.player_x
        player_o = db_game.player_o
        print(f'size = {size}')
        print(f'field = {field}')
        print(f'player X = {player_x}')
        print(f'player O = {player_o}')
        print(f'step = {step}')

        step = game.Menu().input('start', [player_x, player_o], size, field, step)
        print(step)
        str_field = field_list_to_str(step['field'], step['size'])
        db_game.field = str_field
        db_game.state = step['state']
        db_game.save()

        return self.get(request, game_id)
