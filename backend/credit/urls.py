from django.urls import path

from backend.credit.views import CreditPlanAPIView


urlpatterns = [path("credit-plan/", CreditPlanAPIView.as_view())]
