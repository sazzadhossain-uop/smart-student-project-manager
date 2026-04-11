from rest_framework import serializers
from .models import Group, GroupMember


class GroupMemberSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = GroupMember
        fields = ["id", "name", "email", "role", "joined_at"]


class GroupSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source="creator.name", read_only=True)
    creator_email = serializers.EmailField(source="creator.email", read_only=True)
    members = GroupMemberSerializer(source="memberships", many=True, read_only=True)

    class Meta:
        model = Group
        fields = [
            "id",
            "group_name",
            "group_code",
            "expected_members",
            "creator",
            "creator_name",
            "creator_email",
            "members",
            "created_at",
        ]
        read_only_fields = ["id", "creator", "created_at"]


class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["group_name", "group_code", "expected_members"]

    def validate_group_code(self, value):
        if Group.objects.filter(group_code__iexact=value).exists():
            raise serializers.ValidationError("This group code already exists.")
        return value


class JoinGroupSerializer(serializers.Serializer):
    group_name = serializers.CharField()
    group_code = serializers.CharField()

    def validate(self, attrs):
        group_name = attrs.get("group_name", "").strip()
        group_code = attrs.get("group_code", "").strip()

        try:
            group = Group.objects.get(
                group_name__iexact=group_name,
                group_code__iexact=group_code,
            )
        except Group.DoesNotExist:
            raise serializers.ValidationError("Group name or group code does not match.")

        attrs["group"] = group
        return attrs