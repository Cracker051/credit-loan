from django.core.management.base import BaseCommand

from backend.authorize.const import RoleChoices
from backend.authorize.models import Role, User


class Command(BaseCommand):
    help = "Seeds the database with initial data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding roles...")

        user_role, _ = Role.objects.get_or_create(name=RoleChoices.USER)
        operator_role, _ = Role.objects.get_or_create(name=RoleChoices.OPERATOR)
        creditor_role, _ = Role.objects.get_or_create(name=RoleChoices.CREDITOR)
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

        User.objects.create_user(
            email="creditor@example.com",
            first_name="Alice",
            last_name="Johnson",
            password="password123",
            role=creditor_role,
        )

        User.objects.create_superuser(
            email="admin@example.com", first_name="Admin", last_name="User", password="password123", role=user_role
        )
        self.stdout.write(self.style.SUCCESS("Users seeded"))

        self.stdout.write(self.style.SUCCESS("Database seeded successfully"))
