from rest_framework import serializers
from ads.models import Ad, Selection
from locations.models import Location
from users.models import User


class AdListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="first_name"

    )

    class Meta:
        model = Ad
        fields = ["id", "name", "author", "price"]


class AdDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="first_name"

    )

    class Meta:
        model = Ad
        fields = ["id", "name", "author", "price"]


class AdCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    locations = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field="name"
    )

    class Meta:
        model = Ad
        fields = ["id", "name", "author", "price", "locations"]

    def is_valid(self, *, raise_exception=False):
        self._locations = self.initial_data.pop("locations", [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        ad = Ad.objects.create(**validated_data)

        for location in self._locations:
            locations_obj, _ = Location.objects.get_or_create(name=location)
            ad.skills.add(locations_obj)
        ad.save()
        return ad


class AdUpdateSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field="name"
    )
    #user = serializers.IntegerField(read_only=True)
    created = serializers.DateField(read_only=True)

    class Meta:
        model = Ad
        fields = ["id", "name", "author", "price", "locations", "created"]

    def is_valid(self, *, raise_exception=False):
        self._locations = self.initial_data.pop("locations", [])
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        ad = super().save()

        for location in self._locations:
            locations_obj, _ = Location.objects.get_or_create(name=location)
            ad.locations.add(locations_obj)
        ad.save()
        return ad


class AdDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ["id"]


class SelectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ["id", "name"]


class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'


class SelectionDetailSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    items = AdListSerializer(many=True)

    class Meta:
        model = Selection
        fields = '__all__'