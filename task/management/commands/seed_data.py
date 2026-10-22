
import random
import uuid

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from ...models import Project, Task, Comment


User = get_user_model()


class Command(BaseCommand):
    help = "Create sample users, projects, tasks and comments"

    @transaction.atomic
    def handle(self, *args, **options):
        rng = random.Random(42)

        self.stdout.write("Creating users...")

        users = []

        # Create 20 users
        for i in range(1, 21):
            username = f"seed_user_{i:02d}"

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": f"{username}@example.com",
                    "first_name": f"User{i}",
                    "last_name": "Test",
                },
            )

            if created:
                user.set_password("TestPass123!")
                user.save(update_fields=["password"])

            users.append(user)

        self.stdout.write(f"Users ready: {len(users)}")

        priorities = [
            Task.Priority.HIGH,
            Task.Priority.MEDIUM,
            Task.Priority.LOW,
        ]

        statuses = [
            Task.Status.TODO,
            Task.Status.IN_PROGRESS,
            Task.Status.DONE,
        ]

        task_titles = [
            "Implement authentication",
            "Fix API validation",
            "Write unit tests",
            "Optimize database queries",
            "Build dashboard endpoint",
            "Add pagination",
            "Review permissions",
            "Improve error handling",
            "Update documentation",
            "Configure deployment",
        ]

        comment_messages = [
            "I have started working on this.",
            "Can we review this together?",
            "The implementation looks good.",
            "I found an issue that needs fixing.",
            "The tests are passing now.",
            "I will handle this today.",
            "Could you provide more details?",
            "This is ready for review.",
        ]

        self.stdout.write("Creating projects, tasks and comments...")

        total_projects = 0
        total_tasks = 0
        total_comments = 0

        for user in users:
            # Five projects per user
            for project_number in range(1, 6):
                project_id = uuid.uuid5(
                    uuid.NAMESPACE_URL,
                    f"taskforge-seed-{user.pk}-{project_number}",
                )

                project, project_created = Project.objects.get_or_create(
                    id=project_id,
                    defaults={
                        "owner": user,
                        "name": (
                            f"Seed Project {project_number} "
                            f"- {user.username}"
                        ),
                        "description": (
                            f"Sample project {project_number} "
                            f"owned by {user.username}."
                        ),
                    },
                )

                if project_created:
                    total_projects += 1

                # Three to ten tasks per project
                task_count = rng.randint(3, 10)

                for task_number in range(1, task_count + 1):
                    title = (
                        f"{task_number}. "
                        f"{rng.choice(task_titles)}"
                    )

                    task, task_created = Task.objects.get_or_create(
                        project=project,
                        title=title,
                        defaults={
                            "description": (
                                f"Sample task {task_number} "
                                f"for {project.name}."
                            ),
                            "status": rng.choice(statuses),
                            "priority": rng.choice(priorities),
                        },
                    )

                    if task_created:
                        total_tasks += 1

                    # One to four comments per task
                    comment_count = rng.randint(1, 4)

                    for comment_number in range(1, comment_count + 1):
                        message = rng.choice(comment_messages)
                        body = (
                            f"[Seed comment {comment_number}] {message}"
                        )

                        comment, comment_created = (
                            Comment.objects.get_or_create(
                                task=task,
                                body=body,
                                defaults={
                                    "user": rng.choice(users),
                                },
                            )
                        )

                        if comment_created:
                            total_comments += 1

        self.stdout.write(
            self.style.SUCCESS(
                "\nSample data generation completed!\n"
                f"Users available: {len(users)}\n"
                f"New projects: {total_projects}\n"
                f"New tasks: {total_tasks}\n"
                f"New comments: {total_comments}"
            )
        )

