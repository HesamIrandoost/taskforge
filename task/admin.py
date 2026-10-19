from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Project, Task, Comment, ProjectMembership


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    show_change_link = True
    fields = ("title", "status", "priority", "created_at")
    readonly_fields = ("created_at",)


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    show_change_link = True
    fields = ("user", "body", "created_at")
    readonly_fields = ("created_at",)


class ProjectMembershipInline(admin.TabularInline):
    model = ProjectMembership
    extra = 0
    autocomplete_fields = ("user",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "slug",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at", "updated_at")
    search_fields = ("name", "slug", "owner__username")
    autocomplete_fields = ("owner",)
    readonly_fields = ("id", "slug", "created_at", "updated_at")
    inlines = (TaskInline, ProjectMembershipInline)
    date_hierarchy = "created_at"
    list_per_page = 25


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "project",
        "status",
        "priority",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "priority", "created_at")
    search_fields = ("title", "project__name")
    autocomplete_fields = ("project",)
    readonly_fields = ("created_at", "updated_at")
    inlines = (CommentInline,)
    list_select_related = ("project",)
    date_hierarchy = "created_at"
    list_per_page = 25


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "task", "user", "created_at")
    list_filter = ("created_at",)
    search_fields = ("body", "user__username", "task__title")
    autocomplete_fields = ("user", "task")
    readonly_fields = ("created_at",)
    list_select_related = ("user", "task")
    date_hierarchy = "created_at"
    list_per_page = 50


@admin.register(ProjectMembership)
class ProjectMembershipAdmin(admin.ModelAdmin):
    list_display = ("project", "user", "role")
    list_filter = ("role",)
    search_fields = ("project__name", "user__username")
    autocomplete_fields = ("project", "user")
    list_select_related = ("project", "user")
