from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

import backend.base.const as backend_const
from backend.credit import permissions
from backend.credit.models import CreditPlan, CreditRequest, CreditRequestStatusType, Transaction
from backend.credit.serializers import CreditPlanSerializer, CreditRequestSerializer, TransactionSerializer
from backend.credit.services import CreditRequestPortfolioService


class CreditPlanListCreateView(generics.ListCreateAPIView):
    """
    Отримати список кредитних планів (доступно всім)
    Створити кредитний план (доступно лише staff-користувачам)
    """

    queryset = CreditPlan.objects.all()
    serializer_class = CreditPlanSerializer
    permission_classes = [permissions.IsReadOnlyContent]


class CreditPlanRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Переглянути, змінити або видалити кредитний план
    Зміна і видалення доступно лише staff-користувачам
    Перегляд доступно усім
    """

    queryset = CreditPlan.objects.all()
    serializer_class = CreditPlanSerializer
    permission_classes = [permissions.IsReadOnlyContent]


class CreditRequestListCreateView(generics.ListCreateAPIView):
    """
    Створити кредитний план (доступно лише зареєстрованим користувачам).
    Отримати список кредитних запитів (доступно лише staff-користувачам).
    Можна фільтрувати за статусом: credit/plans/?status=pending
    """

    queryset = CreditRequest.objects.all()
    serializer_class = CreditRequestSerializer
    permission_classes = [permissions.IsUserListContent]

    def get_queryset(self):
        queryset = CreditRequest.objects.all()

        status_param = self.request.query_params.get("status")
        if status_param and not CreditRequestStatusType.is_valid(status_param):
            valid_statuses = CreditRequestStatusType.choices().values()
            raise ValidationError({"status": f"Invalid value. Available: {valid_statuses}"})

        if status_param:
            queryset = queryset.filter(status=status_param)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CreditRequestRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Переглянути, змінити або видалити кредитний план
    Доступно лише автору запиту або staff-користувачам
    """

    queryset = CreditRequest.objects.all()
    serializer_class = CreditRequestSerializer
    permission_classes = [permissions.IsVerifiedUserContent]


class CreditRequestPortfolioView(APIView):
    """
    Обчислити оптимальний портфель кредитів на основі
    кредитних запитів зі статусом `pending`
    Доступно лише staff-користувачам
    """

    permission_classes = [permissions.IsStaffOnlyContent]

    def get(self, request):
        data = CreditRequestPortfolioService().calculate_portfolio()
        return Response(data)


class CreditRequestPortfolioAcceptView(APIView):
    """
    Змінити стан кредитних запитів з оптимального портфеля на `Accepted`,
    а які не ввійшли в портфель -- на `Rejected`
    Доступно лише staff-користувачам
    """

    permission_classes = [permissions.IsStaffOnlyContent]

    def post(self, request):
        service = CreditRequestPortfolioService()
        portfolio = service.calculate_portfolio()
        accepted = []
        rejected = []
        for node in portfolio:
            credit_request_id = node["credit_request_id"]
            credit_request = CreditRequest.objects.get(pk=credit_request_id)
            if node["is_selected"]:
                service.accept(credit_request)
                accepted.append(credit_request_id)
            else:
                credit_request.status = CreditRequestStatusType.REJECTED
                rejected.append(credit_request_id)

            credit_request.save()

        return Response({"accepted": accepted, "rejected": rejected}, status=status.HTTP_200_OK)


class CreditRequestPortfolioRejectView(APIView):
    """
    Змінити статус усіх кредитних запитів зі статусом `Pending` на `Rejected`
    Доступно лише staff-користувачам
    """

    permission_classes = [permissions.IsStaffOnlyContent]

    def post(self, request):
        credit_requests = CreditRequest.objects.filter(status=CreditRequestStatusType.PENDING)
        id_list = []
        for credit_request in credit_requests:
            credit_request.status = CreditRequestStatusType.REJECTED
            id_list.append(credit_request.id)
        return Response({"rejected_credit_request": id_list}, status=status.HTTP_200_OK)


class TransactionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    CRUD операції для транзакцій
    Доступно лише staff-користувачам
    """

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsStaffOnlyContent]


class TransactionsListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsStaffOnlyContent]


class CurrentBalanceView(APIView):
    """
    Отримати поточний баланс (розмі кредитних ресурсів)
    Доступно лише staff-користувачам
    """

    permission_classes = [permissions.IsStaffOnlyContent]

    def get(self, request):
        data = {"balance": Transaction.objects.latest("created_at").balance}
        return Response(data)
