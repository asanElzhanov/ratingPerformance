from django.db import models

class IndicatorSegment(models.Model):
    id = models.IntegerField(primary_key=True)
    changed = models.DateTimeField(null=True, blank=True, auto_now=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(null=True, blank=True)
    label = models.CharField(max_length=100)
    system_name = models.CharField(max_length=255, null=True, blank=True)
    coefficient = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    
    class Meta:
        db_table = 'indicator_segments'
        verbose_name = 'Сектор показателей'
        verbose_name_plural = 'Сектора показателей'

    def __str__(self):
        return self.label

class IndicatorCategory(models.Model):
    id = models.AutoField(primary_key=True)
    segment = models.ForeignKey(IndicatorSegment, on_delete=models.SET_NULL, related_name='categories', null=True, blank=True)
    changed = models.DateTimeField(null=True, blank=True, auto_now=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(null=True, blank=True)
    label = models.CharField(max_length=150)
    system_name = models.CharField(max_length=255, null=True, blank=True)
    coefficient = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    
    class Meta:
        db_table = 'indicator_categories'
        verbose_name = 'Категория показателей'
        verbose_name_plural = 'Категории показателей'

    def __str__(self):
        return self.label

class IndicatorScope(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(IndicatorCategory, on_delete=models.SET_NULL, related_name='scopes', null=True, blank=True)
    changed = models.DateTimeField(null=True, blank=True, auto_now=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(null=True, blank=True)
    label = models.CharField(max_length=100)
    system_name = models.CharField(max_length=255, null=True, blank=True)
    coefficient = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)

    class Meta:
        db_table = 'indicator_scopes'
        verbose_name = 'Сфера показателей'
        verbose_name_plural = 'Сферы показателей'

    def __str__(self):
        return self.label

class Indicator(models.Model):
    id = models.AutoField(primary_key=True)
    scope = models.ForeignKey(IndicatorScope, on_delete=models.SET_NULL, null=True, blank=True)
    changed = models.DateTimeField(null=True, blank=True, auto_now=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(null=True, blank=True)
    label = models.CharField(max_length=255)
    source = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    small_description = models.TextField(null=True, blank=True)
    confidence_level = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    influence_level = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    high_score = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    measurement_unit = models.CharField(max_length=50, null=True, blank=True)
    root_system_name = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        db_table = 'indicators'
        verbose_name = 'Показатель'
        verbose_name_plural = 'Показатели'

    def __str__(self):
        return self.label

class IndicatorPriority(models.Model):
    id = models.AutoField(primary_key=True)
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE, related_name='priority_entries')
    priority_number = models.PositiveIntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'indicator_priorities'
        verbose_name = 'Приоритет показателя'
        verbose_name_plural = 'Приоритеты показателей'