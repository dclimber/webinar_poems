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
    poems = poet.poem_set.all()
    divide_at = poems.count() // 2

    context = {
        'poet': poet,
        'poems': poet.poem_set.all(),
        'divide_at': divide_at
    }
    return render(request, template_name, context)


def poem_view(request, poem_pk):
    template_name = 'poem.html'

    poem = get_object_or_404(Poem, pk=poem_pk)

    context = {
        'poem': poem,
    }
    return render(request, template_name, context)


def search(request):
    template_name = 'search.html'
    search = False

    context = {
        'search': search,
    }
    return render(request, template_name, context)
