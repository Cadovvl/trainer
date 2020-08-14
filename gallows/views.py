import random

from django.shortcuts import render


def start(request):
    return render(request, "gallows/gallows_start.html")