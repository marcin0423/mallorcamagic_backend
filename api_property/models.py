from django.db import models


class PropertyModel(models.Model):
    slug = models.CharField(max_length=256, primary_key=True)
    slug_es = models.CharField(max_length=256)
    slug_de = models.CharField(max_length=256)
    location = models.CharField(max_length=256)
    type = models.CharField(max_length=64)
    thumbnail = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    title = models.TextField()
    title_es = models.TextField()
    title_de = models.TextField()

    description = models.TextField()
    description_es = models.TextField()
    description_de = models.TextField()

    price_unit = models.CharField(max_length=4)
    price_amount = models.CharField(max_length=16)

    bathrooms = models.CharField(max_length=8)
    bedrooms = models.CharField(max_length=8)
    area = models.CharField(max_length=16)

    def __str__(self):
        return self.slug

    def to_dict(self, lang_id=0):
        data = {}
        if lang_id == 0:
            data['slug'] = self.slug
        elif lang_id == 1:
            data['slug'] = self.slug_es
        else:
            data['slug'] = self.slug_de

        if lang_id == 0:
            data['title'] = self.title
        elif lang_id == 1:
            data['title'] = self.title_es
        else:
            data['title'] = self.title_de

        data['thumbnail'] = self.thumbnail
        data['price'] = self.price_unit + self.price_amount

        data['bathrooms'] = self.bathrooms
        data['bedrooms'] = self.bedrooms
        data['area'] = self.area
        return data
