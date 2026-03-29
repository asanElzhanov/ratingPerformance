from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from regions.services import get_regions_with_segment_scores
from regions.models import Region
from regions.services import get_priority_indicators_values, get_region_scores_with_segments, get_categories_by_segment
from indicators.models import IndicatorSegment
from indicators.constants import SegmentID

def RapPage(request):
    allowed_views = {'map', 'list', 'dashboard'}
    requested_view = request.GET.get('currentView')
    if requested_view not in allowed_views:
        requested_view = 'map'

    data = {
        'title': 'RAP',
        "currentView": requested_view
    }

    if requested_view == 'list':
        data["regions"] = get_regions_with_segment_scores()

    return render(request, 'main/RAP.html', data)

def mainPage(request):
    current_view = request.GET.get('currentView')
    rap_page_url = reverse('main:rapPage')
    if current_view:
        return redirect(f'{rap_page_url}?currentView={current_view}')
    return redirect(rap_page_url)

def RapRegionDetailPage(request, region_id):
    region = get_object_or_404(Region.objects.select_related('akim'), id=region_id)

    segments = list(IndicatorSegment.objects.filter(is_active=True).order_by('order', 'id'))
    region_score = get_region_scores_with_segments(region.id, segments=segments)
    current_view = request.GET.get('currentView') or 'list'

    allowed_tabs = {'priority'} | {segment.system_name for segment in segments}
    requested_tab = request.GET.get('tabname', 'priority')
    active_tab = requested_tab if requested_tab in allowed_tabs else 'priority'

    context = {
        'region': region,
        'akim': region.akim,
        'region_score': region_score,
        'date_start_string': (
            region.akim.date_start.strftime('В должности с %d.%m.%Y')
            if region.akim and region.akim.date_start
            else 'Дата назначения неизвестна'
        ),
        'active_tab': active_tab,
        'segments': segments,
        'current_view': current_view,
    }

    if active_tab == 'priority':
        context['priority_indicators'] = get_priority_indicators_values(region.id)
    else:
        current_segment = next((s for s in segments if s.system_name == active_tab), None)
        categories = get_categories_by_segment(current_segment.id) if current_segment else []
        if current_segment and current_segment.id == SegmentID.PEOPLE:
            for index in range(len(categories)):
                categories[index].name = categories[index].name.replace('(оценка населения)', '', -1)

        context['segment_categories'] = categories

    return render(request, 'main/RAP_region_detail.html', context)