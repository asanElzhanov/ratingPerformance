from django.contrib import admin
from .models import RegionScore

@admin.register(RegionScore)
class RegionScoreAdmin(admin.ModelAdmin):
	list_display = ('region', 'overall_score', 'result_score', 'work_score', 'people_score', 'updated_at')
	search_fields = ('region__name',)
	list_filter = ('updated_at',)
