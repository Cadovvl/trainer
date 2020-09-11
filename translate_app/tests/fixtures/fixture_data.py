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
        # Word(word='дерево', lang=Lang.RU),
        # Word(word='вода', lang=Lang.RU),
        # Word(word='ветер', lang=Lang.RU),
        
        Word(word='onion', lang=Lang.EN),
        # Word(word='bow', lang=Lang.EN),
        # Word(word='nose', lang=Lang.EN),        
        # Word(word='arrow', lang=Lang.EN),
        # Word(word='tree', lang=Lang.EN),
        # Word(word='water', lang=Lang.EN),
        # Word(word='wind', lang=Lang.EN),


    ])

    words = Word.objects.all()

    translations = Translation.objects.bulk_create([
        Translation(source_word=words[0], target_word=words[4], priority=10),
        Translation(source_word=words[4], target_word=words[0], priority=5),


        # Translation(source_word=words[0], target_word=words[7], priority=10),
        # Translation(source_word=words[0], target_word=words[8], priority=5),
        # Translation(source_word=words[7], target_word=words[0], priority=5),
        # Translation(source_word=words[8], target_word=words[0], priority=15),
        # Translation(source_word=words[8], target_word=words[1], priority=10),
        # Translation(source_word=words[8], target_word=words[2], priority=5),

        # Translation(source_word=words[3], target_word=words[10], priority=5),
        # Translation(source_word=words[4], target_word=words[11], priority=5),
        # Translation(source_word=words[5], target_word=words[12], priority=5),
        # Translation(source_word=words[6], target_word=words[13], priority=5),

        # Translation(source_word=words[10], target_word=words[3], priority=5),
        # Translation(source_word=words[11], target_word=words[4], priority=5),
        # Translation(source_word=words[12], target_word=words[5], priority=5),
        # Translation(source_word=words[13], target_word=words[5], priority=5),

    ])

    return words