from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PoetForm, PoemForm
from .models import Poet, Poem


def index(request):
    template_name = 'poems/index.html'
    poets = list(Poet.objects.all())

    context = {
        'poets': poets,
    }
    return render(request, template_name, context)


def poet_view(request, poet_pk):
    template_name = 'poems/poet.html'

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
    template_name = 'poems/poem.html'

    poem = get_object_or_404(Poem, pk=poem_pk)

    context = {
        'poem': poem,
    }
    return render(request, template_name, context)


@login_required
def add_poem(request):
    template_name = 'poems/poem_form.html'
    form = PoemForm()
    if request.method == 'POST':
        form = PoemForm(request.POST)
        if form.is_valid():
            poem = form.save()
            return redirect(poem.get_absolute_url())
    return render(request, template_name, {'form': form})


@login_required
def update_poem(request, poem_pk):
    template_name = 'poems/poem_form.html'
    poem = get_object_or_404(Poem, pk=poem_pk)
    form = PoemForm(instance=poem)
    if request.method == 'POST':
        form = PoemForm(request.POST)
        if form.is_valid():
            poem = form.save()
            return redirect(poem.get_absolute_url())
    return render(request, template_name, {'form': form, 'edit': True})


@login_required
def delete_poem(request, poem_pk):
    template_name = 'poems/poem_confirm_delete.html'
    poem = get_object_or_404(Poem, pk=poem_pk)
    poet_url = poem.author.get_absolute_url()
    if request.method == 'POST':
        poem.delete()
        return redirect(poet_url)
    return render(request, template_name, {'poem': poem})
