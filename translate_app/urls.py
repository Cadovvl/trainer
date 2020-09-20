from django.urls import path

from . import views

urlpatterns = [
    path("", views.start, name="translate"),
    path(
        "translatetask/<int:task_id>/",
        views.translatetask,
        name="translate_task",
    ),
    path(
        "translatetask/<int:task_id>/result/",
        views.result,
        name="translate_result",
    ),
]
