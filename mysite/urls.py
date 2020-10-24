"""Add path to url."""
from django.contrib import admin
from django.urls import include, path
from . import views

__author__ = "Saruj Sattayanurak"

urlpatterns = [
    path('', views.index, name="main_index_page"),
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
