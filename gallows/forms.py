from django import forms

from translations.models import Word

from .models import Game


class SettingsForm(forms.Form):
    DIFFICULTIES = [("easy", "Easy"), ("normal", "Normal"), ("hard", "Hard")]
    difficulty = forms.ChoiceField(
        widget=forms.RadioSelect,
        label="Выберите уровень сложности",
        choices=DIFFICULTIES
    )
    language = forms.ChoiceField(widget=forms.RadioSelect, label="Выберите язык", choices=Word.Language.choices)


class GuessForm(forms.Form):
    current_guess = forms.ChoiceField(widget=forms.RadioSelect, choices=[])

    def __init__(self, choices, *args, **kwargs):
        super(GuessForm, self).__init__(*args, **kwargs)
        self.fields["current_guess"].choices = choices
