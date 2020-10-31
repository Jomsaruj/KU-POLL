"""Redirection for page and link to html files."""

from django.contrib.auth import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import logging

from .models import Question, Choice, Vote

__author__ = "Saruj Sattayanurak"


def formatter():
    """Configure logging using basicConfig for simple configuration.

    You should call this before creating logging objects.

    Some attributes you can set are:
        filename = (creates a FileHandler and uses it)
        stream = (name of a StreamHandler to use), cannot use with filename=
        filemode = 'a' (append mode), 'w' (truncate & open for writing)
        level = set the root logger level

    """
    # custom format of log messages
    FORMAT = '%(asctime)s %(name)s %(levelname)s: %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    return logging.getLogger("polls")


def get_client_ip(request):
    """ Getting the visitor’s actual IP address """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(user_logged_in)
def check_login(request, user, **kwargs):
    """logging for login successfully"""
    logger = formatter()
    logger.info("IP address: %s, Username: %s Login", get_client_ip(request), user)


@receiver(user_login_failed)
def check_login_fail(request, **kwargs):
    """logging for login unsuccessfully"""
    logger = formatter()
    logger.warning("IP address: %s:  Login unsuccessful", get_client_ip(request))


@receiver(user_logged_out)
def check_logout(request, user, **kwargs):
    """logging for logout successful"""
    logger = formatter()
    logger.info("IP address: %s, Username: %s Logout", get_client_ip(request), user)


class IndexView(generic.ListView):
    """redirect page to index page."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:]


class ResultsView(generic.DetailView):
    """Redirect page to voting Results page."""

    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    """Redirect page to voting page."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])

    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html',
                      {'question': question, 'error_message': "You didn't select any choice.", })

    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        Vote.objects.update_or_create(question=question, user=request.user, defaults={"choice": selected_choice})
        messages.success(request, "Your choice successfully recorded. Thank you.")
        logger = formatter()
        logger.info("IP address: %s, Username: %s Vote to question: %s", get_client_ip(request), request.user, question_id)
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


# redirect visitor back to polls index page and show error message,
# if they accidentally navigates to the polls detail page for a poll
# where voting is not allowed.
@login_required
def vote_for_poll(request, question_id):
    """Redirect to voting page if function can_vote return True or show warning message if False."""
    question = get_object_or_404(Question, pk=question_id)
    current_choice = Vote.objects.filter(question=question, user=request.user).first()
    if not question.can_vote():
        messages.error(request, " Warning: poll name " + question.question_text + " is already expired")
        return redirect('polls:index')
    elif question.can_vote():
        return render(request, 'polls/detail.html', {'question': question, 'current_choice': current_choice})
