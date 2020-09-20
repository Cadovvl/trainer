from enum import Enum

from django.db import models

# Create your models here.


class Word(models.Model):
    class Language(models.TextChoices):
        EN = 'EN'  # English
        RU = 'RU'  # Russian
        NO = 'NO'  # Norwegian

    word = models.CharField(max_length=200, db_column='word')
    lang = models.CharField(max_length=2, choices=Language.choices)

    def __str__(self):
        return f"{self.lang} - {self.word}"


class Translation(models.Model):
    source_word = models.ForeignKey(Word, on_delete=models.PROTECT, related_name='sources')
    target_word = models.ForeignKey(Word, on_delete=models.PROTECT, related_name='targets')

    priority = models.IntegerField()

    def __str__(self):
        return (f"({self.source_word}) перевод ({self.target_word})" 
        f" приоритет: {self.priority}")