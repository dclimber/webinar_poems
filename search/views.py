from django.db.models import Q
from django.shortcuts import render

from poems.models import Poet, Poem


def search(request):
    template_name = 'poems/search.html'
    search = False

    query = request.GET.get('q', None)
    if query is not None:
        search = True

        poets = list(Poet.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        ))
        poems = list(Poem.objects.filter(
            Q(title__icontains=query) | Q(text__icontains=query)
        ))
        results = poets + poems
    else:
        results = []

    context = {
        'results': results,
        'search': search,
    }
    return render(request, template_name, context)
