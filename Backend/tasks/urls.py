from django.urls import path
from .views import (
    TaskCreateView,
    TaskDetailView,
    TaskUpdateView,
    TaskDeleteView,
    GroupTaskListView,
    MyTaskListView,
)

urlpatterns = [
    path("tasks/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/my/", MyTaskListView.as_view(), name="my-task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("groups/<int:group_id>/tasks/", GroupTaskListView.as_view(), name="group-task-list"),
]