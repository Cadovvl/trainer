from django.urls import path

from . import views


urlpatterns = [
    path('', views.start, name="gallows_start"),
    path('game/', views.game, name="gallows_game"),
]

