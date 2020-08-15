import string

from django.db import models


class Game(models.Model):
    DIFFICULTIES = [
        ('e', 'Easy'),
        ('n', 'Normal'),
        ('h', 'Hard')
    ]
    
    LETTER_CHOICES = [(key, key) for key in string.ascii_lowercase]

    word_to_guess = models.CharField(max_length=20) # ForeignKey(Word) ?
    word_to_show = models.CharField("Загаданное слово", max_length=20, blank=True, null=True)
    difficulty = models.CharField("Выберите уровень сложности", max_length=10, choices=DIFFICULTIES)
    counter = models.IntegerField("Осталось попыток", blank=True, null=True)
    tried_letters = models.CharField(max_length=40, blank=True, null=True)
    current_guess = models.CharField("Выберите букву", max_length=1, blank=True, null=True, choices=LETTER_CHOICES)
    
    class Meta:
        pass

    def __str__(self):
        return self.word_to_guess
 