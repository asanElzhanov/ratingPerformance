from dataclasses import asdict

from django.http import JsonResponse
from indicators.services import get_category_with_scopes
from django.shortcuts import render

# Create your views here.
def getCategoryWithScopes(request, category_id=None):
    request_category_id = category_id or request.GET.get('category_id')
    request_region_id = request.GET.get('region_id')

    if not request_category_id or not request_region_id:
        return JsonResponse({'category': None})

    try:
        category_id = int(request_category_id)
        region_id = int(request_region_id)
    except (TypeError, ValueError):
        return JsonResponse({'category': None}, status=400)

    category_vm = get_category_with_scopes(category_id=category_id, region_id=region_id)
    if category_vm is None:
        return JsonResponse({'category': None}, status=404)

    category_data = asdict(category_vm)
    return JsonResponse({'category': category_data})

def getCategoryWithScopesHTML(request, category_id=None):
    request_category_id = category_id or request.GET.get('category_id')
    request_region_id = request.GET.get('region_id')
    if not request_category_id:
        return render(request, 'invalid_request.html', {'message': 'category_id is required'})
    
    if not request_region_id:
        return render(request, 'invalid_request.html', {'message': 'region_id is required'})
    
    try:
        parsed_category_id = int(request_category_id)
        parsed_region_id = int(request_region_id)
    except (TypeError, ValueError):
        return render(request, 'invalid_request.html', {'message': 'category_id and region_id must be integers'})

    category_vm = get_category_with_scopes(category_id=parsed_category_id, region_id=parsed_region_id)
    if category_vm is None:
        return render(request, 'invalid_request.html', {'message': 'category not found'})
    
    category_date = asdict(category_vm)
    return render(request, 
                  'scope/scope_list.html', 
                  {'category': category_date})