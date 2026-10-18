from django.db import models
import random
from django.utils.text import slugify


# Create your models here.


class Project(models.Model):
    owner = models.ForeignKey("User", on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
       base_slug = slugify(self.name)
       ran2 = random.randint(100000, 999999)
       ran = random.randint(1000, 9999)
       self.slug = f"{base_slug}-{ran2}-{ran}"
       super().save(*args, **kwargs) # Call the real save() method

    def __str__(self):
        return self.name[:20]
    


class Task(models.Model):
    PRIORITY_CHOICES = (
        (HIGH, "High"),
        (MEDIUM, "Medium"),
        (LOW, "Low"),
        )

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField()
    description = models.TextField()
    status = models.BooleanField(default=False)
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default="Low")
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title[:10]


class Comment(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    task = models.ForeignKey("Task", on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return self.body[:10]


class ProjectMembership(models.Model):
    ROLE_CHOICES = (
            (OWNER, "Owner"),
            (MEMBER, "Member"),
            )
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default="Member")

    class Meta:
        unique_together = ['project', 'user']   


    def __str__(self):
        return f"{self.project.name} -- {self.user.username}"