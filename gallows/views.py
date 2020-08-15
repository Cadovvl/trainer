import random

from django.shortcuts import redirect, render
from django.db.models.functions import Length

from translations.models import Word

from .forms import GameForm
from .models import Game


DIFFICULTY_COUNTER = {
    "e": 3,
    "n": 2,
    "h": 1,
}


def mask_word(word, tried_letters):
    guess_part = word[1:-1]
    masked_part = ""
    for letter in guess_part:
        if letter not in tried_letters:
            masked_part += "*"
        else:
            masked_part += letter
    return word[0] + masked_part + word[-1]


def start(request):
    if request.method == "POST":
        form = GameForm(request.POST)
        if form.is_valid():
            word_to_guess = random.choice(
                Word.objects.annotate(length=Length('word')).filter(length__gt=3)
            ).word.lower()
            tried_letters = ""
            word_to_show = mask_word(word_to_guess, tried_letters)
            difficulty = form.cleaned_data["difficulty"]
            counter = DIFFICULTY_COUNTER[difficulty] * (len(word_to_guess) - 2)
            game = Game.objects.create(
                word_to_guess=word_to_guess,
                tried_letters=tried_letters,
                word_to_show=word_to_show,
                difficulty=difficulty,
                counter=counter,
            )
            form = GameForm(instance=game)
            context = {"form": form, "game": game}
            return render(request, "gallows/gallows_game.html", context=context)
        return render(request, "gallows/gallows_start.html", {"form": form})
    form = GameForm()
    return render(request, "gallows/gallows_start.html", {"form": form})


def game(request):
    if request.method == "POST":
        form = GameForm(request.POST)
        if form.is_valid():
            # word_to_guess = ?
            current_guess = form.cleaned_data["current_guess"]
            # tried_letters = "".join(set( ? + current_guess))
            word_to_show = mask_word(word_to_guess, tried_letters)
            # counter = ?
            if counter == 0:
                return render(request, "gallows/gallows_gameover.html")

            context = {
                "form": form
            }
            return render(request, "gallows/gallows_game.html", context=context)
        return render(request, "gallows/gallows_game.html", {"form": form})
    form = GameForm()
    return render(request, "gallows/gallows_game.html", {"form": form})
