from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Task
from .serializers import (
    TaskCreateSerializer,
    TaskUpdateSerializer,
    TaskListDetailSerializer,
)
from groups.models import GroupMember


def is_group_member(user, group):
    return GroupMember.objects.filter(group=group, user=user).exists()


def is_group_manager(user, group):
    return GroupMember.objects.filter(
        group=group,
        user=user,
        role__in=["leader", "co-leader"]
    ).exists()


class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        group = serializer.validated_data["group"]
        user = self.request.user

        if not is_group_member(user, group):
            raise PermissionDenied("You are not a member of this group.")

        if not is_group_manager(user, group):
            raise PermissionDenied("Only leader or co-leader can create tasks.")

        serializer.save(created_by=user)


class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.select_related("group", "assignee", "created_by")
    serializer_class = TaskListDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        task = super().get_object()
        user = self.request.user

        if not is_group_member(user, task.group):
            raise PermissionDenied("You are not a member of this group.")

        return task


class TaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.select_related("group", "assignee", "created_by")
    serializer_class = TaskUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        task = super().get_object()
        user = self.request.user

        if not is_group_member(user, task.group):
            raise PermissionDenied("You are not a member of this group.")

        if not is_group_manager(user, task.group):
            raise PermissionDenied("Only leader or co-leader can update tasks.")

        return task


class TaskDeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        task = super().get_object()
        user = self.request.user

        if not is_group_member(user, task.group):
            raise PermissionDenied("You are not a member of this group.")

        if not is_group_manager(user, task.group):
            raise PermissionDenied("Only leader or co-leader can delete tasks.")

        return task


class GroupTaskListView(generics.ListAPIView):
    serializer_class = TaskListDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        group_id = self.kwargs["group_id"]

        membership = GroupMember.objects.filter(group_id=group_id, user=user).first()

        if not membership:
            raise PermissionDenied("You are not a member of this group.")

        if membership.role in ["leader", "co-leader"]:
            return Task.objects.filter(group_id=group_id).select_related(
                "group", "assignee", "created_by"
            ).order_by("-created_at")

        return Task.objects.filter(
            group_id=group_id,
            assignee=user
        ).select_related("group", "assignee", "created_by").order_by("-created_at")


class MyTaskListView(generics.ListAPIView):
    serializer_class = TaskListDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(
            assignee=self.request.user
        ).select_related("group", "assignee", "created_by").order_by("-created_at")