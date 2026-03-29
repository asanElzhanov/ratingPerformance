from django.shortcuts import render
from django.views.generic import DetailView

from regions.models import Region
from regions.services import get_priority_indicators_values, get_region_scores_with_segments, get_categories_by_segment
from indicators.models import IndicatorSegment 
from indicators.constants import SegmentID

# Create your views here.

