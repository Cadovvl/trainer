from django.urls import path

from . import views

urlpatterns = [
    path("", views.start, name="gallows_start"),
    path("gallows_game/<int:game_id>/", views.game, name="gallows_game"),
]
