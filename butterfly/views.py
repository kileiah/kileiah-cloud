from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    context = {
        'eaten': False,
        'big': False
    }
    request.session.set_expiry(100)
    if request.method == 'POST':
        food = request.POST.get('food', None)
        if food is not None:
            request.session['eaten'] = True
            if 'food' not in request.session:
                request.session['food'] = []
            elif len(request.session['food']) >= 10:
                request.session['big'] = True
            request.session['food'].append(food)
            print(request.session.__dict__)
        elif 'reset' in request.POST:
            request.session.flush()
    if request.session.get('eaten', False):
        context['eaten'] = True
        context['food'] = request.session['food']
    if request.session.get('big', False):
        context['big'] = True
        context['big'] = request.session['big']
    return render(request, 'butterfly/index.html', context)
