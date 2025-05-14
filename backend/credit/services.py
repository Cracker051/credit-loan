import backend.base.const as backend_const

from django.utils import timezone

from backend.credit.models import CreditPlanType, CreditRequest, CreditRequestStatusType, Transaction
from backend.credit.portfolio.solver import find_optimal_portfolio
from backend.credit.portfolio.credit_requests import BaseCreditRequest, NonConsumerCreditRequest
from backend.credit.portfolio.data_types import Rate, TimePeriod, TimePeriodType, Payment

from datetime import datetime
from typing import Iterable

class CreditRequestPortfolioService:
  def calculate_portfolio(self):
    credit_requests = CreditRequest.objects.filter(status=CreditRequestStatusType.PENDING)
    result = []
    if len(credit_requests) == 0:
      print("No credit requests with status 'pending'")
      return result
    
    converted = self.convert_requests_set(credit_requests)
    balance = Transaction.objects.latest("created_at").balance
    print("Balance:", balance)
    print("Count of credit requests:", len(converted))
    print("Calculating the optimal portfolio...")
    model, selected_requests = find_optimal_portfolio(converted, float(balance))
    print("Done")
    print("Selected requests:", selected_requests)
    print("Total income:", round(model.objective.value(), 4))
    
    for idx, request in enumerate(credit_requests):
      result.append({"credit_request_id": request.id, "is_selected": selected_requests[idx]})
    return result

  def convert_requests_set(self, models: Iterable[CreditRequest]) -> Iterable[BaseCreditRequest]:
    return tuple(self.convert_credit_request(model) for model in models)

  def convert_credit_request(self, model: CreditRequest) -> BaseCreditRequest:
    if model.plan.type == CreditPlanType.PURPOSE:
      rate_frequency = self.to_time_period_type(model.plan.rate_frequency)
      rate = Rate(float(model.plan.interest_rate), rate_frequency)
      unit = self.to_time_period_type(model.repayment_period_unit)
      repayment_period = TimePeriod(unit, model.repayment_period_duration,
        model.repayment_period_start_date)
      if not isinstance(model.return_schedule, list):
        raise ValueError("return_schedule is not a list")

      payments = []
      for item in model.return_schedule:
        naive_dt = datetime.strptime(item["date"], '%Y-%m-%d')
        date = timezone.make_aware(naive_dt)
        payment = Payment(item["amount"], date)
        payments.append(payment)

      return NonConsumerCreditRequest(
        float(model.amount), rate, repayment_period, payments)
    elif model.plan.type == CreditPlanType.CONSUMER:
      # TODO
      pass
    else:
      raise ValueError(f"Unexpected type of CreditPlan ({model.plan.type})")

  def to_time_period_type(self, choice: str) -> TimePeriodType:
    match choice:
      case backend_const.TimePeriodType.DAY:
        return TimePeriodType.DAY
      case backend_const.TimePeriodType.MONTH:
        return TimePeriodType.MONTH
      case backend_const.TimePeriodType.QUARTER:
        return TimePeriodType.QUARTER
      case backend_const.TimePeriodType.YEAR:
        return TimePeriodType.YEAR
    
    raise ValueError(f"Failed to convert '{choice}' to TimePeriodType")

  def accept(self, credit_request: CreditRequest) -> None:
    transaction = Transaction.objects.create(
      amount=credit_request.amount,
      type=backend_const.TransactionType.OUTCOME,
      description=f"CreditRequest<id: {credit_request.id}>")
    transaction.save()
    credit_request.status = CreditRequestStatusType.ACCEPTED
