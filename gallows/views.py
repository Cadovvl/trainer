import random
import string

from django.db.models.functions import Length
from django.shortcuts import get_object_or_404, render

from translations.models import Word

from .forms import GuessForm, SettingsForm
from .models import Game

DIFFICULTY_COUNTER = {
    "e": 3,
    "n": 2,
    "h": 1,
}

LATIN_LETTERS = [(key, key) for key in string.ascii_lowercase]
CYRILLIC_LETTERS = [(key, key) for key in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"]


def mask_word(word, tried_letters):
    mask = (
        word[0]
        + "".join([letter if letter in tried_letters else "*" for letter in word[1:-1]])
        + word[-1]
    )
    return mask


def start(request):
    if request.method == "POST":
        form = SettingsForm(request.POST)
        if form.is_valid():
            word_language = form.cleaned_data["language"]
            difficulty = form.cleaned_data["difficulty"]
            word_to_guess = random.choice(
                Word.objects.annotate(length=Length("word"))
                .filter(length__gt=3)
                .filter(lang=word_language)
            ).word.lower()
            tried_letters = ""
            word_to_show = mask_word(word_to_guess, tried_letters)
            counter = DIFFICULTY_COUNTER[difficulty] * (len(word_to_guess) - 2)
            game = Game.objects.create(
                word_to_guess=word_to_guess,
                tried_letters=tried_letters,
                counter=counter,
                language=word_language.lower(),
            )
            game.save()
            context = {"form": form, "game": game, "word": word_to_show}
            return render(request, "gallows/gallows_game.html", context)
        return render(request, "gallows/gallows_start.html", {"form": form})
    form = SettingsForm()
    return render(request, "gallows/gallows_start.html", {"form": form})


def game(request, game_id):
    game = get_object_or_404(Game, game_id=game_id)
    LETTER_CHOICES = CYRILLIC_LETTERS if game.language == "ru" else LATIN_LETTERS
    if request.method == "POST":
        form = GuessForm(LETTER_CHOICES, request.POST)
        if form.is_valid():
            game.current_guess = form.cleaned_data["current_guess"]
            game.tried_letters = "".join(set(game.tried_letters + game.current_guess))
            word_to_show = mask_word(game.word_to_guess, game.tried_letters)
            game.counter -= 1

            if "*" not in word_to_show:
                game.delete()
                return render(request, "gallows/gallows_win.html")

            if game.counter == 0:
                game.delete()
                return render(request, "gallows/gallows_gameover.html")

            game.save()
            context = {"form": form, "game": game, "word": word_to_show}
            return render(request, "gallows/gallows_game.html", context)
        return render(
            request, "gallows/gallows_game.html", {"form": form, "game": game}
        )
    form = GuessForm(LETTER_CHOICES)
    return render(request, "gallows/gallows_game.html", {"form": form, "game": game})
