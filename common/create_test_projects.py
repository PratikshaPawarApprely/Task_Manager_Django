
from projects.models import Project

project_data = [
    {
        "name": "E-Commerce Platform",
        "description": "Manage products, orders, and inventory.",
    },
    {
        "name": "Online Learning Platform",
        "description": "Manage courses and student progress.",
    },
    {
        "name": "YouTube Analytics Dashboard",
        "description": "Track video views and engagement.",
    },
    {
        "name": "Hospital Appointment System",
        "description": "Manage patient appointments and schedules.",
    },
    {
        "name": "Food Delivery Management",
        "description": "Manage orders and delivery status.",
    },
]

created_count = 0

for data in project_data:
    project, created = Project.objects.get_or_create(
        name=data["name"],
        defaults={"description": data["description"]},
    )
    if created:
        created_count += 1
        print(f"Created: {project.name}")
    else:
        print(f"Already exists: {project.name}")

print("New projects created:", created_count)
print("Total projects:", Project.objects.count())
