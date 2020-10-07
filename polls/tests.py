"""Add unittest for KU-polls."""
import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse


class QuestionModelTests(TestCase):
    """unittest for Question model."""

    def test_was_published_recently_with_future_question(self):
        """
        * copy comment from tutorial.

        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        * copy comment from tutorial.

        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        * copy comment from tutorial.

        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_future_question(self):
        """is_published() return False if current date is on or after question’s publication date."""
        time = timezone.now() + datetime.timedelta(days=30)
        question_tester = Question(pub_date=time)
        self.assertIs(question_tester.is_published(), False)

    def test_is_published_with_old_question(self):
        """is_published() return False if current date is on or after question’s publication date."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        question_tester = Question(pub_date=time)
        self.assertIs(question_tester.is_published(), True)

    def test_is_published_with_recent_question(self):
        """is_published() return False if current date is on or after question’s publication date."""
        time = timezone.now()
        question_tester = Question(pub_date=time)
        self.assertIs(question_tester.is_published(), True)

    def test_can_vote_with_recent_question(self):
        """can_vote() returns true if voting is currently allowed."""
        pubtime = timezone.now()
        endtime = timezone.now() + datetime.timedelta(days=30)
        question_tester = Question(pub_date=pubtime, end_date=endtime)
        self.assertIs(question_tester.can_vote(), True)

    def test_can_vote_with_expired_question(self):
        """can_vote() returns true if voting is currently allowed."""
        pubtime = timezone.now() - datetime.timedelta(days=1, seconds=1)
        endtime = timezone.now() - datetime.timedelta(hours=23,
                                                      minutes=59, seconds=59)
        question_tester = Question(pub_date=pubtime, end_date=endtime)
        self.assertIs(question_tester.can_vote(), False)


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


class QuestionIndexViewTests(TestCase):
    """unittest for redirect page."""

    def test_no_questions(self):
        """
        * copy comment from tutorial.

        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        * copy comment from tutorial.

        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_question(question_text="Past question.", days=- 30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        * copy comment from tutorial.

        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        * copy comment from tutorial.

        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(question_text="Past question.", days=- 30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        * copy comment from tutorial.

        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=- 30)
        create_question(question_text="Past question 2.", days=- 5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


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
        self.assertContains(response, past_question.question_text)
