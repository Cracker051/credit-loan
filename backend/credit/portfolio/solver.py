from .credit_requests import BaseCreditRequest, ArtificialCreditRequest
# from credit_requests import BaseCreditRequest, ArtificialCreditRequest
from typing import Iterable, Union
import numpy as np
import cvxpy as cp
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, PULP_CBC_CMD


def find_deterministic_optimal_portfolio(credit_requests: Iterable[BaseCreditRequest], available_resources: float, pulp_logs: bool = False) -> tuple[LpProblem, tuple[bool]]:
    model = LpProblem("Binary_Optimization", LpMaximize)
    n = len(credit_requests)
    x = [LpVariable(f"x{i}", cat="Binary") for i in range(n)]
    model += lpSum(x[i] * credit_requests[i].compute_income() for i in range(n)), "Maximize_Sum"
    model += lpSum(x[i] * credit_requests[i].amount for i in range(n)) <= available_resources
    model.solve(PULP_CBC_CMD(msg=pulp_logs))
    return model, tuple(x[i].varValue for i in range(n))


def find_stochastic_optimal_portfolio(credit_requests: Iterable[BaseCreditRequest], available_resources: float, pulp_logs: bool = False, k: float = 0, corr_matrix: Union[None, np.ndarray[float]] = None, insolvency_probs: Union[np.ndarray, None] = None) -> tuple[LpProblem, tuple[bool]]:
    if corr_matrix is None:
       corr_matrix = np.eye((len(credit_requests), len(credit_requests)))
    else:
       assert isinstance(corr_matrix, np.ndarray), "Type of correlation matrix should be numpy.ndarray"
       assert corr_matrix.shape == (len(credit_requests), len(credit_requests)), "Correlation matrix should be N x N, where N is the number of credit requests"

    if insolvency_probs is None:
       insolvency_probs = np.zeros((len(credit_requests), 1))
    else: 
        assert isinstance(insolvency_probs, np.ndarray), "Type of insolvency probabilities should be numpy.ndarray"
        assert insolvency_probs.shape == (len(credit_requests),)

    n = len(credit_requests)
    x = cp.Variable(n, boolean=True)

    profit = np.array([
        credit_requests[i].compute_income() * (1 - insolvency_probs[i]) -
        2 * credit_requests[i].amount * insolvency_probs[i]
        for i in range(n)
    ])
    print(profit)
    Q = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            Q[i, j] = corr_matrix[i, j] * \
                      credit_requests[i].compute_income() * \
                      credit_requests[j].compute_income() * \
                      np.sqrt(insolvency_probs[i] * (1 - insolvency_probs[i])) * \
                      np.sqrt(insolvency_probs[j] * (1 - insolvency_probs[j]))

    objective = cp.Maximize(profit.T @ x - k * cp.quad_form(x, Q))

    total_amount = np.array([req.amount for req in credit_requests])
    constraints = [total_amount.T @ x <= available_resources]

    problem = cp.Problem(objective, constraints)
    problem.solve(solver=cp.ECOS_BB)

    return problem, tuple(map(lambda x: float(round(x, 1)), x.value))


def find_optimal_portfolio(credit_requests: Iterable[BaseCreditRequest], available_resources: float, pulp_logs: bool = False, k: float = 0, corr_matrix: Union[None, np.ndarray[float]] = None, insolvency_probs: Union[np.ndarray, None] = None, stochastic: bool = False) -> tuple[LpProblem, tuple[bool]]:
    deterministic_res = find_deterministic_optimal_portfolio(credit_requests, available_resources, pulp_logs)
    stochastic_res = find_stochastic_optimal_portfolio(credit_requests, available_resources, pulp_logs, k, corr_matrix, insolvency_probs)
    if stochastic:
        return deterministic_res, stochastic_res
    else:
       return deterministic_res


# def find_optimal_portfolio(credit_requests: Iterable[BaseCreditRequest], available_resources: float, pulp_logs: bool = False) -> tuple[LpProblem, tuple[bool]]:
#     model = LpProblem("Binary_Optimization", LpMaximize)
#     n = len(credit_requests)
#     x = [LpVariable(f"x{i}", cat="Binary") for i in range(n)]
#     model += lpSum(x[i] * credit_requests[i].compute_income() for i in range(n)), "Maximize_Sum"
#     model += lpSum(x[i] * credit_requests[i].amount for i in range(n)) <= available_resources
#     model.solve(PULP_CBC_CMD(msg=pulp_logs))
#     return model, tuple(x[i].varValue for i in range(n))


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

def run_stochastic_test(
    credit_requests: tuple[BaseCreditRequest],
    available_resources: float,
    expected_result: tuple[bool],
    k: float,
    corr_mat: np.ndarray,
    insolvency_probs: np.ndarray):
  print("  Кредитні запити:")
  for i, credit_request in enumerate(credit_requests):
    print(f"    Запит №{i + 1}:")
    print(f"      Розмір позики: {credit_request.amount}")
    print(f"      Чистий зведений дохід: {credit_request.compute_income()}")

  print("  Кредитні ресурси:", available_resources)
  det_res, stoch_res = find_optimal_portfolio(credit_requests, available_resources, k=k, corr_matrix=corr_mat, insolvency_probs=insolvency_probs, stochastic=True)
  model, selected_requests = det_res
  print("  Детерміністичний випадок")
  print("  Розрахований портфель кредитів:", selected_requests)
  print("  Очікуваний портфель кредитів:", expected_result)
  print("  Оптимальне значення функції:", round(model.objective.value(), 4))

  print("  Стохастичний випадок")
  model, selected_requests = stoch_res
  print("  Детерміністичний випадок")
  print("  Розрахований портфель кредитів:", selected_requests)
  print("  Очікуваний портфель кредитів:", expected_result)
  print("  Оптимальне значення функції:", round(model.objective.value, 4))


if __name__ == "__main__":
  print("Тест №1:")
  credit_requests = (
    ArtificialCreditRequest(200, 100),
    ArtificialCreditRequest(200, 150),
    ArtificialCreditRequest(300, 150),
    ArtificialCreditRequest(300, 200),
  )
  available_resources = sum([request.amount for request in credit_requests])
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

  print("Тест №6:")
  credit_requests = (
    ArtificialCreditRequest(100, 16.19),
    ArtificialCreditRequest(200, 32.38),
    ArtificialCreditRequest(300, 48.57),
    ArtificialCreditRequest(400, 64.76),
    ArtificialCreditRequest(500, 80.95),
  )
  available_resources = 1000
  k = 0.05
  insolvency_probs = np.array([0.03, 0.05, 0.02, 0.01, 0.04])
  corr_mat = np.array([[1, 0.7, -0.1, 0, 0.3],
                      [0.7, 1, 0, 0, 0.1],
                      [-0.1, 0, 1, -0.2, -0.1],
                      [0, 0, -0.2, 1, 0.1],
                      [0.3, 0.1, -0.1, 0.1, 1]])
  
  expected_result = (1.0, 1.0, 1.0, 1.0, 0.0)
  run_stochastic_test(credit_requests, available_resources, expected_result, k, corr_mat, insolvency_probs)