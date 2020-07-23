import textwrap
from django.db import models


class Poet(models.Model):
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150,
                                 blank=True, null=True)
    bio = models.TextField('Биография', null=True, blank=True)
    photo_url = models.URLField('Ссылка на фото', null=True, blank=True)

    class Meta:
        verbose_name = 'Поэт(эсса)'

    def __str__(self):
        return (f"{self.first_name} {self.last_name}"
                if self.last_name is not None
                else f"{self.first_name}")


class Poem(models.Model):
    author = models.ForeignKey('Poet', on_delete=models.CASCADE,
                               verbose_name="Автор(ша)")
    title = models.CharField('Название', max_length=250, blank=True, null=True)
    text = models.TextField('Текст')
    year = models.CharField('Год(ы)', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'Стихотворение'

    def __str__(self):
        return (self.title if self.title is not None
                else textwrap.wrap(self.text)[0])
