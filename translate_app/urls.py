from django.urls import path

from . import views

urlpatterns = [
    path("", views.start, name="translate"),
    path(
        "translatetask/<int:task_id>/",
        views.give_question,
        name="give_question",
    ),
    path(
        "translatetask/answer/<int:question_id>/",
        views.process_answer,
        name="process_answer",
    ),
    path(
        "translatetask/<int:task_id>/result/",
        views.result,
        name="translate_result",
    ),
]
