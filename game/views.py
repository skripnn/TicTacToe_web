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

        field_str = ' ' * size ** 2
        db_game = models.Game.objects.create(
            size=size,
            field_str=field_str,
            state='game not finished',
            player_x=player_x,
            player_o=player_o,
            player='X',
            counts=0
        )

        print(f'START GAME {db_game.id}')
        print(f'size = {size}')
        print(f'player X = {player_x}')
        print(f'player O = {player_o}')
        print('-----')

        return redirect(f'{db_game.id}/')


class GameContinue(View):
    def get(self, request, game_id):
        db_game = models.Game.objects.get(
            id=game_id
        )
        field = field_str_to_list(db_game.field_str, db_game.size)

        if any((db_game.player == 'X' and db_game.player_x == 'user',
                db_game.player == 'O' and db_game.player_o == 'user')):
            user_step = True
        else:
            user_step = False

        print('GET')
        print(f'game id = {game_id}')
        print(f'player_x = {db_game.player_x}')
        print(f'player_o = {db_game.player_o}')
        print(f'player = {db_game.player}')
        print(f'user_step = {user_step}')
        print(f'all counts = {db_game.counts}')
        print('-----')
        
        context = {
            'size': db_game.size,
            'state': db_game.state,
            'field': field,
            'player': db_game.player,
            'red_line': db_game.red_line,
            'user_step': user_step
        }

        return render(request, 'game/field.html', context=context)

    def post(self, request, game_id):
        db_game = models.Game.objects.get(
            id=game_id
        )
        
        if 'step' in request.POST:
            step = request.POST['step']
        else:
            step = None
        
        size = int(db_game.size)
        field_str = db_game.field_str
        player_x = db_game.player_x
        player_o = db_game.player_o
        
        print('POST')
        print(f'size = {size}')
        print(f'field_str = {field_str}')
        print(f'player X = {player_x}')
        print(f'player O = {player_o}')
        print(f'step = {step}')
        print('')

        context = game.TicTacToe(player_x, player_o, size, field_str, step).get_context()
        
        print('GOT CONTEXT')
        for key, value in context.items():
            if key == 'field':
                print(f'{key} =')
                for row in value:
                    print(row)
            else:
                print(f'{key} = {value}')
        print('-----')

        field_str = field_list_to_str(context['field'], context['size'])

        db_game.player = context['player']
        db_game.field_str = field_str
        db_game.state = context['state']
        db_game.counts += context['counts']
        db_game.red_line = context['red_line']
        db_game.save()

        return self.get(request, game_id)
