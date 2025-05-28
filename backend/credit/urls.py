from django.urls import path

from backend.credit import views


urlpatterns = [
    path("plans/", views.CreditPlanListCreateView.as_view(), name="credit-plan-list-create"),
    path("plans/<int:pk>/", views.CreditPlanRetrieveUpdateDestroyView.as_view(), name="credit-plan-detail"),
    path("requests/", views.CreditRequestListCreateView.as_view(), name="credit-request-list-create"),
    path("requests/<int:pk>/", views.CreditRequestRetrieveUpdateDestroyView.as_view(), name="credit-request-detail"),
    path("requests/portfolio/", views.CreditRequestPortfolioView.as_view(), name="credit-requests-portfolio"),
    path(
        "requests/portfolio/non-deterministic",
        views.CreditRequestPortfolioStochasticView.as_view(),
        name="credit-requests-portfolio-non-deterministic"),
    path(
        "requests/portfolio/accept",
        views.CreditRequestPortfolioAcceptView.as_view(),
        name="credit-requests-portfolio-accept",
    ),
    path(
        "requests/portfolio/reject",
        views.CreditRequestPortfolioRejectView.as_view(),
        name="credit-requests-portfolio-reject",
    ),
    path("transactions/<int:pk>/", views.TransactionRetrieveUpdateDestroyView.as_view(), name="transactions-crud"),
    path("transactions/", views.TransactionsListCreateView.as_view(), name="transactions-crud"),
    path("transactions/balance", views.CurrentBalanceView.as_view(), name="transactions-balance"),
]
