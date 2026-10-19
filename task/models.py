from django.db import models, transaction
import random, uuid
from django.utils.text import slugify
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="projects")
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding

        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = f"{base_slug}-{self.id}"
        
        with transaction.atomic():
            super().save(*args, **kwargs) # Call the real save() method

            if is_new and self.owner:
                ProjectMembership.objects.get_or_create(
                    project=self,
                    user=self.owner,
                    defaults={
                        "role": ProjectMembership.Role.OWNER    
                    }
                )

    def __str__(self):
        return self.name[:20]
    


class Task(models.Model):
    
    class Priority(models.TextChoices):
        HIGH = "High", "High"
        MEDIUM = "Medium", "Medium"
        LOW = "Low", "Low"

    class Status(models.TextChoices):
        TODO = "Todo", "Todo"
        IN_PROGRESS = "In_progress", "In_progress"
        DONE = "Done", "Done"
 
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.TODO)
    priority = models.CharField(max_length=50, choices=Priority.choices, default=Priority.LOW)
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title[:10]


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="comments")
    task = models.ForeignKey("Task", on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        username = self.user.username if self.user else "deleted user" 
        return f"{username} - {self.body[:10]}"


class ProjectMembership(models.Model):
    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        VIEWER = "viewer", "Viewer"
        MEMBER = "member", "Member"
            
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="project_memberships")
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.MEMBER)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "project"],
                name="unique_project_member"
                ),
            models.UniqueConstraint(
                fields=["project"],
                condition=models.Q(role="owner"),
                name="unique_project_owner",
            ),
        ]

    def __str__(self):
        return f"{self.project.name} -- {self.user.username}"