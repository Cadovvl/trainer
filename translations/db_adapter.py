from translations.models import Translation


def translate(word):
    tr = Translation.objects.select_related('source_word', 'target_word')\
        .filter(source_word__word=word)\
        .order_by('-priority')[:1]
    if len(tr) <= 0:
        return None
    return tr[0].target_word.word


def translations(word):
    tr = Translation.objects.select_related('source_word', 'target_word')\
        .filter(source_word__word=word)\
        .order_by('-priority')
    return [i.target_word.word for i in tr]

