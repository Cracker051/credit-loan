from django.urls import path

from backend.credit.views import (
  CreditPlanListCreateView,
  CreditPlanRetrieveUpdateDestroyView,
  CreditRequestListCreateView,
  CreditRequestRetrieveUpdateDestroyView,
  CreditRequestPortfolioView,
  CreditRequestPortfolioAcceptView,
  CreditRequestPortfolioRejectView,
  TransactionRetrieveUpdateDestroyView,
  CurrentBalanceView
)


urlpatterns = [
  path("plans/", CreditPlanListCreateView.as_view(), name='credit-plan-list-create'),
  path("plans/<int:pk>/", CreditPlanRetrieveUpdateDestroyView.as_view(), name='credit-plan-detail'),
  path("requests/", CreditRequestListCreateView.as_view(), name='credit-request-list-create'),
  path("requests/<int:pk>/", CreditRequestRetrieveUpdateDestroyView.as_view(), name='credit-request-detail'),
  path("requests/portfolio/", CreditRequestPortfolioView.as_view(), name='credit-requests-portfolio'),
  path("requests/portfolio/accept", CreditRequestPortfolioAcceptView.as_view(), name='credit-requests-portfolio-accept'),
  path("requests/portfolio/reject", CreditRequestPortfolioRejectView.as_view(), name='credit-requests-portfolio-reject'),
  path("transactions/<int:pk>/", TransactionRetrieveUpdateDestroyView.as_view(), name='transactions-crud'),
  path("transactions/balance", CurrentBalanceView.as_view(), name='transactions-balance'),
]
