from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from ads.permissions import IsOwnerPermission
from ads.models import Selection
from ads.serializers import SelectionSerializer, SelectionListSerializer, SelectionDetailSerializer


class SelectionViewSet(ModelViewSet):
    queryset = Selection.objects.all()
    # default_serializer = SelectionSerializer
    serializer_class = SelectionSerializer

    default_permission = [AllowAny()]
    permissions = {
        "create": [IsAuthenticated()],
        "retrieve": [IsAuthenticated()],
        "update": [IsAuthenticated(), IsOwnerPermission()],
        "partial_update": [IsAuthenticated(), IsOwnerPermission()],
        "delete": [IsAuthenticated(), IsOwnerPermission()]
    }