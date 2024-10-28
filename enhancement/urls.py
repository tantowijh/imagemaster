from django.urls import path
from . import views

app_name = 'enhancement'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('result/', views.ResultView.as_view(), name='result'),
]