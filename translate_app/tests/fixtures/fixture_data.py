import pytest

from translations.models import Translation, Word

Lang = Word.Language


@pytest.fixture
def database():
    Word.objects.bulk_create([
        Word(word='лук', lang=Lang.RU),
        Word(word='поклон', lang=Lang.RU),
        Word(word='нос', lang=Lang.RU),
        Word(word='стрела', lang=Lang.RU),
        Word(word='onion', lang=Lang.EN),
    ])

    words = Word.objects.all()

    translations = Translation.objects.bulk_create([
        Translation(source_word=words[0], target_word=words[4], priority=10),
        Translation(source_word=words[4], target_word=words[0], priority=5),
    ])

    return words