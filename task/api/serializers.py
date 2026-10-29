from rest_framework import serializers
from task import models
from account.api.serializers import UserSerializer


class TaskOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = ["id", "title", "status", "priority"]


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    first_tasks = TaskOneSerializer(many=True, read_only=True)

    class Meta:
        model = models.Project
        fields = [
            "id",
            "owner",
            "name",
            "slug",
            "description",
            "first_tasks",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id", "owner", "slug", "first_tasks",
            "created_at", "updated_at",
        ]


class ProjectRUDSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = models.Project
        fields = [
            "id",
            "owner",
            "name",
            "slug",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id", "owner", "slug",
            "created_at", "updated_at",
        ]


class TaskSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(
        read_only=True,
        slug_field="slug",
    )

    class Meta:
        model = models.Task
        fields = [
            "id",
            "project",
            "title",
            "description",
            "status",
            "priority",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id", "project", "created_at", "updated_at",
        ]