from django import forms
from .models import Poet, Poem


class PoetForm(forms.ModelForm):
    class Meta:
        model = Poet
        fields = '__all__'


class PoemForm(forms.ModelForm):
    class Meta:
        model = Poem
        fields = '__all__'
