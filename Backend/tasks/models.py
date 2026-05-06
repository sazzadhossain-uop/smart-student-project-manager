from django.db import models


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]

    STATUS_CHOICES = [
        ("todo", "To Do"),
        ("progress", "In Progress"),
        ("done", "Done"),
    ]

    group_id = models.CharField(max_length=100, default="")

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True, default="")

    assignee_name = models.CharField(max_length=255, blank=True, default="")

    assignee_email = models.EmailField(blank=True, default="")

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="medium"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="todo"
    )

    time = models.CharField(max_length=50, blank=True, default="")

    due_date = models.DateField(null=True, blank=True)

    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title