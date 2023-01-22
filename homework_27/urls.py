from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework import routers
from ads.selection_views import SelectionViewSet
from ads import views
from locations.views import LocationViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = routers.SimpleRouter()
router.register('location', LocationViewSet, basename='Location')
router1 = routers.SimpleRouter()
router1.register('selection', SelectionViewSet, basename='Selection')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', views.root),
    path('cat/', include('categories.urls')),
    path('ad/', include('ads.urls')),
    path('user/', include('users.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'))
]

urlpatterns += router.urls
urlpatterns += router1.urls


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
