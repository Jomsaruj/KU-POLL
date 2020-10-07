"""Add attribute and method for each objects."""
from django.db import models
from django.utils import timezone
import datetime

__author__ = "Saruj Sattayanurak"


class Question(models.Model):
    """Attribute and method for Question objects."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("Date published")
    end_date = models.DateTimeField("Date expired", default=None)

    def __str__(self):
        """Attribute question_text."""
        return self.question_text

    """
    Return True only if pub_date is in the past.
    """

    def was_published_recently(self):
        """:return True if question is recently published."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    """
    Returns True if current date is on or after question’s publication date
    """

    def is_published(self):
        """:return True if question is published."""
        now = timezone.now()
        return now >= self.pub_date

    """
    Returns True if voting is currently allowed for this question
    """

    def can_vote(self):
        """:return True if question is published and with in end date."""
        now = timezone.now()
        return self.is_published() and now <= self.end_date

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    """Attribute and method for Choice objects."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Attribute choice_text."""
        return self.choice_text
