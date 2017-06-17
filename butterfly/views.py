from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    context = {
        'eaten': False
    }
    if request.method == 'POST':
        food = request.POST.get('food', None)
        if food is not None:
            request.session['eaten'] = True
            if 'food' not in request.session:
                request.session['food'] = []
            request.session['food'].append(food)
            print(request.session.__dict__)
    request.session.set_expiry(5)
    if request.session.get('eaten', False):
        context['eaten'] = True
        context['food'] = request.session['food']
    return render(request, 'butterfly/index.html', context)
