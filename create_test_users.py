
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create 100 test users for performance testing"

    def handle(self, *args, **options):
        User = get_user_model()
        created_count = 0

        for i in range(1, 101):
            name = f"User{i:03d}"
            username = name.lower()
            email = f"{username}@example.com"

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "first_name": name,
                },
            )

            if created:
                password = f"{name[:3].capitalize()}@932214"
                user.set_password(password)
                user.save()
                created_count += 1

        total = User.objects.filter(
            username__startswith="user"
        ).count()

        self.stdout.write(
            self.style.SUCCESS(
                f"New users created: {created_count}; "
                f"matching users in database: {total}"
            )
        )
