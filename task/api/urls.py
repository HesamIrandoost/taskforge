# from django.urls import path
# from . import views

# app_name = "task"

# urlpatterns = [
#     path("projects/", views.ProjectAPIView.as_view(), name="projects"),
#     path("projects/<slug:slug>/", views.ProjectDetailAPIView.as_view(), name="projects-detail"),

# ]


from django.urls import path

from .views import (
    ProjectAPIView,
    ProjectDetailAPIView,
    TaskListView,
    TaskDetailView,
)

urlpatterns = [
    path(
        "projects/",
        ProjectAPIView.as_view(),
        name="project-list",
    ),
    path(
        "projects/<slug:slug>/",
        ProjectDetailAPIView.as_view(),
        name="project-detail",
    ),
    path(
        "projects/<slug:slug>/tasks/",
        TaskListView.as_view(),
        name="task-list",
    ),
    path(
        "projects/<slug:slug>/tasks/<int:pk>/",
        TaskDetailView.as_view(),
        name="task-detail",
    ),
]