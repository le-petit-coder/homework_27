from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from locations.models import Location


# class UserManager(BaseUserManager):
#     def create_user(self, username, password):
#         user = self.model(
#             username=username
#         )
#         user.set_password(password)
#         user.save()
#         return user
#
#     def create_superuser(self, username, password):
#         user = self.create_user(username, password)
#
#         user.is_staff = True
#         user.is_superuser = True
#         user.save()
#         return user


class User(AbstractUser):
    ROLE = [
        ("member", "пользователь"),
        ("admin", "администратор"),
        ("moderator", "модератор")
    ]

    role = models.CharField(max_length=9, choices=ROLE, default="member")
    locations = models.ManyToManyField(Location)
    age = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username



