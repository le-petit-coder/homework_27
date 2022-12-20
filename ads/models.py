from django.db import models
from categories.models import Category


class Ad(models.Model):

    name = models.CharField(max_length=50)
    author_id = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=250)
    is_published = models.BooleanField()
    image = models.ImageField(upload_to='images/', null=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"






