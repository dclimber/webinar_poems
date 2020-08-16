from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PoetForm, PoemForm
from .models import Poet, Poem


def index(request):
    template_name = 'poems/poet_list.html'
    poets = list(Poet.objects.all())

    context = {
        'poets': poets,
    }
    return render(request, template_name, context)


def poet_view(request, pk):
    template_name = 'poems/poet_detail.html'

    poet = get_object_or_404(Poet, pk=pk)
    poems = poet.poem_set.all()
    divide_at = poems.count() // 2

    context = {
        'poet': poet,
        'poems': poems,
        'divide_at': divide_at
    }
    return render(request, template_name, context)


def poem_view(request, pk):
    template_name = 'poems/poem_detail.html'

    poem = get_object_or_404(Poem, pk=pk)

    context = {
        'poem': poem,
    }
    return render(request, template_name, context)


@login_required
def poem_create(request):
    template_name = 'poems/poem_form.html'
    # set author if provided
    poet_pk = request.GET.get('poet', None)
    initial = {}

    if poet_pk is not None:
        poet = Poet.objects.filter(pk=poet_pk).first()
        if poet is not None:
            initial['author'] = poet

    form = PoemForm(initial=initial)
    if request.method == 'POST':
        form = PoemForm(request.POST)
        if form.is_valid():
            poem = form.save()
            return redirect(poem.get_absolute_url())
    return render(request, template_name, {'form': form})


@login_required
def poem_update(request, pk):
    template_name = 'poems/poem_form.html'
    poem = get_object_or_404(Poem, pk=pk)
    form = PoemForm(request.POST or None, instance=poem)
    if form.is_valid():
        form.save()
        return redirect(poem.get_absolute_url())
    return render(request, template_name, {'form': form, 'poem': poem})


@login_required
def poem_delete(request, pk):
    template_name = 'poems/poem_confirm_delete.html'
    poem = get_object_or_404(Poem, pk=pk)
    poet_url = poem.author.get_absolute_url()
    if request.method == 'POST':
        poem.delete()
        return redirect(poet_url)
    return render(request, template_name, {'poem': poem})


@login_required
def poet_create(request):
    template_name = 'poems/poet_form.html'
    form = PoetForm()
    if request.method == 'POST':
        form = PoetForm(request.POST)
        if form.is_valid():
            poet = form.save()
            return redirect(poet.get_absolute_url())
    return render(request, template_name, {'form': form})


@login_required
def poet_update(request, pk):
    template_name = 'poems/poet_form.html'
    poet = get_object_or_404(Poet, pk=pk)
    form = PoetForm(request.POST or None, instance=poet)
    if form.is_valid():
        form.save()
        return redirect(poet.get_absolute_url())
    return render(request, template_name, {'form': form, 'poet': poet})


@login_required
def poet_delete(request, pk):
    template_name = 'poems/poet_confirm_delete.html'
    poet = get_object_or_404(Poet, pk=pk)
    if request.method == 'POST':
        poet.delete()
        return redirect('index')
    return render(request, template_name, {'poet': poet})
