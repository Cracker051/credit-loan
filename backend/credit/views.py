from rest_framework.generics import RetrieveUpdateDestroyAPIView

from backend.credit.models import CreditPlan
from backend.credit.serializers import CredinPlanSerializer


class CreditPlanAPIView(RetrieveUpdateDestroyAPIView):
    queryset = CreditPlan.objects.all()
    serializer_class = CredinPlanSerializer
