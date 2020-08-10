import pytest

from translations.db_adapter import translate, translations
from translations.models import Word, Translation


@pytest.fixture
def database():
    Word.objects.bulk_create([
        Word(word='лук', lang=Word.Language.RU),
        Word(word='onion', lang=Word.Language.EN),
        Word(word='bow', lang=Word.Language.EN),
        Word(word='поклон', lang=Word.Language.RU),
        Word(word='нос', lang=Word.Language.RU),
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
    assert translate('onion') == 'лук'
    assert translate('bow') == 'лук'
    assert translate('лук') == 'onion'
    assert translate('поклон') is None
    assert translate('нос') is None
    assert translate('несуществую') is None


@pytest.mark.django_db
def test_translations(database):
    assert translations('onion') == ['лук']
    assert translations('bow') == ['лук', 'поклон', 'нос']
    assert translations('лук') == ['onion', 'bow']
    assert translations('поклон') == []
    assert translations('нос') == []
    assert translations('несуществую') == []



