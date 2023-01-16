import factory.django
from ads.models import Ad
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = "test_user"
    password = "test_password"


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad

    name = "test"
    price = 100

