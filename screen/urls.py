from django.urls import path

from screen.views import main_page

urlpatterns = [
    path('', main_page, name="main_page"),
]


