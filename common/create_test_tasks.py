
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.db import transaction

from tasks.models import Task
from projects.models import Project
from categories.models import Category

User = get_user_model()

users = list(
    User.objects.filter(username__startswith="user").order_by("id")
)
projects = list(Project.objects.all().order_by("id"))
categories = list(Category.objects.all().order_by("id"))

if not users:
    raise Exception("No test users found. Create test users first.")

if not projects:
    raise Exception("No projects found. Create projects first.")

if not categories:
    raise Exception("No categories found. Create categories first.")

# Check the fields and choices used by your Task model.
print("Task fields:", [field.name for field in Task._meta.fields])
print("Users:", len(users))
print("Projects:", len(projects))
print("Categories:", len(categories))

# Check that the model has the expected fields before creating records.
required_fields = {
    "title", "description", "priority", "created_by",
    "assigned_to", "project", "category", "due_date",
}
actual_fields = {field.name for field in Task._meta.fields}

missing_fields = required_fields - actual_fields
if missing_fields:
    raise Exception(f"Update script for missing fields: {missing_fields}")

priorities = ["low", "medium", "high"]

tasks_to_create = []
start_number = Task.objects.count() + 1

for i in range(10_000):
    creator = users[i % len(users)]
    assignee = users[(i + 1) % len(users)]

    tasks_to_create.append(
        Task(
            title=f"Performance Test Task {start_number + i}",
            description=(
                f"Sample task for database performance testing. "
                f"Record number {start_number + i}."
            ),
            priority=priorities[i % len(priorities)],
            created_by=creator,
            assigned_to=assignee,
            project=projects[i % len(projects)],
            category=categories[i % len(categories)],
            due_date=date.today() + timedelta(days=i % 90),
        )
    )

with transaction.atomic():
    Task.objects.bulk_create(tasks_to_create, batch_size=1000)

print("New tasks created:", len(tasks_to_create))
print("Total tasks in database:", Task.objects.count())
