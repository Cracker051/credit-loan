from datetime import datetime
from dateutil.relativedelta import relativedelta
from enum import Enum


class TimePeriodType(Enum):
  DAY = 0
  MONTH = 1
  QUARTER = 2
  YEAR = 3


def calc_duration(start_date: datetime,
                  end_date: datetime,
                  unit_type: TimePeriodType) -> int:
  match unit_type:
    case TimePeriodType.DAY:
      return (end_date - start_date).days
    case TimePeriodType.MONTH:
      delta = relativedelta(end_date, start_date)
      return delta.years * 12 + delta.months
    case TimePeriodType.QUARTER:
      delta = relativedelta(end_date, start_date)
      return (delta.years * 12 + delta.months) // 4
    case TimePeriodType.YEAR:
      return relativedelta(end_date, start_date).years


def to_plural_str(time_period_type: TimePeriodType) -> str:
  match time_period_type:
    case TimePeriodType.DAY:
      return "дні"
    case TimePeriodType.MONTH:
      return "місяці"
    case TimePeriodType.QUARTER:
      return "квартали"
    case TimePeriodType.YEAR:
      return "роки"
