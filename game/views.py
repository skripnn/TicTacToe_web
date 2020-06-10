from django.shortcuts import render, redirect
from django.views import View
from game import game
from . import models
from .functions import field_str_to_list, field_list_to_str


class Game(View):
    def get(self, request):
        return render(request, 'game/start_form.html')

    def post(self, request):
        size = int(request.POST['size'])
        player_x = request.POST['player_x']
        player_o = request.POST['player_o']
        print(f'size = {size}')
        print(f'player X = {player_x}')
        print(f'player O = {player_o}')

        field = ' ' * size ** 2
        db_game = models.Game.objects.create(
            size=size,
            field=field,
            state='game not finished',
            player_x=player_x,
            player_o=player_o,
            player='X'
        )
        return redirect(f'{db_game.id}/')


class GameContinue(View):
    def get(self, request, game_id):
        my_game = models.Game.objects.get(
            id=game_id
        )
        cells = field_str_to_list(my_game.field, my_game.size)
        print(cells)
        print('GET')
        print(f'my_game.player = {my_game.player}')
        print(f'player_x = {my_game.player_x}')
        print(f'player_o = {my_game.player_o}')

        if any((my_game.player == 'X' and my_game.player_x == 'user',
               my_game.player == 'O' and my_game.player_o == 'user')):
            user_step = True
        else:
            user_step = False

        print(f'user_step = {user_step}')
        context = {
            'size': my_game.size,
            'state': my_game.state,
            'cells': cells,
            'player': my_game.player
        }

        if any((
                my_game.state == 'Draw',
                my_game.state == 'X',
                my_game.state == 'O'
        )):
            my_game.delete()

        if user_step:
            return render(request, 'game/field_user.html', context=context)
        return render(request, 'game/field_ai.html', context=context)

    def post(self, request, game_id):
        db_game = models.Game.objects.get(
            id=game_id
        )
        print('TEST')
        if 'step' in request.POST:
            step = request.POST['step']
        else:
            step = None
        size = int(db_game.size)
        field = db_game.field
        player_x = db_game.player_x
        player_o = db_game.player_o
        print('POST')
        print(f'size = {size}')
        print(f'field = {field}')
        print(f'player X = {player_x}')
        print(f'player O = {player_o}')
        print(f'step = {step}')

        step = game.Menu().input('start', [player_x, player_o], size, field, step)
        print(step)

        str_field = field_list_to_str(step['field'], step['size'])
        db_game.player = step['player']
        db_game.field = str_field
        db_game.state = step['state']
        db_game.save()

        return self.get(request, game_id)


class DB(View):
    def get(self, request):
        self.delete()
        return redirect('../')

    def delete(self):
        games = models.Game.objects.all()
        for i in games:
            print(f'{i} is deleting')
        games.delete()
        print('Database is clear')
