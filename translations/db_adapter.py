from typing import Optional

from django.db.models import Q

from translations.models import Translation, Word


def translate(word: str, lang: Word.Language) -> Optional[str]:
    tr = Translation.objects.select_related('source_word', 'target_word')\
        .filter(Q(source_word__word=word) & Q(target_word__lang=lang))\
        .order_by('-priority').first()

    return None if tr is None else tr.target_word.word


def translations(word: str, lang: Word.Language) -> [str]:
    tr = Translation.objects.select_related('source_word', 'target_word')\
        .filter(Q(source_word__word=word) & Q(target_word__lang=lang))\
        .order_by('-priority')
    return [i.target_word.word for i in tr]
