from rest_framework import serializers
from .models import Group, GroupMember


class GroupMemberSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = GroupMember
        fields = ["id", "name", "email", "role", "joined_at"]

    def get_name(self, obj):
        if hasattr(obj.user, "username") and obj.user.username:
            return obj.user.username

        if hasattr(obj.user, "name") and obj.user.name:
            return obj.user.name

        return obj.user.email.split("@")[0]


class GroupSerializer(serializers.ModelSerializer):
    creator_name = serializers.SerializerMethodField()
    creator_email = serializers.EmailField(source="creator.email", read_only=True)
    members = GroupMemberSerializer(
        source="memberships",
        many=True,
        read_only=True
    )

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

    def get_creator_name(self, obj):
        if hasattr(obj.creator, "username") and obj.creator.username:
            return obj.creator.username

        if hasattr(obj.creator, "name") and obj.creator.name:
            return obj.creator.name

        return obj.creator.email.split("@")[0]


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
            raise serializers.ValidationError(
                "Group name or group code does not match."
            )

        attrs["group"] = group
        return attrs