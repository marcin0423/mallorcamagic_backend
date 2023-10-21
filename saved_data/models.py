from django.db import models
from accounts.models import CustomUser


# Create your models here.
class SavedGuide(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    slug = models.CharField(max_length=256, primary_key=True)
    creator = models.CharField(max_length=64)
    thumbnail = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    title_en = models.TextField()
    title_es = models.TextField()
    title_de = models.TextField()

    short_desc_en = models.TextField()
    short_desc_es = models.TextField()
    short_desc_de = models.TextField()

    long_desc_en = models.TextField()
    long_desc_es = models.TextField()
    long_desc_de = models.TextField()

    def __str__(self):
        return self.title_en


class SavedProperty(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    slug = models.CharField(max_length=256, primary_key=True)
    partner = models.CharField(max_length=64)
    thumbnail = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    title = models.TextField()
    description = models.TextField()

    price_unit = models.CharField(max_length=4)
    price_amount = models.CharField(max_length=16)

    bathrooms = models.IntegerField(default=0)
    bedrooms = models.IntegerField(default=0)
    area = models.CharField(max_length=16)

    def __str__(self):
        return self.title
