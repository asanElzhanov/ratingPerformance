from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'regions'

urlpatterns = [
    path('<int:region_id>', views.RegionDetailView.as_view(), name='region_detail'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)