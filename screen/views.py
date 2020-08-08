from django.shortcuts import render


def main_page(request):
    return render(request, 'main_screen.html')

