"""provide a proper name for the admin."""
from django.apps import AppConfig


class PollsConfig(AppConfig):
    """set variable name as 'polls'."""

    name = 'polls'
