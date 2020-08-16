import string

from django import forms

from translations.models import Word


class SettingsForm(forms.Form):
    DIFFICULTIES = [("e", "Easy"), ("n", "Normal"), ("h", "Hard")]
    difficulty = forms.ChoiceField(
        label="Выберите уровень сложности", choices=DIFFICULTIES
    )
    language = forms.ChoiceField(label="Выберите язык", choices=Word.Language.choices)


class GuessForm(forms.Form):
    current_guess = forms.CharField(label="Введите букву", max_length=1)
