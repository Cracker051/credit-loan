from rest_framework import serializers

from backend.credit.models import CreditPlan, CreditRequest, Transaction


class CreditPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditPlan
        exclude = []


class CreditRequestSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')
    plan_name = serializers.ReadOnlyField(source='plan.name')

    class Meta:
        model = CreditRequest
        exclude = []


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = []
