# Generated by Django 3.1 on 2020-08-19 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gallows", "0009_game_language"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="language",
            field=models.CharField(
                choices=[("EN", "En"), ("RU", "Ru"), ("NO", "No")], max_length=2
            ),
        ),
    ]
