from django.db import models
from django.utils import timezone

# Create your models here.
class downloadFileList(models.Model):
    print(timezone.now())
    file_name = models.CharField(max_length=150)
    down_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name+"------" + str(self.down_date)[:11]
