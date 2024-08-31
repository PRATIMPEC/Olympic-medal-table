from django.db import models

# Create your models here.
class Data(models.Model):
    country = models.CharField(max_length=50)
    isMale = models.BooleanField(null = True)
    isFemale = models.BooleanField(null=True)
    year = models.IntegerField(default=0)
    sports = models.TextField(null=True)
    season = models.TextField(null=True)
    medal = models.TextField(null=True)

    def __str__(self) -> str:
        return self.country

