from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from ads.permissions import IsOwnerOrStuffPermission
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.generic import UpdateView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from ads.serializers import AdListSerializer, AdCreateSerializer, AdUpdateSerializer, AdDestroySerializer
from ads.models import Ad



def root(request):
    return JsonResponse({"status": "ok"}, status=200)


class AdListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdListSerializer

    @extend_schema(
        description="Retrieve ad list",
        summary="Ad list"
    )

    def get(self, request, *args, **kwargs):
        ad_text = request.GET.get('text', None)
        if ad_text:
            self.queryset = self.queryset.filter(
                name__icontains=ad_text
            )

        cat_query = request.GET.get('cat', None)
        if cat_query:
            self.queryset = self.queryset.filter(
                category_id=cat_query
            )

        location_name = request.GET.get('location', None)
        if location_name:
            self.queryset = self.queryset.filter(
                author__locations__name__icontains=location_name
            )

        price_from = request.GET.get('price_from', None)
        price_to = request.GET.get('price_to', None)
        if price_from or price_to:
            self.queryset = self.queryset.filter(
                price__range=(price_from, price_to.rstrip('/'))
            )

        return super().get(request, *args, *kwargs)


class AdCreateView(CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer
    permission_classes = [IsAuthenticated]


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdListSerializer
    permission_classes = [IsAuthenticated]


class AdUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrStuffPermission]


@method_decorator(csrf_exempt, name='dispatch')
class AdImageUpdate(UpdateView):
    model = Ad
    fields = ["name", "author", "price", "description", "address", "is_published", "image", "category_id"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES["image"]
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None
        }, status=200)


class AdDeleteView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDestroySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrStuffPermission]