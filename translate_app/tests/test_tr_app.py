import pytest

from translate_app.models import AnswerOptions, Question, Task
from translate_app.views import generate_task
from translations.db_adapter import translate, translations
from translations.models import Translation, Word

from .fixtures.fixture_data import database
from .fixtures.fixture_user import user, user_client

Lang = Word.Language


@pytest.mark.django_db
@pytest.mark.tr_app
def test_task_generate(database, user):
    num_of_q = 1
    word_lang = "EN"
    translation_lang = "RU"
    new_task = generate_task(user, num_of_q, word_lang, translation_lang)
    assert new_task.questions.count() == 1
    assert new_task.status == False
    assert new_task.assessment == None

    question = new_task.questions.get(id=1)
    assert question.task == new_task
    assert question.word.word == "onion"

    options = question.options
    assert options.question == question
    assert options.answer.word == "лук"
    assert options.bait_1.word not in translations(
        options.answer.word, translation_lang
    )
    assert options.bait_2.word not in translations(
        options.answer.word, translation_lang
    )
    assert options.bait_3.word not in translations(
        options.answer.word, translation_lang
    )
