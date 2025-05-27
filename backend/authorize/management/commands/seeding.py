from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from backend.authorize.models import Role, User
from backend.credit.models import CreditPlan, CreditPlanType, TimePeriodType, CreditRequest, Transaction, TransactionType
from backend.base.const import RoleChoices


class Command(BaseCommand):
    help = "Seeds the database with initial data"

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            self.generate_users()
            
            self.stdout.write("Seeding credit plans...")
            CreditPlan.objects.create(
                name="Приклад з лекції",
                description="Неспоживчий кредит з добовою ставкою 0.1%",
                type=CreditPlanType.PURPOSE,
                interest_rate="0.001",
                rate_frequency=TimePeriodType.DAY)
            CreditPlan.objects.create(
                name="Споживчий кредит",
                description="Споживчий кредит з річною ставкою 44.02%",
                type=CreditPlanType.CONSUMER,
                interest_rate="0.4402",
                rate_frequency=TimePeriodType.YEAR)
            self.stdout.write(self.style.SUCCESS("Credit plans seeded"))
            
            self.stdout.write("Seeding credit requests...")
            CreditRequest.objects.create(
                amount=100,
                repayment_period_unit=TimePeriodType.MONTH,
                repayment_period_duration=5,
                repayment_period_start_date=datetime(year=2012, month=9, day=1),
                user=User.objects.get(email="userJohn@example.com"),
                plan=CreditPlan.objects.get(name="Приклад з лекції"),
                return_schedule=[
                    {'amount': 10, 'date': '2012-10-01'},
                    {'amount': 20, 'date': '2012-11-01'},
                    {'amount': 30, 'date': '2012-12-01'},
                    {'amount': 30, 'date': '2013-01-01'}]
            )
            CreditRequest.objects.create(
                amount=200,
                repayment_period_unit=TimePeriodType.MONTH,
                repayment_period_duration=5,
                repayment_period_start_date=datetime(year=2012, month=9, day=1),
                user=User.objects.get(email="userEmily@example.com"),
                plan=CreditPlan.objects.get(name="Приклад з лекції"),
                return_schedule=[
                    {'amount': 20, 'date': '2012-10-01'},
                    {'amount': 40, 'date': '2012-11-01'},
                    {'amount': 60, 'date': '2012-12-01'},
                    {'amount': 60, 'date': '2013-01-01'}]
            )
            CreditRequest.objects.create(
                amount=300,
                repayment_period_unit=TimePeriodType.MONTH,
                repayment_period_duration=5,
                repayment_period_start_date=datetime(year=2012, month=9, day=1),
                user=User.objects.get(email="userLiam@example.com"),
                plan=CreditPlan.objects.get(name="Приклад з лекції"),
                return_schedule=[
                    {'amount': 30, 'date': '2012-10-01'},
                    {'amount': 60, 'date': '2012-11-01'},
                    {'amount': 90, 'date': '2012-12-01'},
                    {'amount': 90, 'date': '2013-01-01'}]
            )
            CreditRequest.objects.create(
                amount=400,
                repayment_period_unit=TimePeriodType.MONTH,
                repayment_period_duration=5,
                repayment_period_start_date=datetime(year=2012, month=9, day=1),
                user=User.objects.get(email="userSophia@example.com"),
                plan=CreditPlan.objects.get(name="Приклад з лекції"),
                return_schedule=[
                    {'amount': 40, 'date': '2012-10-01'},
                    {'amount': 80, 'date': '2012-11-01'},
                    {'amount': 120, 'date': '2012-12-01'},
                    {'amount': 120, 'date': '2013-01-01'}]
            )
            CreditRequest.objects.create(
                amount=500,
                repayment_period_unit=TimePeriodType.MONTH,
                repayment_period_duration=5,
                repayment_period_start_date=datetime(year=2012, month=9, day=1),
                user=User.objects.get(email="userNoah@example.com"),
                plan=CreditPlan.objects.get(name="Приклад з лекції"),
                return_schedule=[
                    {'amount': 50, 'date': '2012-10-01'},
                    {'amount': 100, 'date': '2012-11-01'},
                    {'amount': 150, 'date': '2012-12-01'},
                    {'amount': 150, 'date': '2013-01-01'}]
            )
            self.stdout.write(self.style.SUCCESS("Credit requests seeded"))

            self.stdout.write("Seeding transactions...")
            Transaction.objects.create(amount=1000, type=TransactionType.INCOME, description="Initial balance")
            self.stdout.write(self.style.SUCCESS("Transactions seeded"))

        self.stdout.write(self.style.SUCCESS("Database seeded successfully"))
    
    def generate_users(self):
        self.stdout.write("Seeding roles...")
        user_role, _ = Role.objects.get_or_create(name=RoleChoices.USER)
        operator_role, _ = Role.objects.get_or_create(name=RoleChoices.OPERATOR)
        admin_role, _ = Role.objects.get_or_create(name=RoleChoices.ADMIN)
        self.stdout.write(self.style.SUCCESS("Roles seeded"))

        self.stdout.write("Seeding users...")
        User.objects.create_user(
            email="userJohn@example.com",
            first_name="John",
            last_name="Doe",
            password="password123",
            role=user_role,
            insolvency_probability=0.03)
        User.objects.create_user(
            email="userEmily@example.com",
            first_name="Emily", 
            last_name="Roberts",
            password="password123",
            role=user_role,
            insolvency_probability=0.05)
        User.objects.create_user(
            email="userLiam@example.com",
            first_name="Liam", 
            last_name="Walker",
            password="password123",
            role=user_role,
            insolvency_probability=0.02)
        User.objects.create_user(
            email="userSophia@example.com",
            first_name="Sophia", 
            last_name="Turner",
            password="password123",
            role=user_role,
            insolvency_probability=0.01)
        User.objects.create_user(
            email="userNoah@example.com",
            first_name="Noah", 
            last_name="Bennett",
            password="password123",
            role=user_role,
            insolvency_probability=0.04)

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

