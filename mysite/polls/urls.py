from django.urls import path
from. import views

__author__      = "Saruj Sattayanurak"

app_name = "polls"
urlpatterns = [
    path('', views.IndexView.as_view(), name = 'index'),
    #"name" is represent {% url %} template tag
    path('<int:pk>/', views.DetailView.as_view(),name = 'detail'),
    path('<int:pk>/results/',views.ResultsView.as_view(),name = 'results'),
    path('<int:question_id>/vote/',views.vote,name = 'vote'),
    path('<int:question_id>/vote/',views.vote,name = 'vote'),
]

