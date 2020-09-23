from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from translations.models import Word

from .models import AnswerOptions, Question, Task


class SettingsForm(forms.Form):
    source_language = forms.ChoiceField(
        label="Выберите язык слов",
        choices=Word.Language.choices,
        widget=forms.RadioSelect,
    )
    target_language = forms.ChoiceField(
        label="Выберите язык перевода",
        choices=Word.Language.choices,
        widget=forms.RadioSelect,
    )

    def clean(self):
        cleaned_data = super().clean()
        s_lang = cleaned_data.get("source_language")
        t_lang = cleaned_data.get("target_language")

        if s_lang and t_lang and s_lang == t_lang:
            raise ValidationError(
                "Translation language must be different from the source one. "
            )


class AnswerForm(forms.Form):
    answer = forms.ChoiceField(
        widget=forms.RadioSelect, label="Варианты ответа", choices=[],
    )

    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["answer"].choices = choices
