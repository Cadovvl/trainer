from django.urls import path

from screen.views import main_page

screen_urls = [
    path('', main_page, name="main_page"),
]


