from django.urls import path
from . import views

app_name = "task"

urlpatterns = [
    path("projects/", views.ProjectAPIView.as_view(), name="projects"),

]
