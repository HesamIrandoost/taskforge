from rest_framework import permissions

from task.models import ProjectMembership


class IsProjectOwner(permissions.BasePermission):
    """
    Only project owners and superusers can access the object.
    """

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        # obj can be either a Project or a Task.
        project = getattr(obj, "project", obj)

        return ProjectMembership.objects.filter(
            project=project,
            user=request.user,
            role=ProjectMembership.Role.OWNER,
        ).exists()


class IsProjectMember(permissions.BasePermission):
    """
    Project owners and members can access the object.
    Viewers are excluded.
    """

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        project = getattr(obj, "project", obj)

        return ProjectMembership.objects.filter(
            project=project,
            user=request.user,
            role__in=[
                ProjectMembership.Role.OWNER,
                ProjectMembership.Role.MEMBER,
            ],
        ).exists()


class IsProjectViewer(permissions.BasePermission):
    """
    Any project participant can view the object.
    """

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        project = getattr(obj, "project", obj)

        return ProjectMembership.objects.filter(
            project=project,
            user=request.user,
        ).exists()


class IsTaskMember(IsProjectMember):
    """
    Reuse project membership rules for Task objects.
    """

    pass
