import random

from django.shortcuts import render

from translations.db_adapter import translate, translations
from translations.models import Translation, Word

from .models import AnswerOptions, Question, Task


def generate_task(user, num_of_q, word_lang, translation_lang):

    new_task = Task.objects.create(user=user)
    used_words = []

    for i in range(num_of_q):
        word_to_guess = random.choice(
            Word.objects.filter(lang=word_lang).exclude(word__in=used_words)
        )
        used_words.append(word_to_guess)
        answer = random.choice(word_to_guess.targets.all()).source_word

        baits = set()
        bait_pool = Word.objects.filter(lang=translation_lang).exclude(
            word__in=translations(word_to_guess.word, translation_lang)
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
    return new_task


def start(request):
    return render(request, "translate_app/translate_start.html")
