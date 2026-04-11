from rest_framework import serializers
from .models import Task


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "group",
            "title",
            "description",
            "assignee",
            "priority",
            "status",
            "due_date",
            "time",
        ]


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "assignee",
            "priority",
            "status",
            "due_date",
            "time",
        ]


class TaskListDetailSerializer(serializers.ModelSerializer):
    assignee_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    group_name = serializers.CharField(source="group.name", read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "group",
            "group_name",
            "title",
            "description",
            "assignee",
            "assignee_name",
            "priority",
            "status",
            "due_date",
            "time",
            "created_by",
            "created_by_name",
            "created_at",
            "updated_at",
        ]

    def get_assignee_name(self, obj):
        if obj.assignee:
            return obj.assignee.name if hasattr(obj.assignee, "name") else obj.assignee.email
        return None

    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.name if hasattr(obj.created_by, "name") else obj.created_by.email
        return None