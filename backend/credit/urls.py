from django.urls import path

from backend.credit.views import (
  CreditPlanListCreateView,
  CreditPlanRetrieveUpdateDestroyView,
  CreditRequestListCreateView,
  CreditRequestRetrieveUpdateDestroyView,
  confirm_portfolio
)


urlpatterns = [
  path("plans/", CreditPlanListCreateView.as_view(), name='credit-plan-list-create'),
  path("plans/<int:pk>/", CreditPlanRetrieveUpdateDestroyView.as_view(), name='credit-plan-detail'),
  path("requests/", CreditRequestListCreateView.as_view(), name='credit-request-list-create'),
  path("requests/<int:pk>/", CreditRequestRetrieveUpdateDestroyView.as_view(), name='credit-request-detail'),
  path("confirm_portfolio/", confirm_portfolio)
]
