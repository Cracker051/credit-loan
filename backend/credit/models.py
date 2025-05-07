from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from backend.authorize.models import User
from backend.base.const import CreditPlanType


class Budget(models.Model):
    value = models.BigIntegerField()  # Just to mock our storage, storing only one row

    class Meta:
        db_table = "credit_budget"


class CreditPlan(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    bet = models.DecimalField(
        validators=[MinValueValidator(0.1), MaxValueValidator(0.9)], max_digits=2, decimal_places=1
    )
    type = models.CharField(choices=CreditPlanType.choices(), max_length=50)

    class Meta:
        db_table = "credit_creditplan"


class Credit(models.Model):
    value = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    plan = models.ForeignKey(CreditPlan, on_delete=models.PROTECT)
    return_schedule = models.JSONField()

    class Meta:
        db_table = "credit_credit"
