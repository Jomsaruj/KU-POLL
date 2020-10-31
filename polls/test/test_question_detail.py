"""Add unittest for KU-polls."""
import datetime
from django.test import TestCase
from django.utils import timezone
from polls.models import Question
from django.urls import reverse


def create_question(question_text, days, end_date=30):
    """
    * copy comment from tutorial.

    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    publish_time = timezone.now() + datetime.timedelta(days=days)
    # add ending date
    ending_time = publish_time + datetime.timedelta(days=end_date)
    return Question.objects.create(question_text=question_text,
                                   pub_date=publish_time, end_date=ending_time)


class QuestionDetailViewTests(TestCase):
    """unittest for question that published in different time."""

    def test_future_question(self):
        """
        * copy comment from tutorial.

        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.',
                                          days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """
        * copy comment from tutorial.

        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.',
                                        days=- 5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
