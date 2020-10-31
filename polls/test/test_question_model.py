"""Add unittest for KU-polls."""
import datetime
from django.test import TestCase
from django.utils import timezone
from polls.models import Question


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