from django.urls import path
from . import views

app_name = 'indicators'

urlpatterns = [
    path('category/<int:category_id>', views.getCategoryWithScopes, name='category_with_scopes'),
]