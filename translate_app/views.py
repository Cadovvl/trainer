import random

from django.shortcuts import render

from translations.db_adapter import translate, translations
from translations.models import Translation, Word

from .models import AnswerOptions, Question, Task


def generate_task(user, num_of_q, word_lang, translation_lang):
    new_task = Task.objects.create(user=user)

    random_id_word = random.sample(
        list(
            Translation.objects.filter(
                source_word__lang=word_lang
            ).values_list("id", flat=True)
        ),
        num_of_q,
    )
    word_pool = list(Translation.objects.filter(id__in=random_id_word))

    exceptions = []
    for translation in word_pool:
        for word in translations(
            translation.source_word.word, translation_lang
        ):
            exceptions.append(word)

    random_id_bait = random.sample(
        list(
            Word.objects.filter(lang=translation_lang)
            .exclude(word__in=exceptions)
            .values_list("id", flat=True)
        ),
        num_of_q * 3,
    )

    bait_pool = list(Word.objects.filter(id__in=random_id_bait))

    for translation in word_pool:
        word_to_guess = translation.source_word
        answer = translation.target_word
        question = Question.objects.create(task=new_task, word=word_to_guess)
        options = AnswerOptions.objects.create(
            question=question,
            answer=answer,
            bait_1=bait_pool.pop(),
            bait_2=bait_pool.pop(),
            bait_3=bait_pool.pop(),
        )
    return new_task


def start(request):
    return render(request, "translate_app/translate_start.html")
