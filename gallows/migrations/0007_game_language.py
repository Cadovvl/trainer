# Generated by Django 3.1 on 2020-08-15 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gallows", "0006_remove_game_word_to_show"),
    ]

    operations = [
        migrations.AddField(
            model_name="game",
            name="language",
            field=models.CharField(default="RU", max_length=2),
            preserve_default=False,
        ),
    ]
