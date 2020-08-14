import random

from django.shortcuts import render

# from translations.models import Word


def start(request):
    return render(request, "gallows/gallows_start.html")

"""     word = random.choice(Word.objects.filter(length__gt=3)).word
    
    difficulty = 2 # would be user choice from easy/normal/hard = 3/2/1 for example
    counter = (len(word)-2) * difficulty

    context = {
        "word" : word,
        "counter" : counter
    }
 """

def game(request):
        return render(request, "gallows/gallows_game.html")




