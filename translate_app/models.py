from django.db import models

from users.models import CustomUser


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
        help_text="Статус выполнения задания"
    )
    assessment = models.BooleanField(
        verbose_name="Оценка",
        help_text="Оценка правильности выполнения задания"
    )
    

    def __str__(self):
        return self.taskword


class Question(models.Model):
    word = models.CharField(
        max_length=20,
        verbose_name="Слово для перевода",
        help_text="Слово для перевода",
    )
    task = models.ForeignKey(
        Task,
        related_name='questions',
        on_delete=models.CASCADE,
        verbose_name="Задание",
        help_text="Задание, содержащее слово"
    )
    answer_options = models.JSONField()