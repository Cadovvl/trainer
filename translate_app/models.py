from django.db import models

from users.models import CustomUser
from translations.models import Translation, Word
from translations.db_adapter import translate


class Task(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="translate_tasks",
        verbose_name="Пользователь",
        help_text="Пользователь, выполняющий задание",
    )
    status = models.BooleanField(
        default=False,
        verbose_name="Статус задания",
        help_text="Статус выполнения задания",
    )
    assessment = models.BooleanField(
        verbose_name="Оценка",
        help_text="Оценка правильности выполнения задания",
        null=True,
        blank=True,
    )


class Question(models.Model):
    task = models.ForeignKey(
        Task,
        related_name="questions",
        on_delete=models.CASCADE,
        verbose_name="Задание",
        help_text="Задание, содержащее слово",
    )
    word = models.CharField(
        max_length=20,
        verbose_name="Слово для перевода",
        help_text="Слово для перевода",
    )


class AnswerOptions(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="options",
        verbose_name="Варианты ответа",
        help_text="Варианты ответа на вопрос",
    )
    answer = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="+")
    bait_1 = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="+")
    bait_2 = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="+")
    bait_3 = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="+")
