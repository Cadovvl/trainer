# Generated by Django 3.1 on 2020-08-15 18:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("gallows", "0005_auto_20200815_1341"),
    ]

    operations = [
        migrations.RemoveField(model_name="game", name="word_to_show",),
    ]