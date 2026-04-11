from django.conf import settings
from django.db import models


class Group(models.Model):
    ROLE_CHOICES = (
        ("leader", "Leader"),
        ("co-leader", "Co-Leader"),
        ("member", "Member"),
    )

    group_name = models.CharField(max_length=255)
    group_code = models.CharField(max_length=50, unique=True)
    expected_members = models.PositiveIntegerField()
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_groups",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.group_name} ({self.group_code})"


class GroupMember(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="group_memberships",
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    role = models.CharField(max_length=20, choices=Group.ROLE_CHOICES, default="member")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "group")

    def __str__(self):
        return f"{self.user.email} - {self.group.group_name} - {self.role}"