from django.contrib import admin
from .models import Indicator, IndicatorScope, IndicatorCategory, IndicatorSegment, IndicatorPriority


@admin.register(IndicatorSegment)
class IndicatorSegmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'label', 'system_name', 'order', 'is_active', 'changed')
    list_filter = ('is_active', 'changed')
    search_fields = ('label', 'system_name')
    ordering = ('order',)
    readonly_fields = ('changed',)
    list_editable = ('label', 'system_name', 'order', 'is_active')
    fieldsets = (
        ('Основная информация', {
            'fields': ('label', 'system_name')
        }),
        ('Параметры', {
            'fields': ('order', 'coefficient', 'is_active')
        }),
        ('Служебная информация', {
            'fields': ('changed',),
            'classes': ('collapse',)
        }),
    )


@admin.register(IndicatorCategory)
class IndicatorCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'label', 'segment', 'system_name', 'order', 'coefficient', 'is_active')
    list_filter = ('is_active', 'segment', 'changed')
    search_fields = ('label', 'system_name')
    ordering = ('segment', 'order')
    readonly_fields = ('changed',)
    list_editable = ('label', 'segment', 'system_name', 'order', 'is_active')
    fieldsets = (
        ('Основная информация', {
            'fields': ('label', 'segment', 'system_name')
        }),
        ('Параметры', {
            'fields': ('order', 'coefficient', 'is_active')
        }),
        ('Служебная информация', {
            'fields': ('changed',),
            'classes': ('collapse',)
        }),
    )


@admin.register(IndicatorScope)
class IndicatorScopeAdmin(admin.ModelAdmin):
    list_display = ('id', 'label', 'category', 'system_name', 'order', 'is_active')
    list_filter = ('is_active', 'category', 'changed')
    search_fields = ('label', 'system_name')
    ordering = ('category', 'order')
    readonly_fields = ('changed',)
    list_editable = ('label', 'category', 'system_name', 'order', 'is_active')
    fieldsets = (
        ('Основная информация', {
            'fields': ('label', 'category', 'system_name')
        }),
        ('Параметры', {
            'fields': ('order', 'coefficient', 'is_active')
        }),
        ('Служебная информация', {
            'fields': ('changed',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'label', 'scope', 'high_score', 'measurement_unit', 'is_active')
    list_filter = ('is_active', 'scope', 'changed', 'measurement_unit')
    search_fields = ('label', 'description', 'small_description', 'root_system_name')
    ordering = ('scope', 'order')
    readonly_fields = ('changed',)
    list_editable = ('label', 'scope', 'high_score', 'measurement_unit', 'is_active')
    fieldsets = (
        ('Основная информация', {
            'fields': ('label', 'scope', 'source', 'root_system_name')
        }),
        ('Описание', {
            'fields': ('description', 'small_description')
        }),
        ('Показатели', {
            'fields': ('high_score', 'confidence_level', 'influence_level', 'measurement_unit')
        }),
        ('Параметры', {
            'fields': ('order', 'is_active')
        }),
        ('Служебная информация', {
            'fields': ('changed',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('changed',)


@admin.register(IndicatorPriority)
class IndicatorPriorityAdmin(admin.ModelAdmin):
    list_display = ('id', 'indicator', 'priority_number')
    list_filter = ('indicator', 'priority_number')
    search_fields = ('indicator__label',)
    ordering = ('priority_number',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('indicator', 'priority_number')
        }),
    )