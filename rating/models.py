from django.db import models

# Create your models here.
    
class RegionScore(models.Model):
    id = models.AutoField(primary_key=True)
    region = models.ForeignKey('regions.Region', on_delete=models.CASCADE, related_name='regions_scores')
    score_type = models.ForeignKey('RegionScoreType', on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.IntegerField(null=True, blank=True)  # For linking to specific category/scope if needed
    value = models.FloatField(default=0, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Оценка по показателю"
        verbose_name_plural = "Оценки по показателям"
        unique_together = ('region', 'score_type', 'object_id')
        db_table = 'region_scores'
        
class RegionScoreType(models.Model):
    id = models.IntegerField(primary_key=True)
    label = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "Тип оценки"
        verbose_name_plural = "Типы оценок"
        db_table = 'region_score_types'
    