from typing import List, Dict

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from poems.models import Poem
from .parser import parse_html_file, TextPoem


def parser_directory_path(instance, filename):
    return f'parser/{filename}'


class PoemsFile(models.Model):
    poet = models.ForeignKey('poems.Poet', null=True, blank=True,
                             on_delete=models.SET_NULL)
    file = models.FileField(
        upload_to=parser_directory_path,
        validators=[FileExtensionValidator(
            allowed_extensions=("html",))],
    )
    processed = models.BooleanField('Обработан?', default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ('uploaded_at',)

    def __str__(self):
        return self.get_filename()

    def get_filename(self):
        name = self.file.name.split('/')[-1]
        return f"{name}"


@receiver(post_save, sender=PoemsFile)
def parse_file(sender: PoemsFile, instance: PoemsFile,
               created: bool, **kwargs: Dict) -> None:
    if created:  # runs only if file was created (uploaded)
        file_path: str = f"{settings.MEDIA_ROOT}/{instance.file.name}"
        text_poems: List[TextPoem] = parse_html_file(file_path)
        # create poems
        poems: List[Poem] = [
            Poem(
                author=instance.poet,
                title=text_poem.title,
                text=text_poem.text,
                year=text_poem.year
            ) for text_poem in text_poems
        ]
        # bulk create poems
        Poem.objects.bulk_create(poems)

        # mark PoemsFile as processed
        instance.processed = True
        instance.save()
