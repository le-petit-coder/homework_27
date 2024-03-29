from rest_framework import serializers
from locations.models import Location
from users.models import User
from django.contrib.auth.hashers import make_password
from datetime import date


# class NotUnderNineAge:
#     def __init__(self, birthday):
#         self.birthday = birthday
#
#     def __call__(self, birthday):
#         today = date.today()
#         age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
#         if age < 9:
#             raise serializers.ValidationError(f"User is younger than 9.")


class UserSerializer(serializers.ModelSerializer):
    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    locations = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field="name"
    )
    # birth_date = serializers.DateField(validators=[NotUnderNineAge])

    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        self._locations = self.initial_data.pop("locations", [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        pas = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(pas)
        user.save()

        for location in self._locations:
            location_obj, _ = Location.objects.get_or_create(name=location)
            user.locations.add(location_obj)
        user.save()
        return user
