from django.contrib.auth.models import AbstractUser
from django.db import models
from locations.models import Location
from datetime import date
from django.core.exceptions import ValidationError


def check_age_more_nine(value: date):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 9:
        raise ValidationError(f"User is younger than 9.")


def check_email_not_rambler(value):
    email_status = value.endswith("@rambler.ru")
    if email_status:
        raise ValidationError(f"Domain @rambler.ru is not allowed, please choose another domain.")


class User(AbstractUser):
    ROLE = [
        ("member", "пользователь"),
        ("admin", "администратор"),
        ("moderator", "модератор")
    ]

    role = models.CharField(max_length=9, choices=ROLE, default="member")
    locations = models.ManyToManyField(Location)
    age = models.PositiveSmallIntegerField()
    birth_date = models.DateField(null=True, validators=[check_age_more_nine])
    email = models.CharField(max_length=50, null=True, unique=True, validators=[check_email_not_rambler])

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username



