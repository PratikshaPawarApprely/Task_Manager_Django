
from categories.models import Category

category_data = [
    {
        "name": "Bug Fixing",
        "description": "Identifying and fixing software defects",
    },
    {
        "name": "Code Review",
        "description": "Reviewing code quality and best practices",
    },
    {
        "name": "Database",
        "description": "Database design, queries, and optimization",
    },
    {
        "name": "Performance",
        "description": "Improving application speed and scalability",
    },
    {
        "name": "Security",
        "description": "Authentication, authorization, and security improvements",
    },
    {
        "name": "Maintenance",
        "description": "Routine updates and application maintenance",
    },
]

created_count = 0

for data in category_data:
    category, created = Category.objects.get_or_create(
        name=data["name"],
        defaults={"description": data["description"]},
    )

    if created:
        created_count += 1
        print(f"Created: {category.name}")
    else:
        print(f"Already exists: {category.name}")

print("New categories created:", created_count)
print("Total categories:", Category.objects.count())
