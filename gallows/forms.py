import string

from django import forms


class DifficultyForm(forms.Form):
    DIFFICULTIES = [("e", "Easy"), ("n", "Normal"), ("h", "Hard")]
    difficulty = forms.ChoiceField(
        label="Выберите уровень сложности", choices=DIFFICULTIES
    )


class GuessForm(forms.Form):
    LETTER_CHOICES = [(key, key) for key in string.ascii_lowercase]
    current_guess = forms.ChoiceField(label="Выберите букву", choices=LETTER_CHOICES)
