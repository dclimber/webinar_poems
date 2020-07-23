from django.shortcuts import render

from .models import Poet, Poem


def index(request):
    template_name = 'index.html'
    poets = list(Poet.objects.all())

    context = {
        'poets': poets,
    }
    return render(request, template_name, context)
