from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy

from .models import Poet, Poem


class Index(ListView):
    model = Poet
    context_object_name = 'poets'


class PoetView(DetailView):
    model = Poet
    context_object_name = 'poet'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        poet = context['poet']
        poems = poet.poem_set.all()
        divide_at = poems.count() // 2

        context['poems'] = poems
        context['divide_at'] = divide_at
        return context


class PoemView(DetailView):
    model = Poem
    context_object_name = 'poem'


class PoemCreate(CreateView):
    model = Poem
    fields = '__all__'

    def get_initial(self):
        poet_pk = self.request.GET.get('poet', None)
        initial = {}
        if poet_pk is not None:
            poet = Poet.objects.filter(pk=poet_pk).first()
            if poet is not None:
                initial['author'] = poet
        return initial


class PoemUpdate(UpdateView):
    model = Poem
    fields = '__all__'


class PoemDelete(DeleteView):
    model = Poem
    success_url = reverse_lazy('index')

    def get_success_url(self):
        poem = self.get_object()
        success_url = poem.author.get_absolute_url()
        return success_url


class PoetCreate(CreateView):
    model = Poet
    fields = '__all__'


class PoetUpdate(UpdateView):
    model = Poet
    fields = '__all__'


class PoetDelete(DeleteView):
    model = Poet
    success_url = reverse_lazy('index')
