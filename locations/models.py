from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100)
    lat = models.CharField(max_length=9)
    lng = models.CharField(max_length=9)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Местоположение"
        verbose_name_plural = "Местоположения"
