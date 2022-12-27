import json

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.generics import ListAPIView
from ads.serializers import AdListSerializer
from ads.models import Ad
from users.models import User
from categories.models import Category


def root(request):
    return JsonResponse({"status": "ok"}, status=200)


class AdListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdListSerializer

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
        price_to = request.GET.get('price_to', None).rstrip('/')
        if price_from or price_to:
            self.queryset = self.queryset.filter(
                price__range=(price_from, price_to)
            )

        return super().get(request, *args, *kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ["name", "author", "price", "description", "address", "is_published", "image", "category"]

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)

        author_id = ad_data["author"]
        author = User.objects.get(pk=author_id)

        category_id = ad_data["category"]
        category = Category.objects.get(pk=category_id)

        ad = Ad.objects.create(
            name=ad_data["name"],
            author=author,
            price=ad_data["price"],
            description=ad_data["description"],
            address=ad_data["address"],
            is_published=ad_data["is_published"],
            image=ad_data["image"] if ad_data["image"] else None,
            category=category if category else None
        )

        return JsonResponse(
            {
                "id": ad.id,
                "name": ad.name,
                "author": ad.author.username,
                "price": ad.price,
                "description": ad.description,
                "address": ad.address,
                "is_published": ad.is_published,
                "image": ad.image.url if ad_data["image"] else None,
                "category": ad.category.name if ad.category else None
            }, status=200)


class AdDetailView(DetailView):
    model = Ad

    def get(self, *args, **kwargs):
        ad = self.get_object()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author.username,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published,
            "image": ad.image.url if ad.image else None,
            "category": ad.category.name if ad.category else None
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ["name", "author", "price", "description", "address", "is_published", "image", "category"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)

        author_id = ad_data["author"]
        author = User.objects.get(pk=author_id)

        category_id = ad_data["category"]
        category = Category.objects.get(pk=category_id)

        self.object.name=ad_data["name"]
        self.object.author=author
        self.object.price=ad_data["price"]
        self.object.description=ad_data["description"]
        self.object.address=ad_data["address"]
        self.object.is_published=ad_data["is_published"]
        self.object.image=ad_data["image"]
        self.object.category=category

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author.username,
            "price": self.object.price,
            "description": self.object.description,
            "address": self.object.address,
            "is_published": self.object.is_published,
            "image": self.object.image if self.object.image else None,
            "category": self.object.category.name
            })


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


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"
    fields = ["name", "author", "price", "description", "address", "is_published", "image", "category"]

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)