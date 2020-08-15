from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View, TemplateView

from poems.models import Poet, Poem


def search(request):
    template_name = 'search/search.html'
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
        'query': query,
    }
    return render(request, template_name, context)


class SearchView(View):

    def get(self, request):
        template_name = 'search/search.html'
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
            'query': query
        }
        return render(request, template_name, context)


class SearchTemplateView(TemplateView):
    template_name = 'search/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search = False

        query = self.request.GET.get('q', None)
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

        context['results'] = results
        context['search'] = search
        context['query'] = query
        return context
