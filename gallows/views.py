import random
import string

from django.db.models.functions import Length
from django.shortcuts import get_object_or_404, redirect, render

from translations.models import Word

from .forms import GuessForm, SettingsForm
from .models import Game

DIFFICULTY_COUNTER = {
    "easy": 3,
    "normal": 2,
    "hard": 1,
}

EDGE_LETTERS = 2
MIN_WORD_LENGTH = 3

CYRILLIC_LETTERS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
LANGUGE_LETTERS = {
    Word.Language.EN: [(key, key) for key in string.ascii_lowercase],
    Word.Language.RU: [(key, key) for key in CYRILLIC_LETTERS],
}

WORD_DB_COLUMN = Word._meta.get_field("word").__dict__["db_column"]


def mask_word(word, tried_letters):
    mask = (
        word[0]
        + "".join([letter if letter in tried_letters else "*" for letter in word[1:-1]])
        + word[-1]
    )
    return mask


def start(request):
    form = SettingsForm()
    if request.method == "POST":
        form = SettingsForm(request.POST)
        if form.is_valid():
            word_language = form.cleaned_data["language"]
            difficulty = form.cleaned_data["difficulty"]
            word_to_guess = random.choice(
                Word.objects.annotate(length=Length(WORD_DB_COLUMN))
                .filter(length__gt=MIN_WORD_LENGTH)
                .filter(lang=word_language)
            ).word.lower()
            tried_letters = ""
            word_to_show = mask_word(word_to_guess, tried_letters)
            counter = DIFFICULTY_COUNTER[difficulty] * (
                len(set(word_to_guess)) - EDGE_LETTERS
            )
            game = Game.objects.create(
                word_to_guess=word_to_guess,
                tried_letters=tried_letters,
                counter=counter,
                language=word_language,
            )
            game.save()
            return redirect("gallows_game", game_id=game.game_id)
    return render(request, "gallows/gallows_start.html", {"form": form})


def game(request, game_id):
    game = get_object_or_404(Game, game_id=game_id)
    choices = LANGUGE_LETTERS[game.language]
    word_to_show = mask_word(game.word_to_guess, game.tried_letters)
    form = GuessForm(choices)
    if request.method == "POST":
        form = GuessForm(choices, request.POST)
        if form.is_valid():
            current_guess = form.cleaned_data["current_guess"]
            game.tried_letters = "".join(set(game.tried_letters + current_guess))
            game.counter -= 1
            word_to_show = mask_word(game.word_to_guess, game.tried_letters)
            if "*" not in word_to_show:
                game.delete()
                return render(request, "gallows/gallows_win.html")
            if game.counter < 0:
                game.delete()
                return render(request, "gallows/gallows_gameover.html")
            game.save()
    context = {"form": form, "game": game, "word": word_to_show}
    return render(request, "gallows/gallows_game.html", context)
