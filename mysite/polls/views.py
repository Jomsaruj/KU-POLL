from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import Http404

from .models import Question

__author__      = "Saruj Sattayanurak"

def index(request):
    lastest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'lastest_question_list': lastest_question_list,}
    """
    
    This is the direct way, but we used shortcut way.
    
    template = loader.get_template('polls/index.html')
    return HttpResponse(template.render(context, request))
    
    """
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    """
    This is the direct way
    
    try:
        question = Question.objects.get(pk = question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})
    
    """
    question = Question.objects.get(pk = question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    text = "You're  looking at the result of question %s."
    return HttpResponse(text %question_id)
    
def vote(request, question_id):
    return HttpResponse("You're voting on question %s" %question_id)

