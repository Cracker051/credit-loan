from credit_requests import NonConsumerCreditRequest
from data_types import Rate, TimePeriodType, TimePeriod, Payment
from datetime import datetime
from loan_portfolio import find_optimal_loan_portfolio
from typing import Iterable


def get_non_consumer_credit_request() -> Iterable[NonConsumerCreditRequest]:
  credit_requests = []
  rate = Rate(0.001, TimePeriodType.DAY)
  repayment_period = TimePeriod(TimePeriodType.MONTH, 5, datetime(2012, 9, 1))
  payments = (
    Payment(10, datetime(2012, 10, 1)),
    Payment(20, datetime(2012, 11, 1)),
    Payment(30, datetime(2012, 12, 1)),
    Payment(30, datetime(2013, 1, 1))
  )
  credit_requests.append(NonConsumerCreditRequest(100, rate, repayment_period, payments))
  payments = (
    Payment(20, datetime(2012, 10, 1)),
    Payment(40, datetime(2012, 11, 1)),
    Payment(60, datetime(2012, 12, 1)),
    Payment(60, datetime(2013, 1, 1))
  )
  credit_requests.append(NonConsumerCreditRequest(200, rate, repayment_period, payments))
  payments = (
    Payment(30, datetime(2012, 10, 1)),
    Payment(60, datetime(2012, 11, 1)),
    Payment(90, datetime(2012, 12, 1)),
    Payment(90, datetime(2013, 1, 1))
  )
  credit_requests.append(NonConsumerCreditRequest(300, rate, repayment_period, payments))
  payments = (
    Payment(40, datetime(2012, 10, 1)),
    Payment(80, datetime(2012, 11, 1)),
    Payment(120, datetime(2012, 12, 1)),
    Payment(120, datetime(2013, 1, 1))
  )
  credit_requests.append(NonConsumerCreditRequest(400, rate, repayment_period, payments))
  payments = (
    Payment(50, datetime(2012, 10, 1)),
    Payment(100, datetime(2012, 11, 1)),
    Payment(150, datetime(2012, 12, 1)),
    Payment(150, datetime(2013, 1, 1))
  )
  credit_requests.append(NonConsumerCreditRequest(500, rate, repayment_period, payments))
  return credit_requests


def test_last_payment(credit_requests: Iterable[NonConsumerCreditRequest]):
  print("Виконується тест розрахунку останнього платежу "
        "для кредитних запитів з прикладу в лекції")
  print("Кількість кредитних запитів:", len(credit_requests))
  print("Інформація про кредитні запити:")
  for request in credit_requests:
    request.print()
  
  print("Тест розрахунку останнього платежу для кожного кредитного запиту:")
  for idx, request in enumerate(credit_requests):
    last_payment: Payment = request.calc_last_payment(print=True)
    print(f"Останній платіж для кредитного запиту №{idx + 1}:", last_payment)


def test_income(credit_requests: Iterable[NonConsumerCreditRequest]):
  print("Виконується тест розрахунку прибутку для кредитних запитів з прикладу в лекції")
  print("Кількість кредитних запитів:", len(credit_requests))
  print("Інформація про кредитні запити:")
  for request in credit_requests:
    request.print()
  
  print("Тест розрахунку доходу для кожного кредитного запиту:")
  for idx, request in enumerate(credit_requests):
    print(f"Прибуток з кредитного запиту №{idx + 1}:", request.compute_income())


def test_solver(credit_requests: Iterable[NonConsumerCreditRequest]):
  print("Кількість запитів:", len(credit_requests))
  print("Інформація про запити:")
  for request in credit_requests:
    request.print()
  
  available_resources = 1000
  print("Кредитні ресурси:", available_resources)
  print("Обчислення оптимального портфелю кредитів...")
  model, selected_requests = find_optimal_loan_portfolio(credit_requests, available_resources)
  print("Оптимальний портфель кредитів:")
  for idx in range(len(selected_requests)):
    is_selected = selected_requests[idx]
    is_selected_str = "прийняти" if is_selected else "відхилити" 
    print(f"  Кредитний запит №{idx + 1}: {is_selected_str}")
  
  total_income = round(model.objective.value(), 4)
  print("Загальний прибуток з усіх прийнятих кредитів:", total_income)


if __name__ == "__main__":
  options = (
    "Розрахунок останнього платежу для кредитних запитів з прикладу в лекції",
    "Розрахунок прибутку з кожного кредитного запиту з прикладу в лекції",
    "Розв'язання задачі формування портфелю кредитів на основі неспожичних кредитів з прикладу в лекції",    
    "Усі сценарії"
  )
  print("Сценарії тестування:")
  for i, option in enumerate(options):
    print(f"  {i + 1}. {option}")
  
  option = input(f"Виберіть сценарій тестування (введіть число від 1 до {len(options)}): ")
  option = int(option)
  credit_requests = get_non_consumer_credit_request()
  match option:
    case 1:
      test_last_payment(credit_requests)
    case 2:
      test_income(credit_requests)
    case 3:
      test_solver(credit_requests)
    case 4:
      test_last_payment(credit_requests)
      test_income(credit_requests)
      test_solver(credit_requests)
