"""Add unittest for KU-polls."""
import datetime

from django.contrib.auth.models import User
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


class AuthenticationTest(TestCase):
    """unittest for authentication"""
    def setUp(self) -> None:
        self.question = create_question(question_text="Past question.", days=- 30)
        user = User.objects.create_user(username="saruj", password="saruj_isp")
        user.save()

    def test_unauthenticated_result(self):
        """ view result page without login """
        url = reverse('polls:results', args=(self.question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_vote(self):
        """ vote without login"""
        url = reverse('polls:vote', args=(self.question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_authenticated_vote(self):
        """vote after login"""
        self.client.login(username="saruj", password="saruj_isp")
        url = reverse('polls:vote', args=(self.question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_authenticated_result(self):
        """view result page after login"""
        self.client.login(username="saruj", password="saruj_isp")
        url = reverse('polls:results', args=(self.question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

