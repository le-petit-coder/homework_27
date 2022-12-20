import json

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from ads.models import Ad
from django.core.paginator import Paginator
from homework_27.settings import TOTAL_ON_PAGE


def root(request):
    return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        search_text = request.GET.get("text", None)
        if search_text:
            self.object_list = self.object_list.filter(text=search_text)

        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        ads = []
        for ad in page_obj:
            ads.append({
                "id": ad.id,
                "name": ad.name,
                "author_id": ad.author_id,
                "price": ad.price,
                "description": ad.description,
                "address": ad.address,
                "is_published": ad.is_published,
                "image": ad.image.url if ad.image else None,
                #"category_id": ad.category_id if ad.category_id else None
            })

        response = {
            "items": ads,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdCrateView(CreateView):
    model = Ad
    fields = ["name", "author_id", "price", "description", "address", "is_published", "image", "category_id"]

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)

        ad = Ad.objects.create(
            name=ad_data["name"],
            author_id=ad_data["author_id"],
            price=ad_data["price"],
            description=ad_data["description"],
            address=ad_data["address"],
            is_published=ad_data["is_published"],
            image=ad_data["image"] if ad_data["image"] else None,
            #category_id=ad_data["category_id"]
        )

        return JsonResponse(
            {
                "id": ad.id,
                "name": ad.name,
                "author_id": ad.author_id,
                "price": ad.price,
                "description": ad.description,
                "address": ad.address,
                "is_published": ad.is_published,
                "image": ad.image if ad_data["image"] else None,
                #"category_id": ad.category.id
            }, status=200)


class AdDetailView(DetailView):
    model = Ad

    def get(self, *args, **kwargs):
        ad = self.get_object()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author_id,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published,
            "image": ad.image if ad.image else None,
            #"category_id": ad.category.id
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ["name", "author_id", "price", "description", "address", "is_published", "image", "category_id"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)

        self.object.name=ad_data["name"]
        self.object.author_id=ad_data["author_id"]
        self.object.price=ad_data["price"]
        self.object.description=ad_data["description"]
        self.object.address=ad_data["address"]
        self.object.is_published=ad_data["is_published"]
        self.object.image=ad_data["image"] if self.object.image else None
        #self.object.category_id=ad_data["category_id"]

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "price": self.object.price,
            "description": self.object.description,
            "address": self.object.address,
            "is_published": self.object.is_published,
            "image": self.object.image if self.object.image else None,
            #"category_id": self.object.category_id
            })


@method_decorator(csrf_exempt, name='dispatch')
class AdImageUpdate(UpdateView):
    model = Ad
    fields = ["name", "author_id", "price", "description", "address", "is_published", "image", "category_id"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES["image"]
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            #"author": self.object.author,
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
    fields = ["name", "author_id", "price", "description", "address", "is_published", "image", "category_id"]

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)