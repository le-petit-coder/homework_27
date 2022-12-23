from django.db import models
from categories.models import Category
from users.models import User


class Ad(models.Model):

    name = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=250)
    is_published = models.BooleanField()
    image = models.ImageField(upload_to='images/', null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"






