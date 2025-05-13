import backend.base.const as backend_const

from rest_framework import generics
from rest_framework.exceptions import ValidationError 
from django.http import JsonResponse
from django.core import serializers

from backend.credit.models import CreditPlan, CreditPlanType, CreditRequest, CreditRequestStatusType, Transaction
from backend.credit.serializers import CreditPlanSerializer, CreditRequestSerializer
from backend.credit.permissions import IsVerifiedUserContent, IsReadOnlyContent

from backend.credit.portfolio.solver import find_optimal_portfolio
from backend.credit.portfolio.credit_requests import BaseCreditRequest, NonConsumerCreditRequest
from backend.credit.portfolio.data_types import Rate, TimePeriod, TimePeriodType, Payment
from typing import Iterable
from functools import singledispatchmethod


class CreditPlanListCreateView(generics.ListCreateAPIView):
    """
    Отримати список кредитних планів (доступно всім)
    Створити кредитний план (доступно лише staff-користувачам)
    """
    queryset = CreditPlan.objects.all()
    serializer_class = CreditPlanSerializer
    permission_classes = [IsReadOnlyContent]


class CreditPlanRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Переглянути, змінити або видалити кредитний план
    Зміна і видалення доступно лише staff-користувачам
    Перегляд доступно усім
    """
    queryset = CreditPlan.objects.all()
    serializer_class = CreditPlanSerializer
    permission_classes = [IsReadOnlyContent]


class CreditRequestListCreateView(generics.ListCreateAPIView):
    """
    Створити кредитний план (доступно лише зареєстрованим користувачам).
    Отримати список кредитних запитів (доступно лише staff-користувачам).
    Можна фільтрувати за статусом: credit/plans/?status=pending
    """
    queryset = CreditRequest.objects.all()
    serializer_class = CreditRequestSerializer
    permission_classes = [IsVerifiedUserContent]

    def get_queryset(self):
        queryset = CreditRequest.objects.all()

        status_param = self.request.query_params.get('status')
        if status_param and not CreditRequestStatusType.is_valid(status_param):
            valid_statuses = CreditRequestStatusType.choices().values()
            raise ValidationError({'status': f"Invalid value. Available: {valid_statuses}"})
        
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
    permission_classes = [IsVerifiedUserContent]


# def credit_plans_list(request):
#     if request.method == 'GET':
#         credit_plans_list = CreditPlan.objects.all()
#         data = serializers.serialize('json', credit_plans_list)
#         return JsonResponse(data, safe=False)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)
    

# @non_public_content
# def credit_requests_list(request):
#     if request.method != 'GET':
#         return JsonResponse({'error': 'Method not allowed'}, status=405)

#     status = request.GET.get('status')
#     if CreditRequestStatusType.is_valid(status):
#         request_list = CreditRequest.objects.filter(status=status)
#     else:
#         request_list = CreditRequest.objects.all()
#         if status:
#             print(f"WARN: {status} is not a valid credit status")
            
#     # TODO: test
#     data = serializers.serialize('json', request_list)
#     return JsonResponse(data, safe=False)


@singledispatchmethod
def convert(models: Iterable[CreditRequest]) -> Iterable[BaseCreditRequest]:
    return tuple(convert(model) for model in models)


@convert.register
def convert(model: CreditRequest) -> BaseCreditRequest:
    if model.plan.type == CreditPlanType.PURPOSE:
        rate_frequency = to_time_period_type(model.plan.rate_frequency)
        rate = Rate(model.plan.interest_rate, rate_frequency)
        unit = to_time_period_type(model.repayment_period_unit)
        repayment_period = TimePeriod(unit, model.repayment_period_duration,
            model.repayment_period_start_date)
        if not isinstance(model.return_schedule, list):
            raise ValueError("return_schedule is not a list")

        payments = []
        for item in model.return_schedule:
            payment = Payment(item["amount"], item["date"])
            payments.append(payment)

        return NonConsumerCreditRequest(
            model.amount, rate, repayment_period, payments)
    elif model.plan.type == CreditPlanType.CONSUMER:
        # TODO
        pass
    else:
        print(f"ERROR: unexpected type of CreditPlan({model.plan.type})")
        return None


def to_time_period_type(choice: str) -> TimePeriodType:
    match choice:
        case backend_const.TimePeriodType.DAY:
            return TimePeriodType.DAY
        case backend_const.TimePeriodType.MONTH:
            return TimePeriodType.MONTH
        case backend_const.TimePeriodType.QUARTER:
            return TimePeriodType.QUARTER
        case backend_const.TimePeriodType.YEAR:
            return TimePeriodType.YEAR
    
    print(f"ERROR: failed to convert '{choice}' to TimePeriodType")
    return None

def get_portfolio(credit_requests: Iterable[CreditRequest]) -> tuple[bool]:
    converted = convert(credit_requests)
    balance = Transaction.objects.latest("created_at").balance
    print("Balance:", balance)
    print("Count of credit requests:", len(converted))
    print("Calculating the optimal portfolio...")
    model, selected_requests = find_optimal_portfolio(converted, balance)
    print("Done")
    print("Selected requests:", selected_requests)
    print("Total income:", round(model.objective.value(), 4))
    return selected_requests
    

# TODO: user access
# TODO: test
def process_credit_requests(request):
    if request.method != 'GET':
        print("Method of request is not GET")
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    credit_requests = CreditRequest.objects.filter(status=CreditRequestStatusType.PENDING)
    if not credit_requests.exists():
        print("There are no requests with pending status")
        return JsonResponse({
            'items': [],
            'message': 'No credit requests found with the status "pending"'
        }, status=200)
    
    portfolio = get_portfolio(credit_requests)
    data = serializers.serialize('json', credit_requests)
    for item, i in enumerate(data):
        item["portfolio"] = portfolio[i]
    
    return data


# TODO: test
# TODO: reject all feature, if false are in params  
def confirm_portfolio(request):
    credit_requests = CreditRequest.objects.filter(status=CreditRequestStatusType.PENDING)
    if not credit_requests.exists():
        print("There are no requests with pending status")
        return JsonResponse({
            'items': [],
            'message': 'No credit requests found with the status "pending"'
        }, status=200)
    
    portfolio = get_portfolio(credit_requests)
    for credit_request, idx in enumerate(credit_requests):
        result = CreditRequestStatusType.ACCEPTED if portfolio[idx] else CreditRequestStatusType.REJECTED
        print(f"Status of CreditRequest<px={credit_request.pk}>: {result}")
        
        # Поміняти статуси оптимальних рекветів на апрувнуті,
        # а не оптимальні відхилити
        # *оновити баланс

    return JsonResponse({
        'items': [],
        'message': 'No credit requests found with the status "pending"'
    }, status=200)
