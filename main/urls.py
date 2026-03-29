from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.mainPage, name = 'mainPage'),
    path('RAP/', views.RapPage, name = 'rapPage'),
    path('RAP/regions/<int:region_id>/', views.RapRegionDetailPage, name='rapRegionDetailPage'),
]
