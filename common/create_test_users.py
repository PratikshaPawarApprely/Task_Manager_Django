
from django.contrib.auth import get_user_model

User = get_user_model()
created_count = 0

for i in range(1, 101):
    name = f"User{i:03d}"
    username = name.lower()

    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            "email": f"{username}@example.com",
            "first_name": name,
        },
    )

    if created:
        user.set_password(f"{name[:3]}@932214")
        user.save()
        created_count += 1

total = User.objects.filter(username__startswith="user").count()

print(f"New users created: {created_count}")
print(f"Matching users in database: {total}")
