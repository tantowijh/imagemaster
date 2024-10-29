# urls.py
from django.urls import path
from . import views

app_name = 'configuration'
urlpatterns = [
    path('', views.configure, name='configure'),
]