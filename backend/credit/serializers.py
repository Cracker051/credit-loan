from rest_framework import serializers

from backend.credit.models import CreditPlan, CreditRequest


class CreditPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditPlan
        exclude = ["id"]


class CreditRequestSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')
    plan_name = serializers.ReadOnlyField(source='plan.name')

    class Meta:
        model = CreditRequest
        exclude = ["id"]
