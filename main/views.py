from django.shortcuts import render, redirect

from regions.models import Region

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
        data["regions"] = Region.objects.all().prefetch_related('region_score')

    return render(request, 'main/RAP.html', data)

def mainPage(request):
    return redirect('main:rapPage')