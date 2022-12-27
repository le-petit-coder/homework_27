from functools import partial
from rest_framework import viewsets, status
from locations.models import Location
from rest_framework.views import Response
from locations.serializers import LocationSerializer
from django.shortcuts import get_object_or_404


class LocationViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Location.objects.all()
        serializer = LocationSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = LocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        queryset = Location.objects.all()
        location = get_object_or_404(queryset, pk=pk)
        serializer = LocationSerializer(location)
        return Response(serializer.data)

    def update(self, request, pk=None):
        queryset = Location.objects.all()
        user = get_object_or_404(queryset, pk=pk)

        serializer = LocationSerializer(user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, pk=None):
        queryset = Location.objects.all()
        location = get_object_or_404(queryset, pk=pk)
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)