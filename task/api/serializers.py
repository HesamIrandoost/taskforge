from rest_framework import serializers
from task import models
from account.api.serializers import UserSerializer


class TaskOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = [
            "title",
            "status",
            "priority",
        ]


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    first_task = TaskOneSerializer(read_only=True, many=True)
    
    class Meta:
        model = models.Project
        fields = [
            "id",
            "owner",
            "name",
            "slug",
            "description",
            'first_task',
            "created_at",
            "updated_at",
        ]


        read_only_fields = [
            'id', 'owner', 'slug', 'first_task', "created_at", "updated_at",
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
            'id', 'owner', 'slug', "created_at", "updated_at",
        ]

class TaskSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    project_id = ProjectSerializer(write_only=True)

    class Meta:
        model = models.Task
        fields = [
            "id",
            "project",
            "project_id",
            "title",
            "description",
            "status",
            "priority",
            "created_at",
            "updated_at",
        ]


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    task = TaskSerializer(read_only=True)

    class Meta:
        model = models.Comment
        fields = [
            "id",
            "user",
            "task",
            "body",
            "created_at",
        ]


class ProjectMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = models.ProjectMembership
        fields = [
            "id",
            "project",
            "user",
            "role",
        ]
