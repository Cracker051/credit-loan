from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from decimal import Decimal

from backend.authorize.models import User
from backend.base.const import CreditPlanType, TimePeriodType, TransactionType, CreditRequestStatusType


class Transaction(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=7, choices=TransactionType.choices)
    balance = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            last_transaction = Transaction.objects.order_by('-created_at').first()
            previous_balance = last_transaction.balance if last_transaction else Decimal('0.00')

            if self.type == TransactionType.INCOME:
                self.balance = previous_balance + self.amount
            elif self.type == TransactionType.OUTCOME:
                self.balance = previous_balance - self.amount
        super().save(*args, **kwargs)

    class Meta:
        db_table = "credit_transaction"


class CreditPlan(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    type = models.CharField(choices=CreditPlanType.choices(), max_length=50)
    interest_rate = models.DecimalField(
        validators=[MinValueValidator(0.0001), MaxValueValidator(0.9999)],
        max_digits=5,
        decimal_places=4,
        default=Decimal('0.00')
    )
    rate_frequency = models.CharField(choices=TimePeriodType.choices(), max_length=10, default="year")

    class Meta:
        db_table = "credit_creditplan"


class CreditRequest(models.Model):
    amount = models.BigIntegerField()
    repayment_period_unit = models.CharField(
        choices=TimePeriodType.choices(),
        max_length=10,
        default="year"
    )
    repayment_period_duration = models.IntegerField(validators=[MinValueValidator(0)])
    repayment_period_start_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    plan = models.ForeignKey(CreditPlan, on_delete=models.PROTECT)
    status = models.CharField(
        choices=CreditRequestStatusType.choices(),
        max_length=10,
        default=CreditRequestStatusType.PENDING
    )
    return_schedule = models.JSONField()

    class Meta:
        db_table = "credit_creditrequest"
