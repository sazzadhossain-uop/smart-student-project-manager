from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Group, GroupMember
from .serializers import GroupSerializer, GroupCreateSerializer, JoinGroupSerializer


class CreateGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GroupCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group = serializer.save(creator=request.user)

        GroupMember.objects.create(
            user=request.user,
            group=group,
            role="leader",
        )

        return Response(GroupSerializer(group).data, status=status.HTTP_201_CREATED)


class JoinGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = JoinGroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group = serializer.validated_data["group"]
        user = request.user

        already_joined = GroupMember.objects.filter(user=user, group=group).exists()
        if already_joined:
            return Response(
                {"detail": "You already joined this group."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        current_member_count = GroupMember.objects.filter(group=group).count()
        if current_member_count >= group.expected_members:
            return Response(
                {"detail": "This group is already full."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        GroupMember.objects.create(
            user=user,
            group=group,
            role="member",
        )

        return Response(GroupSerializer(group).data, status=status.HTTP_200_OK)


class MyGroupsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GroupSerializer

    def get_queryset(self):
        return Group.objects.filter(
            memberships__user=self.request.user
        ).distinct().order_by("-created_at")


class GroupDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GroupSerializer
    queryset = Group.objects.all()