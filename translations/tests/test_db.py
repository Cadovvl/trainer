import pytest
from django.db import IntegrityError, transaction

from translations.db_adapter import translate, translations
from translations.models import Translation, Word

from django.db.models import Q

Lang = Word.Language

@pytest.fixture
def database():
    Word.objects.bulk_create([
        Word(word='лук', lang=Lang.RU),
        Word(word='onion', lang=Lang.EN),
        Word(word='bow', lang=Lang.EN),
        Word(word='поклон', lang=Lang.RU),
        Word(word='нос', lang=Lang.RU),
    ])

    words = Word.objects.all()

    print([i.__dict__ for i in words])
    translations = Translation.objects.bulk_create([
        Translation(source_word=words[0], target_word=words[1], priority=10),
        Translation(source_word=words[0], target_word=words[2], priority=5),
        Translation(source_word=words[1], target_word=words[0], priority=5),
        Translation(source_word=words[2], target_word=words[0], priority=15),
        Translation(source_word=words[2], target_word=words[3], priority=10),
        Translation(source_word=words[2], target_word=words[4], priority=5)
    ])

    return words


@pytest.mark.django_db
def test_translation(database):
    assert translate('onion', Lang.RU) == 'лук'
    assert translate('bow', Lang.RU) == 'лук'
    assert translate('bow', Lang.EN) is None
    assert translate('bow', Lang.NO) is None
    assert translate('лук', Lang.EN) == 'onion'
    assert translate('лук', Lang.RU) is None
    assert translate('лук', Lang.NO) is None
    assert translate('поклон', Lang.EN) is None
    assert translate('нос', Lang.EN) is None
    assert translate('несуществую', Lang.EN) is None


@pytest.mark.django_db
def test_translations(database):
    assert translations('onion', Lang.RU) == ['лук']
    assert translations('bow', Lang.RU) == ['лук', 'поклон', 'нос']
    assert translations('bow', Lang.EN) == []
    assert translations('bow', Lang.NO) == []
    assert translations('лук', Lang.EN) == ['onion', 'bow']
    assert translations('лук', Lang.RU) == []
    assert translations('лук', Lang.NO) == []
    assert translations('поклон', Lang.EN) == []
    assert translations('нос', Lang.EN) == []
    assert translations('несуществую', Lang.EN) == []


@pytest.mark.django_db
def test_unique_word_constraint(database):
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            Word.objects.create(word='лук', lang=Lang.RU)
    assert 1 == len(Word.objects.filter(Q(word='лук') & Q(lang=Lang.RU)).all())

    with pytest.raises(IntegrityError):
        with transaction.atomic():
            w1 = Word.objects.filter(Q(word='onion') & Q(lang=Lang.EN)).first()
            w2 = Word.objects.filter(Q(word='лук') & Q(lang=Lang.RU)).first()
            Translation.objects.create(source_word=w1, target_word=w2, priority=100500)

    assert translations('onion', Lang.RU) == ['лук']


