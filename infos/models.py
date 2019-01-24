from django.db import models

# Create your models here.

class tbValues(models.Model):

    rack_num=models.CharField(max_length=20)
    box_num=models.CharField(max_length=30)
    barcode_num=models.CharField(max_length=30)
    well_num=models.CharField(max_length=10)
    freezer_num=models.CharField(max_length=20)

    def __str__(self):
        return self.barcode_num
