from django.db import models
from django.utils.text import slugify

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
