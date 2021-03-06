# Generated by Django 3.1 on 2020-09-12 12:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("translations", "0002_auto_20200819_1925"),
        ("translate_app", "0002_auto_20200912_0255"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="word",
            field=models.ForeignKey(
                help_text="Слово для перевода",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="translations.word",
                verbose_name="Слово для перевода",
            ),
        ),
    ]
