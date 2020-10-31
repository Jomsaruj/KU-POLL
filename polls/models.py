"""Add attribute and method for each objects."""
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
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

    def was_published_recently(self):
        """:return True if question is recently published."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """:return True if question is published."""
        now = timezone.now()
        return now >= self.pub_date

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

    @ property
    def votes(self):
        """:return sum of all vote in the particular question"""
        return self.vote_set.all().count()

    def __str__(self):
        """Attribute choice_text."""
        return self.choice_text


class Vote(models.Model):
    """Attributes for Vote objects."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)



