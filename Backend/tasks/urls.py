from django.urls import path
from .views import task_list_create, task_detail

urlpatterns = [
    path("", task_list_create),
    path("<int:pk>/", task_detail),
]