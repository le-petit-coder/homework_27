import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from users.models import User
from locations.models import Location
from django.core.paginator import Paginator
from homework_27.settings import TOTAL_ON_PAGE


@method_decorator(csrf_exempt, name='dispatch')
class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        search_text = request.GET.get("text", None)
        if search_text:
            self.object_list = self.object_list.filter(text=search_text)

        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        users = []
        for user in page_obj:
            users.append({
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "age": user.age,
                "locations": list(user.locations.all().values_list("name", flat=True)),
                "total_ads": user.ad_set.filter(is_published=True).count()
            })

        response = {
            "items": users,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False}, status=200)


class UserDetailView(DetailView):
    model = User

    def get(self, *args, **kwargs):
        user = self.get_object()

        return JsonResponse({
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "age": user.age,
            "locations": [loc.name for loc in user.locations.all()],
            "total_ads": user.ad_set.filter(is_published=True).count()
        }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserCrateView(CreateView):
    model = User
    fields = ["username", "first_name", "last_name", "role", "age", "locations", "password"]

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        user = User.objects.create(
            username=user_data.get("username"),
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
            password=user_data.get("password"),
            role=user_data.get("role"),
            age=user_data.get("age"),
        )

        for loc in user_data.get("locations"):
            location, _ = Location.objects.get_or_create(name=loc)
            user.locations.add(location)

        return JsonResponse(
            {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "age": user.age,
                "locations": [loc.name for loc in user.locations.all()],
            }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = "__all__"

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)

        if "username" in user_data:
            self.object.username = user_data["username"]
        if "first_name" in user_data:
            self.object.first_name = user_data["first_name"]
        if "last_name" in user_data:
            self.object.last_name = user_data["last_name"]
        if "age" in user_data:
            self.object.age = user_data["age"]
        if "locations" in user_data:
            self.object.locations.all().delete()
            for loc in user_data.get("locations"):
                location, _ = Location.objects.get_or_create(name=loc)
                self.object.locations.add(location)

        return JsonResponse({
            "id": self.object.id,
            "username": self.object.username,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "role": self.object.role,
            "age": self.object.age,
            "locations": [loc.name for loc in self.object.locations.all()],
            })


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"
    fields = "__all__"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)