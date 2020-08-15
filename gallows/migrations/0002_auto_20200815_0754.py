# Generated by Django 3.1 on 2020-08-15 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallows', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='counter',
            field=models.IntegerField(blank=True, null=True, verbose_name='Осталось попыток'),
        ),
        migrations.AlterField(
            model_name='game',
            name='current_guess',
            field=models.CharField(blank=True, choices=[('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'd'), ('e', 'e'), ('f', 'f'), ('g', 'g'), ('h', 'h'), ('i', 'i'), ('j', 'j'), ('k', 'k'), ('l', 'l'), ('m', 'm'), ('n', 'n'), ('o', 'o'), ('p', 'p'), ('q', 'q'), ('r', 'r'), ('s', 's'), ('t', 't'), ('u', 'u'), ('v', 'v'), ('w', 'w'), ('x', 'x'), ('y', 'y'), ('z', 'z')], max_length=1, null=True, verbose_name='Выберите букву'),
        ),
        migrations.AlterField(
            model_name='game',
            name='word_to_show',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Загаданное слово'),
        ),
    ]
