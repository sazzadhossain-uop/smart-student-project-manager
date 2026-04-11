from django.urls import path
from .views import CreateGroupView, JoinGroupView, MyGroupsView, GroupDetailView

urlpatterns = [
    path("", CreateGroupView.as_view(), name="create-group"),
    path("join/", JoinGroupView.as_view(), name="join-group"),
    path("my-groups/", MyGroupsView.as_view(), name="my-groups"),
    path("<int:pk>/", GroupDetailView.as_view(), name="group-detail"),
]