from django.contrib import admin
from django.urls import include, path

__author__      = "Saruj Sattayanurak"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
]
