from dataclasses import dataclass
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .utils import calc_duration, TimePeriodType
# from utils import calc_duration, TimePeriodType


@dataclass(frozen=True)
class TimePeriod:
  unit: TimePeriodType
  duration: int
  start_date: datetime

  def __post_init__(self):
    if self.duration <= 0:
      raise ValueError("Тривалість часового періоду не може бути від’ємною")
    
  def get_end_date(self) -> datetime:
    match self.unit:
      case TimePeriodType.DAY:
        return self.start_date + relativedelta(days=self.duration)
      case TimePeriodType.MONTH:
        return self.start_date + relativedelta(months=self.duration)
      case TimePeriodType.QUARTER:
        return self.start_date + relativedelta(months=self.duration * 3)
      case TimePeriodType.YEAR:
        return self.start_date + relativedelta(years=self.duration)
  
  def to_days(self) -> int:
    return (self.get_end_date() - self.start_date).days
  
  def get_relative_delta(self) -> int:
    return relativedelta(self.get_end_date(), self.start_date)
  
  def convert(self, conversion_type: TimePeriodType) -> int:
    return calc_duration(self.start_date, self.get_end_date(), conversion_type)
  
  def __str__(self) -> str:
    start_date_str = self.start_date.strftime("%d.%m.%Y")
    format_str = f"TimePeriod<кількість %s: {self.duration}, початкова дата: {start_date_str}>"
    match self.unit:
      case TimePeriodType.DAY:
        return format_str % "днів"
      case TimePeriodType.MONTH:
        return format_str % "місяців"
      case TimePeriodType.QUARTER:
        return format_str % "кварталів"
      case TimePeriodType.YEAR:
        return format_str % "років"
        

@dataclass(frozen=True)
class Payment:
  amount: float
  date: datetime
  
  def __post_init__(self):
    if self.amount <= 0:
      raise ValueError("Сума платежу не може бути від’ємною")
    
  def __str__(self):
    date_str = self.date.strftime("%d.%m.%Y")
    return f"Payment<дата: {date_str}, сума: {self.amount}>"


@dataclass(frozen=True)
class Rate:
  value: float
  frequency: TimePeriodType
  
  def __post_init__(self):
    if self.value <= 0 or self.value >= 1:
      raise ValueError("Нормативна ставка повинна бути числом з проміжку (0, 1)")
    
  def to_daily(self):
    match self.frequency:
      case TimePeriodType.DAY:
        return self.value
      case TimePeriodType.MONTH:
        # (1 + monthly_rate) ** (4 * 12) = (1 + daily_rate) ** (4 * 365 + 1)
        # daily_rate = ((1 + monthly_rate) ** (4 * 12)) ** (1 / (4 * 365 + 1)) - 1
        # daily_rate = ((1 + monthly_rate) ** 48) ** (1 / 1461) - 1
        return ((1 + self.value) ** (48 / 1461)) - 1
      case TimePeriodType.QUARTER:
        # (1 + quarterly_rate) ** (4 * 4) = (1 + daily_rate) ** (4 * 365 + 1)
        # daily_rate = ((1 + quarterly_rate) ** (4 * 4)) ** (1 / (4 * 365 + 1)) - 1
        # daily_rate = ((1 + quarterly_rate) ** 16) ** (1 / 1461) - 1
        return ((1 + self.value) ** (16 / 1461)) - 1
      case TimePeriodType.YEAR:
        # (1 + quarterly_rate) ** 4 = (1 + daily_rate) ** (4 * 365 + 1)
        # daily_rate = ((1 + quarterly_rate) ** 4)) ** (1 / 1461) - 1
        return ((1 + self.value) ** (4 / 1461)) - 1
      
  def __str__(self) -> str:
    format_str = f"Rate<відсотки: {self.value * 100}%%, тип: %s>"
    match self.frequency:
      case TimePeriodType.DAY:
        return format_str % "добова"
      case TimePeriodType.MONTH:
        return format_str % "місячна"
      case TimePeriodType.QUARTER:
        return format_str % "квартальна"
      case TimePeriodType.YEAR:
        return format_str % "річна"


@dataclass(frozen=True)
class RepaymentPeriod:
  start_date: datetime
  end_date: datetime
  
  def __post_init__(self):
    if self.start_date >= self.end_date:
      raise ValueError("Дата початку сплати кредиту повинна передувати даті завершення сплати кредиту")
