from django.urls import path
from . import views


app_name = 'restoration'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('mask/', views.MaskView.as_view(), name='mask'),
    path('result/', views.ResultView.as_view(), name='result'),
]