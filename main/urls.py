from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.mainPage, name = 'mainPage'),
    path('RAP/', views.RapPage, name = 'rapPage')
]
