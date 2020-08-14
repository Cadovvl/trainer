from django.shortcuts import render


def start(request):
    return render(request, "gallows/gallows_start.html")


def game(request):
    return render(request, "gallows/gallows_game.html")
