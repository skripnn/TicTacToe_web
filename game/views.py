from django.shortcuts import render
from django.views import View
from TicTacToe_web import game


class Game(View):
    def get(self, request):
        return render(request, 'game/start_form.html')

    def post(self, request):
        size = int(request.POST['size'])
        field = request.POST['field']
        player_x = request.POST['player_x']
        player_o = request.POST['player_o']
        print(f'size = {size}')
        print(f'field = {field}')
        print(f'player X = {player_x}')
        print(f'player O = {player_o}')

        context = game.Menu().input('start', [player_x, player_o], size)

        return render(request, 'game/result.html', context=context)
