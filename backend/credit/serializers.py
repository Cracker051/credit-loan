from rest_framework import serializers

from backend.credit.models import CreditPlan


class CredinPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditPlan
        exclude = ["id"]
