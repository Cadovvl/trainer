from django.db import models

from translations.models import Word


class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    word_to_guess = models.CharField(max_length=20)
    counter = models.IntegerField("Осталось попыток", blank=True, null=True)
    tried_letters = models.CharField(max_length=40, blank=True, null=True)
    language = models.CharField(max_length=2, choices=Word.Language.choices)

    def __str__(self):
        return self.word_to_guess
