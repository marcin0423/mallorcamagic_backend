from django.db import models


# Create your models here.
class GuideModel(models.Model):
    slug = models.CharField(max_length=256, primary_key=True)
    creator = models.CharField(max_length=64)
    thumbnail = models.TextField()
    category = models.CharField(max_length=64)
    timestamp = models.CharField(max_length=64)
    highlighted = models.BooleanField(default=False)

    title_en = models.TextField()
    title_es = models.TextField()
    title_de = models.TextField()

    short_desc_en = models.TextField()
    short_desc_es = models.TextField()
    short_desc_de = models.TextField()

    long_desc_en = models.TextField()
    long_desc_es = models.TextField()
    long_desc_de = models.TextField()

    def to_dtc(self, lang_id=0):
        objDict = {}
        objDict["slug"] = self.slug

        objDict['details'] = {}
        objDict['details']['creator'] = self.creator
        objDict['details']['title'] = [[self.title_en, self.title_es, self.title_de][lang_id]]
        objDict['details']['short_desc'] = [[self.short_desc_en, self.short_desc_es, self.short_desc_de][lang_id]]
        objDict['details']['long_desc'] = [[self.long_desc_en, self.long_desc_es, self.long_desc_de][lang_id]]

        objDict["thumbnail"] = [self.thumbnail]
        objDict['details']["category"] = self.category
        objDict["timestamp"] = self.timestamp
        return objDict
