from django.shortcuts import render
from django.views.generic import DetailView

from regions.models import Region
from regions.services import get_priority_indicators_values, get_region_scores_with_segments
from indicators.models import IndicatorSegment 

# Create your views here.
class RegionDetailView(DetailView):
    model = Region
    template_name = 'regions/region_detail.html'
    context_object_name = 'region'
    pk_url_kwarg = 'region_id'
    
    def get_queryset(self):
        return super().get_queryset().select_related('akim')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        segments = list(IndicatorSegment.objects.filter(is_active=True).order_by('order', 'id'))
        region_score = get_region_scores_with_segments(self.object.id, segments=segments)
        current_view = self.request.GET.get('currentView')

        allowed_tabs = {'priority', 'people', 'result', 'work'} | {segment.system_name for segment in segments}
        requested_tab = self.request.GET.get('tabname', 'priority')
        active_tab = requested_tab if requested_tab in allowed_tabs else 'priority'
        
        context['akim'] = self.object.akim
        context['region_score'] = region_score
        context['date_start_string'] = self.object.akim.date_start.strftime("В должности с %d.%m.%Y") if self.object.akim and self.object.akim.date_start else "Дата назначения неизвестна"
        context['active_tab'] = active_tab
        context['segments'] = segments
        context['current_view'] = current_view
        
        if active_tab == 'priority':
            context['priority_indicators'] = get_priority_indicators_values(self.object.id)
        return context

