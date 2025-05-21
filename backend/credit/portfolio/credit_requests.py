from abc import ABC, abstractmethod
from .data_types import TimePeriod, Payment, Rate
from .utils import calc_duration, to_plural_str


class BaseCreditRequest(ABC):
  def __init__(self, amount: float, rate: Rate, repayment_period: TimePeriod):
    if amount <= 0:
      raise ValueError("Розмір позики має бути додатнім числом")
    
    if repayment_period.convert(rate.frequency) == 0:
      raise ValueError("Частота кредитної ставки не коректна")
    
    self.amount = amount
    self.rate = rate
    self.repayment_period = repayment_period
  
  @abstractmethod
  def compute_income(self) -> float:
    pass
  
  @abstractmethod
  def print(self):
    pass


class ArtificialCreditRequest(BaseCreditRequest):
  def __init__(self, amount: float, income: float):
    if amount <= 0:
      raise ValueError("Розмір позики має бути додатнім числом")
    
    if income <= 0:
      raise ValueError("Число доходу повинно бути додатнім")
    
    self.amount = amount
    self.income = income
  
  def __str__(self):
    return f"ArtificialCreditRequest<розмір позики: {self.amount}, дохід: {self.amount}>"

  def compute_income(self) -> float:
    return self.income
  
  def print(self):
    return print(self)


class NonConsumerCreditRequest(BaseCreditRequest):
  def __init__(self, amount: float, rate: Rate, repayment_period: TimePeriod, payments: tuple[Payment]):
    super().__init__(amount, rate, repayment_period)

    start_date = repayment_period.start_date
    end_date = repayment_period.get_end_date()
    for idx, payment in enumerate(payments):
      if payment.date <= start_date or payment.date >= end_date:
        raise ValueError(f"Дата платежу №{idx + 1} поза періодом виплати кредиту")
      
    # TODO: payments dates should be from the oldest to the newest

    self.payments = payments
  
  def __str__(self):
    payments_str = ", ".join(tuple(str(p) for p in self.payments))
    fields = (
      f"розмір позики: {self.amount}",
      f"ставка дисконту: {self.rate}",
      f"період виплати кредиту: {self.repayment_period}",
      f"графік платежів: [{payments_str}]",
    )
    return f"NonConsumerCreditRequest<{', '.join(fields)}>"
  
  def print(self):
    return print(self)

  def calc_last_payment(self, print: bool = False) -> Payment:
    if print:
      return self.calc_last_payment_print()

    cumulative_amount = self.amount
    for payment in self.payments:
      duration = calc_duration(self.repayment_period.start_date, payment.date, self.rate.frequency)
      cumulative_amount *= (1 + self.rate.value) ** duration
      cumulative_amount -= payment.amount

    duration = calc_duration(self.repayment_period.start_date,
                             self.repayment_period.get_end_date(),
                             self.rate.frequency)
    cumulative_amount *= (1 + self.rate.value) ** duration
    return Payment(cumulative_amount, self.repayment_period.get_end_date())

  def calc_last_payment_print(self) -> Payment:
    print("Розпочато розрахунок останнього платежу")
    print("Розмір позики:", self.amount)
    cumulative_amount = self.amount
    for idx, payment in enumerate(self.payments):
      print(f"{payment} з індексом {idx}:")
      duration = calc_duration(self.repayment_period.start_date, payment.date, self.rate.frequency)
      plural_str = to_plural_str(self.rate.frequency)
      print(f"  Проміжок часу між датою платежу та датою взяття позики ({plural_str}):", duration)
      cumulative_amount *= (1 + self.rate.value) ** duration
      print("  Накопичена сума:", cumulative_amount)
      cumulative_amount -= payment.amount
      print("  Різниця накопиченої суми та суми платежу:", cumulative_amount)

    duration = calc_duration(self.repayment_period.start_date,
                             self.repayment_period.get_end_date(),
                             self.rate.frequency)
    print(f"  Проміжок часу між кінцевою та початковою датами виплати кредиту ({plural_str}):", duration)
    cumulative_amount *= (1 + self.rate.value) ** duration
    print("  Накопичена сума:", cumulative_amount)

    print("Розрахунок останнього платежу завершено")
    return Payment(cumulative_amount, self.repayment_period.get_end_date())
  
  def compute_income(self) -> float:
    d = -self.amount
    for payment in self.payments:
      duration = calc_duration(self.repayment_period.start_date, payment.date, self.rate.frequency)
      d += payment.amount / ((1 + self.rate.value) ** duration)
    
    last_payment = self.calc_last_payment()
    duration = calc_duration(self.repayment_period.start_date, last_payment.date, self.rate.frequency)
    d += last_payment.amount / ((1 + self.rate.value) ** duration)
    return d


class ConsumerCreditRequest(BaseCreditRequest):
  def __init__(self, amount: float, rate: Rate, repayment_period: TimePeriod):
    super().__init__(amount, rate, repayment_period)
    
  def __str__(self):
    fields = (
      f"розмір позики: {self.amount}",
      f"ставка дисконту: {self.rate}",
      f"період виплати кредиту: {self.repayment_period}",
    )
    return f"ConsumerCreditRequest<{', '.join(fields)}>"
  
  def print(self):
    return print(self)

  def compute_income(self) -> float:
    d = -self.amount
    duration = calc_duration(self.repayment_period.start_date, self.repayment_period.get_end_date(), self.rate.frequency)
    d += self.amount * ((1 + self.rate.value) ** duration)
    return d
