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

        if GroupMember.objects.filter(user=user, group=group).exists():
            return Response({"detail": "You already joined this group."}, status=400)

        current_member_count = GroupMember.objects.filter(group=group).count()

        if current_member_count >= group.expected_members:
            return Response({"detail": "This group is already full."}, status=400)

        GroupMember.objects.create(user=user, group=group, role="member")

        return Response(GroupSerializer(group).data, status=200)


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


class RemoveMemberView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        email = request.data.get("email")

        if not email:
            return Response({"detail": "Email is required."}, status=400)

        try:
            group = Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            return Response({"detail": "Group not found."}, status=404)

        actor = GroupMember.objects.filter(user=request.user, group=group).first()

        if not actor:
            return Response({"detail": "You are not in this group."}, status=403)

        if actor.role not in ["leader", "co-leader"]:
            return Response(
                {"detail": "Only leader or co-leader can remove members."},
                status=403,
            )

        target = GroupMember.objects.filter(group=group, user__email=email).first()

        if not target:
            return Response({"detail": "Member not found in this group."}, status=404)

        if target.user == request.user:
            return Response({"detail": "You cannot remove yourself."}, status=400)

        if target.role == "leader":
            return Response({"detail": "Leader cannot be removed."}, status=400)

        if actor.role == "co-leader" and target.role != "member":
            return Response(
                {"detail": "Co-leader can remove only regular members."},
                status=403,
            )

        target.delete()

        return Response(
            {
                "detail": "Member removed successfully.",
                "group": GroupSerializer(group).data,
            },
            status=200,
        )


class MakeCoLeaderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        email = request.data.get("email")

        if not email:
            return Response({"detail": "Email is required."}, status=400)

        try:
            group = Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            return Response({"detail": "Group not found."}, status=404)

        actor = GroupMember.objects.filter(user=request.user, group=group).first()

        if not actor or actor.role != "leader":
            return Response({"detail": "Only leader can make co-leader."}, status=403)

        target = GroupMember.objects.filter(group=group, user__email=email).first()

        if not target:
            return Response({"detail": "Member not found in this group."}, status=404)

        if target.role == "leader":
            return Response({"detail": "Leader role cannot be changed."}, status=400)

        target.role = "co-leader"
        target.save()

        return Response(
            {
                "detail": "Member promoted to co-leader.",
                "group": GroupSerializer(group).data,
            },
            status=200,
        )


class RemoveCoLeaderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        email = request.data.get("email")

        if not email:
            return Response({"detail": "Email is required."}, status=400)

        try:
            group = Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            return Response({"detail": "Group not found."}, status=404)

        actor = GroupMember.objects.filter(user=request.user, group=group).first()

        if not actor or actor.role != "leader":
            return Response({"detail": "Only leader can remove co-leader role."}, status=403)

        target = GroupMember.objects.filter(group=group, user__email=email).first()

        if not target:
            return Response({"detail": "Member not found in this group."}, status=404)

        if target.role != "co-leader":
            return Response({"detail": "This member is not a co-leader."}, status=400)

        target.role = "member"
        target.save()

        return Response(
            {
                "detail": "Co-leader role removed.",
                "group": GroupSerializer(group).data,
            },
            status=200,
        )