from django.shortcuts import render
from django.views.generic import DetailView

from regions.models import Region, Akim
from rating.models import RegionScore

# Create your views here.
class RegionDetailView(DetailView):
    model = Region
    template_name = 'regions/region_detail.html'
    context_object_name = 'region'
    pk_url_kwarg = 'region_id'
    
    def get_queryset(self):
        return super().get_queryset().select_related('akim', 'region_score')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        allowed_tabs = {'priority', 'people', 'result', 'work'}
        requested_tab = self.request.GET.get('tabname', 'priority')
        active_tab = requested_tab if requested_tab in allowed_tabs else 'priority'
        
        context['akim'] = self.object.akim
        context['region_score'] = self.object.region_score
        context['date_start_string'] = self.object.akim.date_start.strftime("В должности с %d.%m.%Y") if self.object.akim and self.object.akim.date_start else "Дата назначения неизвестна"
        context['active_tab'] = active_tab
        return context
