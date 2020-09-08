from django.shortcuts import render

def start(request):
    return render(request, "translate_app/translate_start.html")
