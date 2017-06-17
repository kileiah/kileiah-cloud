from django.shortcuts import render

from django.http import HttpResponse


from .gamelogic import GameLevel

def index(request):
    level = GameLevel(request.session)
    if request.method == 'POST':
        if 'reset' in request.POST:
            request.session.flush()
        elif level.has_name():
            action = request.POST.get('action', None)
            level.perform_action(action)
        else:
            name = request.POST.get('name', None)
            level.set_name(name)
    return level.get_response(request)



