from django.contrib import admin
from .models import Region, Akim

# Register your models here.
@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'isCity', 'population', 'kato', 'sdu_name', 'sdu_second_name', 'sdu_third_name', 'sdu_fourth_name', 'created_at', 'updated_at')
    search_fields = ('name', 'kato')
    list_filter = ('name',)
    
@admin.register(Akim)
class AkimAdmin(admin.ModelAdmin):
    list_display = ('fio', 'region', 'date_start', 'created_at', 'updated_at')
    search_fields = ('fio',)
    list_filter = ('fio',)
