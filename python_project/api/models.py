from datetime import time
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.functions import Now
import uuid
from authentication.models import CustomUser
# Create your models here.
class CommonModel(models.Model):
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def last_updated(self):
        return self.modified_at.strftime("%d %b %y %I:%M %p")
    

class Project(CommonModel):

    class Meta:
        db_table ="projects"

    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(null=False, blank=False, max_length=50)
    description = models.TextField(null=False, blank=False)


class ProjectMember(models.Model):
    class Meta:
        db_table ="project_members"

    class RoleType(models.TextChoices):
        MEMBER = "member", _("Member")
        ADMIN = "admin", _("Admin")

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="project_memberships")
    role = models.CharField(max_length=20, choices=RoleType.choices, default=RoleType.MEMBER)


class Task(CommonModel):
    class Meta:
        db_table ="tasks"

    class Status(models.TextChoices):
        TO_DO = "to_do", _("To Do")
        IN_PROGRESS = "in_progress", _("In Progress")
        DONE = "done", _("Done")

    class Priority(models.TextChoices):
        LOW = "low", _("Low")
        MEDIUM = "medium", _("Medium")
        HIGH = "high", _("High")

    title = models.CharField(max_length=50)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.TO_DO)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.LOW)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    due_date = models.DateTimeField()

class Comment(CommonModel):
    content = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="comments")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")