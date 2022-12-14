import json

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView
from ads.models import Category, Ad


def root(request):
    return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all()

        response = []
        for category in categories:
            response.append({
                "id": category.id,
                "name": category.name
            })

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False}, status=200)

    def post(self, request):
        category_data = json.loads(request.body)

        category = Category()
        category.name = category_data["name"]
        category.save()

        return JsonResponse(
            {
                "id": category.id,
                "text": category.name
            }, status=200)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, *args, **kwargs):

        category = self.get_object()

        return JsonResponse({
            "id": category.id,
            "name": category.name
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdView(View):
    def get(self, request):
        ads = Ad.objects.all()

        response = []
        for ad in ads:
            response.append({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price,
                "description": ad.description,
                "address": ad.address,
                "is_published": ad.is_published
            })

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False}, status=200)

    def post(self, request):
        ad_data = json.loads(request.body)

        ad = Ad()
        ad.name = ad_data["name"]
        ad.author = ad_data["author"]
        ad.price = ad_data["price"]
        ad.description = ad_data["description"]
        ad.address = ad_data["address"]
        ad.is_published = ad_data["is_published"]
        ad.save()

        return JsonResponse(
            {
                "id": ad.id,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price,
                "description": ad.description,
                "address": ad.address,
                "is_published": ad.is_published
            }, status=200)


class AdDetailView(DetailView):
    model = Ad

    def get(self, *args, **kwargs):
        ad = self.get_object()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published
        }, status=200)

