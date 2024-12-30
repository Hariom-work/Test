from rest_framework import serializers
from .models import *

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source="owner.username")
    class Meta:
        model = Project
        fields = ["id", "name", "description","owner"]

class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMember
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    project = serializers.CharField(source="project.name")
    assign_to = serializers.CharField(source="assign_to.username",default=None)
    class Meta:
        model = Task
        fields = ["id", "title", "description", "assign_to", "project", "due_date"]

class CommentSerializer(serializers.ModelSerializer):
    task = serializers.CharField(source="task.title")
    user = serializers.CharField(source="user.username")

    class Meta:
        model = Comment
        fields = ["id", "content", "task", "user"]