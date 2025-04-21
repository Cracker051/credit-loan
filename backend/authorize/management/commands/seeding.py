from django.core.management.base import BaseCommand
from django.db import transaction

from backend.authorize.models import Role, User
from backend.base.const import RoleChoices


class Command(BaseCommand):
    help = "Seeds the database with initial data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding roles...")
        with transaction.atomic():
            user_role, _ = Role.objects.get_or_create(name=RoleChoices.USER)
            operator_role, _ = Role.objects.get_or_create(name=RoleChoices.OPERATOR)
            admin_role, _ = Role.objects.get_or_create(name=RoleChoices.ADMIN)

            self.stdout.write(self.style.SUCCESS("Roles seeded"))

            self.stdout.write("Seeding users...")
            User.objects.create_user(
                email="user@example.com", first_name="John", last_name="Doe", password="password123", role=user_role
            )

            User.objects.create_user(
                email="operator@example.com",
                first_name="Jane",
                last_name="Smith",
                password="password123",
                role=operator_role,
            )

            User.objects.create_superuser(
                email="admin@example.com", first_name="Admin", last_name="User", password="password123"
            )
            self.stdout.write(self.style.SUCCESS("Users seeded"))

        self.stdout.write(self.style.SUCCESS("Database seeded successfully"))
