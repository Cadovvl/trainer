import pytest

from translate_app.models import AnswerOptions, Question, Task
from translations.db_adapter import translate, translations
from translations.models import Translation, Word

from .fixtures.fixture_data import database, task
from .fixtures.fixture_user import user, user_client

Lang = Word.Language


@pytest.mark.django_db
@pytest.mark.tr_app
def test_task_generate(database, user, task):
    assert task.questions.count() == 1
    assert task.status == False
    assert task.assessment == None

    question = task.questions.get(id=1)
    assert question.task == task
    assert question.word.word == "onion"

    options = question.options
    assert options.question == question
    assert options.answer.word == "лук"
    assert options.bait_1.word not in translations(
        options.answer.word, "RU"
    )
    assert options.bait_2.word not in translations(
        options.answer.word, "RU"
    )
    assert options.bait_3.word not in translations(
        options.answer.word, "RU"
    )


@pytest.mark.django_db(transaction=True)
@pytest.mark.skip
def test_task_answer(database, user, user_client, task):
    url = reverse('translate_task', args=[task.id])
    response = user_client.post(
        url,
        {"answer": "onion"},
        follow=True,
    )