from django.urls import path
from users import views


urlpatterns = [
    path('', views.UserListView.as_view()),
    path('<int:pk>/', views.UserDetailView.as_view()),
    path('create/', views.UserCrateView.as_view()),
]