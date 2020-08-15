import random

from django.db.models.functions import Length
from django.shortcuts import get_object_or_404, redirect, render

from translations.models import Word

from .forms import DifficultyForm, GuessForm
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
        form = DifficultyForm(request.POST)
        if form.is_valid():
            word_to_guess = random.choice(
                Word.objects.annotate(length=Length("word")).filter(length__gt=3)
            ).word.lower()
            tried_letters = ""
            word_to_show = mask_word(word_to_guess, tried_letters)
            difficulty = form.cleaned_data["difficulty"]
            counter = DIFFICULTY_COUNTER[difficulty] * (len(word_to_guess) - 2)
            game = Game.objects.create(
                word_to_guess=word_to_guess,
                tried_letters=tried_letters,
                word_to_show=word_to_show,
                counter=counter,
            )
            game.save()
            form = DifficultyForm()
            return render(
                request, "gallows/gallows_game.html", {"form": form, "game": game}
            )
        return render(request, "gallows/gallows_start.html", {"form": form})
    form = DifficultyForm()
    return render(request, "gallows/gallows_start.html", {"form": form})


def game(request, game_id):
    game = get_object_or_404(Game, game_id=game_id)
    if request.method == "POST":
        form = GuessForm(request.POST)
        if form.is_valid():
            current_guess = form.cleaned_data["current_guess"]
            game.current_guess = current_guess
            game.tried_letters = "".join(set(game.tried_letters + game.current_guess))
            game.word_to_show = mask_word(game.word_to_guess, game.tried_letters)
            game.counter -= 1

            if "*" not in game.word_to_show:
                game.delete()
                return render(request, "gallows/gallows_win.html")

            if game.counter == 0:
                game.delete()
                return render(request, "gallows/gallows_gameover.html")

            game.save()
            form = GuessForm()
            return render(
                request, "gallows/gallows_game.html", {"form": form, "game": game}
            )
        return render(
            request, "gallows/gallows_game.html", {"form": form, "game": game}
        )
    form = GuessForm()
    return render(request, "gallows/gallows_game.html", {"form": form, "game": game})
