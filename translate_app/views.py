import random

from django.shortcuts import render
from translations.models import Translation, Word
from translations.db_adapter import translate

from .models import AnswerOptions, Task, Question


def generate_task(user, num_of_q, word_lang, translation_lang):

    new_task = Task.objects.create(user=user)
    used_words = []

    for i in range(num_of_q):
        word_to_guess = random.choice(
            Word.objects.filter(lang=word_lang).exclude(word__in=used_words)
        ).word.lower()
        used_words.append(word_to_guess)
        answer = translate(word_to_guess, translation_lang)

        baits = {}
        bait_pool = (
            Word.objects.filter(lang=translation_lang)
            .exclude(word=answer)
            .word.lower()
        )
        while len(baits) < 3:
            baits.add(random.choice(bait_pool))

        question = Question.objects.create(task=new_task, word=word_to_guess)
        options = AnswerOptions.objects.create(
            question=question,
            answer=answer,
            bait_1=baits.pop(),
            bait_2=baits.pop(),
            bait_3=baits.pop(),
        )


def start(request):
    return render(request, "translate_app/translate_start.html")
