# Generated by Django 3.1 on 2020-08-16 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("gallows", "0007_game_language"),
    ]

    operations = [
        migrations.RemoveField(model_name="game", name="language",),
    ]