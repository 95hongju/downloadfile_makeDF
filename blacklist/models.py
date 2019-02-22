import datetime
from django.db import models
from django.utils import timezone


# Create your models here.

class Version(models.Model):
    version_name = models.CharField(max_length=30)
    def __str__(self):
        return self.version_name

    class Meta:
        verbose_name_plural = "LowQualityMarker_Versions"

class Blacks(models.Model):
    ver = models.ForeignKey(Version, on_delete = models.CASCADE)
    chr = models.CharField(max_length = 20)
    pos = models.CharField(max_length = 20)
    rsid = models.CharField(max_length = 50)
    reason = models.CharField(max_length = 30)
    who = models.CharField(max_length = 30)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.chr + '/' +self.pos + '/' + self.rsid + '/' +self.reason+ '/' +self.who

    class Meta:
        verbose_name_plural = "LowQualityMarker_Markers"
