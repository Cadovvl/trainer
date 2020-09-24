import random

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from translations.models import Translation, Word

from .forms import AnswerForm, SettingsForm
from .models import AnswerOptions, Question, Task

NUMBER_OF_QUESTIONS = 2


@transaction.atomic
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

    source_words = [translation.source_word.word for translation in word_pool]
    targets = list(
        Translation.objects.filter(
            source_word__word__in=source_words,
            target_word__lang=translation_lang,
        )
    )
    exceptions = [translation.target_word.word for translation in targets]

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


def task_status_check(task):
    return not task.questions.filter(status=False).exists()


def answer_options(question):
    options = [
        question.options.answer.word,
        question.options.bait_1.word,
        question.options.bait_2.word,
        question.options.bait_3.word,
    ]
    random.shuffle(options)
    return [(key, key) for key in options]


@login_required
def start(request):
    form = SettingsForm(request.POST or None)
    if form.is_valid():
        source_language = form.cleaned_data["source_language"]
        target_language = form.cleaned_data["target_language"]
        try:
            new_task = generate_task(
                request.user,
                NUMBER_OF_QUESTIONS,
                source_language,
                target_language,
            )
        except IndexError as e:
            return render(request, "translate_app/translate_taskerror.html")
        return redirect("give_question", task_id=new_task.id)
    return render(
        request, "translate_app/translate_initial.html", {"form": form}
    )


@login_required
def give_question(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.status == True:
        return redirect("translate_result", task_id=task_id)

    question = list(task.questions.filter(status=False))
    question.sort(key=lambda x:x.id) 
    question = question[0]

    form = AnswerForm(answer_options(question))
    return render(
        request,
        "translate_app/translate_question.html",
        {"form": form, "task": task, "question": question},
    )

@transaction.atomic
@login_required
def process_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    task = question.task
    form = AnswerForm(answer_options(question), request.POST)
    if form.is_valid():
        answer = form.cleaned_data["answer"]
        question.status = True
        question.assessment = (
            True if answer == question.options.answer.word else False
        )
        question.save()
        task.status = task_status_check(task)
        task.save()
        return redirect("give_question", task_id=task.id)
    

@login_required
def result(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    wrong_count = task.questions.filter(assessment=False).count()

    context = {
        "wrong_count": wrong_count,
    }
    return render(request, "translate_app/translate_result.html", context)
