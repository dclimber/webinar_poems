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
