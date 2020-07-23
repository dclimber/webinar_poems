from django.shortcuts import render, get_object_or_404

from .models import Poet, Poem


def index(request):
    template_name = 'index.html'
    poets = list(Poet.objects.all())

    context = {
        'poets': poets,
    }
    return render(request, template_name, context)


def poet_view(request, poet_pk):
    template_name = 'poet.html'

    poet = get_object_or_404(Poet, pk=poet_pk)

    context = {
        'poet': poet,
    }
    return render(request, template_name, context)
