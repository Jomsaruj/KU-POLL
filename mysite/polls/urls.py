from django.urls import path
from. import views

__author__      = "Saruj Sattayanurak"

urlpatterns = [path('', views.index, name = 'index'),]

