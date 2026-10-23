from django.db.models import Prefetch

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import (
    IsProjectMember, IsProjectOwner , IsProjectViewer, IsTaskMember
)
from ..models import (
    Project, ProjectMembership, Comment, Task
)
from .serializers import (
    ProjectSerializer,
    CommentSerializer,
    TaskSerializer,
    ProjectMembershipSerializer,
)


# ---------------------------
#     Project API's
# ---------------------------

class ProjectAPIView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        first_task = Task.objects.order_by(
            'created_at', 'pk'
        )[:2]

        queryset = Project.objects.filter(
            members__user=self.request.user
            ).select_related(
                "owner").prefetch_related(
                    Prefetch(
                        "tasks",
                        queryset=first_task,
                        to_attr="first_task"
                    )
                )
        return queryset
        
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer    
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD']:
            self.permission_classes = [IsProjectViewer]
        elif self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsProjectMember]
