from django.db import models


class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    word_to_guess = models.CharField(max_length=20) # ForeignKey(Word) ?
    word_to_show = models.CharField("Загаданное слово", max_length=20, blank=True, null=True)
    counter = models.IntegerField("Осталось попыток", blank=True, null=True)
    tried_letters = models.CharField(max_length=40, blank=True, null=True)
    
    class Meta:
        pass

    def __str__(self):
        return self.word_to_guess
 