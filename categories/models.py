from django.db import models
from django.core.validators import MinLengthValidator


class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(null=True, max_length=10, unique=True, validators=[MinLengthValidator(5)])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
