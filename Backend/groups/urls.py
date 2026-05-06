from django.urls import path
from .views import (
    CreateGroupView,
    JoinGroupView,
    MyGroupsView,
    GroupDetailView,
    RemoveMemberView,
    MakeCoLeaderView,
    RemoveCoLeaderView,
)

urlpatterns = [
    path("", CreateGroupView.as_view(), name="create-group"),

    path("join/", JoinGroupView.as_view(), name="join-group"),

    path("my-groups/", MyGroupsView.as_view(), name="my-groups"),

    path("<int:pk>/", GroupDetailView.as_view(), name="group-detail"),

    path(
        "<int:pk>/remove-member/",
        RemoveMemberView.as_view(),
        name="remove-member",
    ),

    path(
        "<int:pk>/make-co-leader/",
        MakeCoLeaderView.as_view(),
        name="make-co-leader",
    ),

    path(
        "<int:pk>/remove-co-leader/",
        RemoveCoLeaderView.as_view(),
        name="remove-co-leader",
    ),
]