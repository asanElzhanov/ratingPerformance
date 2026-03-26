from django.db import models

# Create your models here.
class RegionScore(models.Model):
    region = models.OneToOneField('regions.Region', on_delete=models.CASCADE, related_name='region_score')
    overall_score = models.FloatField()
    result_score = models.FloatField()
    work_score = models.FloatField()
    people_score = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Оценка региона"
        verbose_name_plural = "Оценки регионов"
    
    def __str__(self):
        return f"{self.region.name} - {self.overall_score}"