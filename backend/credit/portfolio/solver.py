from .credit_requests import BaseCreditRequest, ArtificialCreditRequest
from typing import Iterable
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, PULP_CBC_CMD

def find_optimal_portfolio(credit_requests: Iterable[BaseCreditRequest], available_resources: float, pulp_logs: bool = False) -> tuple[LpProblem, tuple[bool]]:
  model = LpProblem("Binary_Optimization", LpMaximize)
  n = len(credit_requests)
  x = [LpVariable(f"x{i}", cat="Binary") for i in range(n)]
  model += lpSum(x[i] * credit_requests[i].compute_income() for i in range(n)), "Maximize_Sum"
  model += lpSum(x[i] * credit_requests[i].amount for i in range(n)) <= available_resources
  model.solve(PULP_CBC_CMD(msg=pulp_logs))
  return model, tuple(x[i].varValue for i in range(n))


def run_test(
    credit_requests: tuple[BaseCreditRequest],
    available_resources: float,
    expected_result: tuple[bool]):
  print("  Кредитні запити:")
  for i, credit_request in enumerate(credit_requests):
    print(f"    Запит №{i + 1}:")
    print(f"      Розмір позики: {credit_request.amount}")
    print(f"      Чистий зведений дохід: {credit_request.compute_income()}")

  print("  Кредитні ресурси:", available_resources)
  model, selected_requests = find_optimal_portfolio(credit_requests, available_resources)
  print("  Розрахований портфель кредитів:", selected_requests)
  print("  Очікуваний портфель кредитів:", expected_result)
  print("  Оптимальне значення функції:", round(model.objective.value(), 4))


if __name__ == "__main__":
  print("Тест №1:")
  credit_requests = (
    ArtificialCreditRequest(200, 100),
    ArtificialCreditRequest(200, 150),
    ArtificialCreditRequest(300, 150),
    ArtificialCreditRequest(300, 200),
  )
  available_resources = sum([request.compute_income() for request in credit_requests])
  expected_result = tuple(1.0 for _ in range(len(credit_requests)))
  run_test(credit_requests, available_resources, expected_result)

  print("Тест №2:")
  available_resources = 800
  expected_result = (0.0, 1.0, 1.0, 1.0)
  run_test(credit_requests, available_resources, expected_result)
  
  print("Тест №3:")
  available_resources = 500
  expected_result = (0.0, 1.0, 0.0, 1.0)
  run_test(credit_requests, available_resources, expected_result)
  
  print("Тест №4:")
  available_resources = 400
  expected_result = (1.0, 1.0, 0.0, 0.0)
  run_test(credit_requests, available_resources, expected_result)

  print("Тест №5:")
  credit_requests = (
    ArtificialCreditRequest(100, 16.19),
    ArtificialCreditRequest(300, 48.57),
    ArtificialCreditRequest(200, 32.38),
    ArtificialCreditRequest(400, 64.76),
    ArtificialCreditRequest(500, 80.95),
  )
  available_resources = 1000
  expected_result = (1.0, 1.0, 1.0, 1.0, 0.0)
  run_test(credit_requests, available_resources, expected_result)
