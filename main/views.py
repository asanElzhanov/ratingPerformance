from django.shortcuts import render, redirect
from django.urls import reverse

from regions.services import get_regions_with_segment_scores

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