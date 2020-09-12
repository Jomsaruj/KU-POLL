from django.http import HttpResponse

__author__      = "Saruj Sattayanurak"

def index(request):
    return HttpResponse("Hello you're at the polls index!")
