# Create your models here.
from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=100)
    isCity = models.BooleanField(default=False)
    population = models.IntegerField()
    kato = models.CharField(max_length=50)
    sdu_name = models.CharField(max_length=100)
    sdu_second_name = models.CharField(max_length=100)
    sdu_third_name = models.CharField(max_length=100)
    sdu_fourth_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"
    
    def __str__(self):
        return self.name
    
    
class Akim(models.Model):
    fio = models.CharField(max_length=200)
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING)
    date_start = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='akims_photos/', null=True, blank=True)
    
    class Meta:
        verbose_name = "Аким"
        verbose_name_plural = "Акимы"
    
    def __str__(self):
        return self.fio