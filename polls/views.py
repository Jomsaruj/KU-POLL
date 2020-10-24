"""Redirection for page and link to html files."""
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages

from .models import Question, Choice

__author__ = "Saruj Sattayanurak"


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


def vote(request, question_id):
    """Redirect page to voting page."""
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])

    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html',
                      {'question': question, 'error_message': "You didn't select any choice.", })

    else:
        selected_choice.votes += 1
        selected_choice.save()
        # copy comment from tutorial
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        messages.success(request, "Your choice successfully recorded. Thank you.")
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


# redirect visitor back to polls index page and show error message,
# if they accidentally navigates to the polls detail page for a poll
# where voting is not allowed.
def vote_for_poll(request, question_id):
    """Redirect to voting page if function can_vote return True or show warning message if False."""
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        messages.error(request, " Warning: poll name " + question.question_text + " is already expired")
        return redirect('polls:index')
    elif question.can_vote():
        return render(request, 'polls/detail.html', {'question': question})




