from django.db.models import Prefetch
from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions

from ..models import Project, Task
from .permissions import (
    IsProjectMember,
    IsProjectOwner,
    IsProjectViewer,
)
from .serializers import (
    ProjectSerializer,
    ProjectRUDSerializer,
    TaskSerializer,
)


# ---------------------------
# Project APIs
# ---------------------------

class ProjectAPIView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        first_tasks = Task.objects.order_by(
            "created_at", "pk"
        )[:2]

        return (
            Project.objects
            .filter(members__user=self.request.user)
            .select_related("owner")
            .prefetch_related(
                Prefetch(
                    "tasks",
                    queryset=first_tasks,
                    to_attr="first_tasks",
                )
            )
            .order_by("-created_at")
            .distinct()
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProjectDetailAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = ProjectRUDSerializer
    lookup_field = "slug"

    def get_permissions(self):
        if self.request.method in ("GET", "HEAD", "OPTIONS"):
            classes = [IsProjectViewer]
        else:
            classes = [IsProjectOwner]

        return [permission() for permission in classes]

    def get_queryset(self):
        return (
            Project.objects
            .filter(members__user=self.request.user)
            .select_related("owner")
            .distinct()
        )


# ---------------------------
# Task APIs
# ---------------------------

class TaskListView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ("GET", "HEAD", "OPTIONS"):
            classes = [IsProjectViewer]
        else:
            classes = [IsProjectMember]

        return [permission() for permission in classes]

    def get_queryset(self):
        return (
            Task.objects
            .filter(
                project__slug=self.kwargs["slug"],
                project__members__user=self.request.user,
            )
            .order_by("-created_at")
        )

    def perform_create(self, serializer):
        project = get_object_or_404(
            Project.objects.filter(
                members__user=self.request.user
            ),
            slug=self.kwargs["slug"],
        )

        serializer.save(project=project)


class TaskDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = TaskSerializer

    def get_permissions(self):
        if self.request.method in ("GET", "HEAD", "OPTIONS"):
            classes = [IsProjectViewer]
        else:
            classes = [IsProjectMember]

        return [permission() for permission in classes]

    def get_queryset(self):
        return (
            Task.objects
            .filter(
                project__slug=self.kwargs["slug"],
                project__members__user=self.request.user,
            )
            .order_by("-created_at")
        )